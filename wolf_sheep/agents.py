import mesa

from .random_walk import RandomWalker


class Mouse(RandomWalker):
    """
    A mouse that walks around, reproduces (asexually) and eats grass.
    """
    energy = None
    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.countup = 0

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.countup += 1
        self.random_move()
        living = True

        self.energy -= 1

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        plants = [obj for obj in this_cell if isinstance(obj, (Grass))]
        if len(plants) > 0:
            plant_to_eat = self.random.choice(plants)
            self.energy += self.model.food_energies[plant_to_eat.__class__]

            self.model.grid.remove_agent(plant_to_eat)
            self.model.schedule.remove(plant_to_eat)

        # Death
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        elif self.energy > self.model.mouse_reproduce_energy:
            if self.random.random() < self.model.mouse_reproduce:
                # Create a new mouse
                self.energy /= 2
                mouse = Mouse(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(mouse, mouse.pos)
                self.model.schedule.add(mouse)
        if self.energy > self.model.mouse_reproduce_energy and self.countup > self.model.mouse_evolution_time:
            pos = self.pos
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            sheep = Sheep(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(sheep, pos)
            self.model.schedule.add(sheep)

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and eats grass, bushes and trees.
    """
    energy = None
    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy
        self.countup = 0

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.countup += 1
        self.random_move()
        living = True

        self.energy -= 2

        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        plants = [obj for obj in this_cell if isinstance(obj, (Grass, Bush))]
        if len(plants) > 0:
            plant_to_eat = self.random.choice(plants)
            self.energy += self.model.food_energies[plant_to_eat.__class__]

            self.model.grid.remove_agent(plant_to_eat)
            self.model.schedule.remove(plant_to_eat)

        # Death
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            living = False

        if living and self.random.random() < self.model.sheep_reproduce:
            # Create a new sheep:
            self.energy /= 2
            lamb = Sheep(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(lamb, self.pos)
            self.model.schedule.add(lamb)

class Cat(RandomWalker):
    """
    A cat that walks around, reproduces (asexually) and eats mice.
    """
    def __init__(self, unique_id, pos, model, moore, energy=None, max_energy=50, reproduction_threshold=None):
        super().__init__(unique_id, pos, model)
        self.energy = energy
        self.countup = 0

    def step(self):
        self.countup += 1
        self.random_move()
        # Bigger animals have bigger energy requirements
        self.energy -= 1

        # If there are is any animal present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        animals = [obj for obj in this_cell if isinstance(obj, (Mouse))]
        if len(animals) > 0:
            animal_to_eat = self.random.choice(animals)
            self.energy += self.model.food_energies[animal_to_eat.__class__]

            # Kill the animal
            self.model.grid.remove_agent(animal_to_eat)
            self.model.schedule.remove(animal_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        elif self.energy > self.model.cat_reproduce_energy:
            if self.random.random() < self.model.cat_reproduce:
                # Create a new kitten
                self.energy /= 2
                kitty = Cat(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(kitty, kitty.pos)
                self.model.schedule.add(kitty)
        if self.energy > self.model.cat_reproduce_energy and self.countup > self.model.cat_evolution_time:
            pos = self.pos
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
            wolf = Wolf(
                self.model.next_id(), self.pos, self.model, self.moore, self.energy
            )
            self.model.grid.place_agent(wolf, pos)
            self.model.schedule.add(wolf)

class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats cats, sheep and mice.
    """
    def __init__(self, unique_id, pos, model, moore, energy=None, max_energy=50, reproduction_threshold=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        # Bigger animals have bigger energy requirements
        self.energy -= 2

        # If there are is any animal present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        animals = [obj for obj in this_cell if isinstance(obj, (Mouse, Sheep, Cat))]
        if len(animals) > 0:
            animal_to_eat = self.random.choice(animals)
            self.energy += self.model.food_energies[animal_to_eat.__class__]

            # Kill the animal
            self.model.grid.remove_agent(animal_to_eat)
            self.model.schedule.remove(animal_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid.remove_agent(self)
            self.model.schedule.remove(self)
        elif self.energy > self.model.wolf_reproduce_energy:
            if self.random.random() < self.model.wolf_reproduce:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)

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
        self.countup_tree = 0
        self.countup_bush = 0
        self.countup_grass = 0


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
        else:
            
            if isinstance(cell_obj[0], (Tree)):
                self.countup_tree += 1
                if self.countup_tree > 200:
                    self.level -= 1
                    self.countup_tree = 0
                    self.model.grid.remove_agent(cell_obj[0])
                    self.model.schedule.remove(cell_obj[0])
            elif isinstance(cell_obj[0], (Bush)):
                self.countup_bush += 1
                if self.countup_bush > 100 and self.level < 4:
                    self.level += 1
                    self.countup_bush = 0
                # self.model.grid.remove_agent(cell_obj[0])
                # self.model.schedule.remove(cell_obj[0])
            elif isinstance(cell_obj[0], (Grass)):
                self.countup_grass += 1
                if self.countup_grass > 150 and self.level < 4:
                    self.level += 1
                    self.countup_grass = 0
                # self.model.grid.remove_agent(cell_obj[0])
                # self.model.schedule.remove(cell_obj[0])

                


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
