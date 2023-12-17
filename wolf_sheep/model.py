"""
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

import mesa

from .agents import SoilPatch, Grass, Bush, Tree, Mouse, Sheep, Cat, Wolf, FirePatch
from .scheduler import RandomActivationByTypeFiltered
import random


class WolfSheep(mesa.Model):
    """
    Wolf-Sheep Predation Model
    """

    height = 20
    width = 20

    initial_sheep = 10
    initial_wolves = 2

    sheep_reproduce = 0.04
    wolf_reproduce = 0.05


    grass = False
    grass_regrowth_time = 30

    grass_evolution_time = 5,
    bush_evolution_time = 5,

    verbose = False  # Print-monitoring

    description = (
        "A model simulating the phenomenon of ecological succession"
    )

    def __init__(
        self,
        width=20,
        height=20,
        initial_mice=10,
        initial_sheep=0,
        initial_cats=4,
        initial_wolves=0,
        mouse_reproduce=0.04,
        sheep_reproduce=0.04,
        cat_reproduce=0.05,
        wolf_reproduce=0.05,
        mouse_reproduce_energy=4,
        sheep_reproduce_energy=15,
        cat_reproduce_energy=10,
        wolf_reproduce_energy=20,
        mouse_evolution_time=5,
        sheep_evolution_time=5,
        cat_evolution_time=5,
        wolf_evolution_time=5,
        soil=False,
        grass_regrowth_time=30,
        grass_evolution_time = 5,
        bush_evolution_time = 5,
        soil_evolution_time = 5,
    ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.soil = soil
        self.grass_regrowth_time = grass_regrowth_time

        # counter
        self.cnt = 1

        # added
        self.initial_mice = initial_mice
        self.initial_cats = initial_cats
        self.mouse_reproduce = mouse_reproduce
        self.cat_reproduce = cat_reproduce
        self.mouse_reproduce_energy = mouse_reproduce_energy
        self.sheep_reproduce_energy = sheep_reproduce_energy
        self.cat_reproduce_energy = cat_reproduce_energy
        self.wolf_reproduce_energy = wolf_reproduce_energy
        self.mouse_evolution_time = mouse_evolution_time
        self.sheep_evolution_time = sheep_evolution_time
        self.cat_evolution_time = cat_evolution_time
        self.wolf_evolution_time = wolf_evolution_time

        self.grass_evolution_time = grass_evolution_time
        self.bush_evolution_time = bush_evolution_time
        self.soil_evolution_time = soil_evolution_time

        self.food_energies = {
            Grass: 4,
            Bush: 8,
            Tree: 12,
            Mouse: 8,
            Sheep: 20,
            Cat: 12,
        }
        ##

        self.schedule = RandomActivationByTypeFiltered(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            {
                "Mice": lambda m: m.schedule.get_type_count(Mouse),
                "Cats": lambda m: m.schedule.get_type_count(Cat),
                "Wolves": lambda m: m.schedule.get_type_count(Wolf),
                "Sheep": lambda m: m.schedule.get_type_count(Sheep),
                "Grass": lambda m: m.schedule.get_type_count(Grass),
                "Bush": lambda m: m.schedule.get_type_count(Bush),
                "Tree": lambda m: m.schedule.get_type_count(Tree),
            }
        )

        # Create mouse:
        for i in range(self.initial_mice):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(10)
            mouse = Mouse(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(mouse, (x, y))
            self.schedule.add(mouse)

        # Create sheep:
        for i in range(self.initial_sheep):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(20)
            sheep = Sheep(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create cats:
        for i in range(self.initial_cats):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(20)
            cat = Cat(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(cat, (x, y))
            self.schedule.add(cat)

        # Create wolves
        for i in range(self.initial_wolves):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            energy = self.random.randrange(30)
            wolf = Wolf(self.next_id(), (x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        # if self.grass:
        #     for agent, (x, y) in self.grid.coord_iter():
        #         fully_grown = self.random.choice([True, False])

        #         if fully_grown:
        #             countdown = self.grass_regrowth_time
        #         else:
        #             countdown = self.random.randrange(self.grass_regrowth_time)

        #         patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
        #         self.grid.place_agent(patch, (x, y))
        #         self.schedule.add(patch)

        # Create soil patches
        if self.soil:
            for agent, (x, y) in self.grid.coord_iter():
                level = self.random.choice([0, 1, 2, 3])
                if level > 0:
                    countdown = self.random.randrange(self.grass_regrowth_time)
                    grass = Grass(self.next_id(), (x, y), self,countdown)
                    self.grid.place_agent(grass, (x, y))
                    self.schedule.add(grass)
                patch = SoilPatch(self.next_id(), (x, y), self, level)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

        # for i in range(self.initial_wolves):
        #     x = self.random.randrange(self.width)
        #     y = self.random.randrange(self.height)
        #     energy = self.random.randrange(2 * self.wolf_gain_from_food)
        #     wolf = Wolf(self.next_id(), (x, y), self, True, energy)
        #     self.grid.place_agent(wolf, (x, y))
        #     self.schedule.add(wolf)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        self.cnt += 1
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    # self.schedule.get_type_count(Wolf),
                    # self.schedule.get_type_count(Sheep),
                    self.schedule.get_type_count(Grass),
                    self.schedule.get_type_count(Tree),
                    self.schedule.get_type_count(Bush),
                    self.schedule.get_type_count(SoilPatch), #, lambda x: x.fully_grown)
                ]
            )
        self.forest_fire()

    def run_model(self, step_count=200):
        if self.verbose:
            # print("Initial number wolves: ", self.schedule.get_type_count(Wolf))
            # print("Initial number sheep: ", self.schedule.get_type_count(Sheep))
            print(
                "Initial number grass: ",
                self.schedule.get_type_count(SoilPatch),
            )

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            # print("Final number wolves: ", self.schedule.get_type_count(Wolf))
            # print("Final number sheep: ", self.schedule.get_type_count(Sheep))
            print(
                "Final number grass: ",
                self.schedule.get_type_count(SoilPatch),
            )

    def forest_fire(self, period=100):
        if self.cnt % period == 0:
            total_cells = self.width * self.height
            cells_to_kill = random.sample(list(self.grid.coord_iter()), int(0.8*total_cells))
            print(cells_to_kill)

            for agents, (x, y) in cells_to_kill:
                # cell_content, x, y = self.grid[x][y]
                if agents:
                    for agent in agents:
                        if not isinstance(agent, SoilPatch):
                            self.grid.remove_agent(agent)
                            self.schedule.remove(agent)
                    fire = FirePatch(self.next_id(), (x, y), self)
                    self.grid.place_agent(fire, (x, y))
                    self.schedule.add(fire)
