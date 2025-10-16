# Agent.py
import random
import typing
from Percept import Percept
from Action import GOFORWARD, TURNLEFT, TURNRIGHT, GRAB, SHOOT, CLIMB
from Orientation import RIGHT, LEFT, UP, DOWN


class Agent:
    """The Agent class, which decides the action to take."""

    def __init__(self):
        """Constructor, called only once for a new agent."""
        self.action: int = -1
        self.location: list[int] = [1, 1]
        self.has_arrow: bool = True
        self.has_gold: bool = False
        self.orientation: int = RIGHT
        pass

    def __del__(self):
        """Destructor, called when the agent is deleted."""
        pass

    def Initialize(self):
        """
        Called at the start of each new game or 'try' in the same world.
        Use this to reset any agent state.
        """
        self.action: int = -1
        self.location: list[int] = [1, 1]
        self.has_arrow: bool = True
        self.has_gold: bool = False
        self.orientation: int = RIGHT
        pass

    def Turn(self, direction: int):
        if direction == TURNLEFT:
            self.orientation += 1
            self.action = TURNLEFT
        elif direction == TURNRIGHT:
            self.orientation -= 1
            self.action = TURNRIGHT

    # def Move(self, direction: int):
    #     """
    #     Moves based on current orientation
    #     """
    #     if direction == GOFORWARD:
    #     elif direction == TURN

    def Process(self, percept: Percept) -> int:
        """
        The main decision-making function.
        Called every turn with the agent's current percepts.
        Must return a valid action as int.
        """
        self.action = -1
        while True:
            if percept.glitter:
                action = GRAB
                self.has_gold = True
            # If the agent is in the (1,1) location and has the gold, then CLIMB.
            elif self.location == [1, 1] and self.has_gold:
                action = CLIMB
            # If the agent has an arrow, and the agent is in the top row (Y=4),
            # and the agent’s orientation=RIGHT, then SHOOT.
            elif self.has_arrow and self.orientation is RIGHT:
                action = SHOOT
                self.has_arrow = False
            # If the agent has an arrow, and the agent is in the rightmost column (X=4),
            # and the agent’s orientation=UP, then SHOOT.
            elif self.has_arrow and self.orientation is UP:
                action = SHOOT
                self.has_arrow = False
            # If none of the above conditions are met, then the agent should randomly choose one
            # of the actions: GOFORWARD, TURNLEFT, TURNRIGHT
            else:
                choice = random.randint(0, 2)
                match choice:
                    case 0:
                        action = GOFORWARD
                    case 1:
                        action = self.Turn(TURNLEFT)
                    case 2:
                        action = self.Turn(TURNRIGHT)
                    case _:
                        print(
                            "Error in none case. Likely the random action generator is broken.")
            return action
