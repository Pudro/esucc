import mesa

from .random_walk import RandomWalker


# class Sheep(RandomWalker):
#     """
#     A sheep that walks around, reproduces (asexually) and gets eaten.

#     The init is the same as the RandomWalker.
#     """

#     energy = None

#     def __init__(self, unique_id, pos, model, moore, energy=None):
#         super().__init__(unique_id, pos, model, moore=moore)
#         self.energy = energy

#     def step(self):
#         """
#         A model step. Move, then eat grass and reproduce.
#         """
#         self.random_move()
#         living = True

#         if self.model.grass:
#             # Reduce energy
#             self.energy -= 1

#             # If there is grass available, eat it
#             this_cell = self.model.grid.get_cell_list_contents([self.pos])
#             grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
#             if grass_patch.fully_grown:
#                 self.energy += self.model.sheep_gain_from_food
#                 grass_patch.fully_grown = False

#             # Death
#             if self.energy < 0:
#                 self.model.grid.remove_agent(self)
#                 self.model.schedule.remove(self)
#                 living = False

#         if living and self.random.random() < self.model.sheep_reproduce:
#             # Create a new sheep:
#             if self.model.grass:
#                 self.energy /= 2
#             lamb = Sheep(
#                 self.model.next_id(), self.pos, self.model, self.moore, self.energy
#             )
#             self.model.grid.place_agent(lamb, self.pos)
#             self.model.schedule.add(lamb)


# class Wolf(RandomWalker):
#     """
#     A wolf that walks around, reproduces (asexually) and eats sheep.
#     """

#     energy = None

#     def __init__(self, unique_id, pos, model, moore, energy=None):
#         super().__init__(unique_id, pos, model, moore=moore)
#         self.energy = energy

#     def step(self):
#         self.random_move()
#         self.energy -= 1

#         # If there are sheep present, eat one
#         x, y = self.pos
#         this_cell = self.model.grid.get_cell_list_contents([self.pos])
#         sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
#         if len(sheep) > 0:
#             sheep_to_eat = self.random.choice(sheep)
#             self.energy += self.model.wolf_gain_from_food

#             # Kill the sheep
#             self.model.grid.remove_agent(sheep_to_eat)
#             self.model.schedule.remove(sheep_to_eat)

#         # Death or reproduction
#         if self.energy < 0:
#             self.model.grid.remove_agent(self)
#             self.model.schedule.remove(self)
#         else:
#             if self.random.random() < self.model.wolf_reproduce:
#                 # Create a new wolf cub
#                 self.energy /= 2
#                 cub = Wolf(
#                     self.model.next_id(), self.pos, self.model, self.moore, self.energy
#                 )
#                 self.model.grid.place_agent(cub, cub.pos)
#                 self.model.schedule.add(cub)

class SoilPatch(mesa.Agent):
    """
    A patch of soil, it represents the soil conditions that allow various plants to grow, level 0 - nothing grows, 1 - only Grass, 2 - Grass and Bush, 3 - Grass, Bush and Tree
    """

    def __init__(self, unique_id, pos, model, level):
        """
        Creates a new patch of soil

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.level = level
        self.pos = pos
        self.countup = 0

    def step(self):
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        cell_obj = [obj for obj in this_cell if isinstance(obj, (Tree, Grass, Bush))]

        if len(cell_obj) == 0:
            self.countup += 1
            if self.countup > self.model.soil_evolution_time and self.level >= 1:
                grass = Grass(self.model.next_id(), self.pos, self.model,self.model.grass_regrowth_time)
                self.model.grid.place_agent(grass, self.pos)
                self.model.schedule.add(grass)
                self.countup = 0


class Grass(mesa.Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by 
    """

    def __init__(self, unique_id, pos, model, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
            countup: Time after the patch of grass was fully grown
        """
        super().__init__(unique_id, model)
        self.fully_grown = False
        self.countdown = countdown
        self.countup = 0
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
        else:
            self.countup += 1

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        soil_patch = [obj for obj in this_cell if isinstance(obj, SoilPatch)][0]
        if self.fully_grown and self.countup > self.model.grass_evolution_time and soil_patch.level > 1:
            pos = self.pos
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            bush = Bush(self.model.next_id(), pos, self.model)
            self.model.grid.place_agent(bush, pos)
            self.model.schedule.add(bush)



# living = True

#         if self.model.grass:
#             # Reduce energy
#             self.energy -= 1

#             # If there is grass available, eat it
#             this_cell = self.model.grid.get_cell_list_contents([self.pos])
#             grass_patch = [obj for obj in this_cell if isinstance(obj, GrassPatch)][0]
#             if grass_patch.fully_grown:
#                 self.energy += self.model.sheep_gain_from_food
#                 grass_patch.fully_grown = False

#             # Death
#             if self.energy < 0:
#                 self.model.grid.remove_agent(self)
#                 self.model.schedule.remove(self)
#                 living = False

#         if living and self.random.random() < self.model.sheep_reproduce:
#             # Create a new sheep:
#             if self.model.grass:
#                 self.energy /= 2
#             lamb = Sheep(
#                 self.model.next_id(), self.pos, self.model, self.moore, self.energy
#             )
#             self.model.grid.place_agent(lamb, self.pos)
#             self.model.schedule.add(lamb)


class Bush(mesa.Agent):
    """
    
    """

    def __init__(self, unique_id, pos, model):
        """
        Creates a bush

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
            countup: Time after the patch of grass was fully grown
        """
        super().__init__(unique_id, model)
        self.countup = 0
        self.pos = pos

    def step(self):
        self.countup += 1

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        soil_patch = [obj for obj in this_cell if isinstance(obj, SoilPatch)][0]
        if self.countup > self.model.bush_evolution_time and soil_patch.level > 2:
            pos = self.pos
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            tree = Tree(self.model.next_id(), pos, self.model)
            self.model.grid.place_agent(tree, pos)
            self.model.schedule.add(tree)


class Tree(mesa.Agent):
    """
    
    """

    def __init__(self, unique_id, pos, model):
        """
        Creates a bush

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
            countup: Time after the patch of grass was fully grown
        """
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

# class GrassPatch(mesa.Agent):
#     """
#     A patch of grass that grows at a fixed rate and it is eaten by sheep
#     """

#     def __init__(self, unique_id, pos, model, fully_grown, countdown):
#         """
#         Creates a new patch of grass

#         Args:
#             grown: (boolean) Whether the patch of grass is fully grown or not
#             countdown: Time for the patch of grass to be fully grown again
#         """
#         super().__init__(unique_id, model)
#         self.fully_grown = fully_grown
#         self.countdown = countdown
#         self.pos = pos

#     def step(self):
#         if not self.fully_grown:
#             if self.countdown <= 0:
#                 # Set as fully grown
#                 self.fully_grown = True
#                 self.countdown = self.model.grass_regrowth_time
#             else:
#                 self.countdown -= 1
