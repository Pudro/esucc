"""
Predator behavior
"""

from typing import Tuple
import mesa
from .random_walk import RandomWalker


class Predator(RandomWalker):
    """
    Base class for predatory behavior
    """
    def __init__(self, unique_id, pos, model, prey, moore=True):
        super().__init__(unique_id, pos, model, moore)
        self.prey = prey

    def hunt(self):
        # Check for nearby Sheep in a two-grid radius
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=1)
        prey_neighbors = [agent for agent in neighbors if isinstance(agent, self.prey)]

        if prey_neighbors:
            # Find the closest Sheep
            closest_prey = min(prey_neighbors, key=lambda x: self.manhattan_distance(self.pos, x.pos))

            # Move towards the closest Sheep
            self.move_towards(closest_prey.pos)

        else:
            # If no Sheep nearby, take a random step
            self.random_move()

    def move_towards(self, target_pos):
        """
        Move towards the target position.
        """
        possible_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        distances = [self.manhattan_distance(move, target_pos) for move in possible_moves]

        # Find the move that minimizes the distance to the target
        best_move = possible_moves[distances.index(min(distances))]

        # Move to the selected position
        self.model.grid.move_agent(self, best_move)

    def manhattan_distance(self, pos1, pos2):
        """
        Calculate the Manhattan distance between two positions.
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
