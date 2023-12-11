from .random_walk import RandomWalker
from .agents import GrassPatch

# zwierzęta -> roślinożerne: (jeden je trawe tylko drugi je krzaki i drzewa) , mięsożerne (dwa gatunki: jeden małe, drugi duże)
#

class Mouse(RandomWalker):
    """
    A mouse that walks around, reproduces (asexually) and eats grass.
    """
    pass

class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and eats grass, bushes and trees.
    """

    energy = None
    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        self.random_move()
        living = True

        if self.model.grass:
            self.energy -= 2

            this_cell = self.model.grid.get_cell_list_contents([self.pos])
            plants = [obj for obj in this_cell if isinstance(obj, (GrassPatch))]
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
            if self.model.grass:
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
            if self.random.random() < self.model.cat_reproduce_chance:
                # Create a new kitten
                self.energy /= 2
                kitty = Cat(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(kitty, kitty.pos)
                self.model.schedule.add(kitty)
        elif self.energy > self.model.cat_reproduce_energy and self.countup > self.model.cat_evolution_time:
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
            if self.random.random() < self.model.wolf_reproduce_chance:
                # Create a new wolf cub
                self.energy /= 2
                cub = Wolf(
                    self.model.next_id(), self.pos, self.model, self.moore, self.energy
                )
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)

