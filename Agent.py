# Agent.py
import random
from Percept import Percept
from Action import GOFORWARD, TURNLEFT, TURNRIGHT, GRAB, SHOOT, CLIMB
from Orientation import RIGHT, LEFT, UP, DOWN


class Agent:
    """The Agent class, which decides the action to take."""

    def __init__(self):
        """Constructor, called only once for a new agent."""
        self.action: int = -1
        self.last_action: int = -1
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
        self.last_action: int = -1
        self.location: list[int] = [1, 1]
        self.has_arrow: bool = True
        self.has_gold: bool = False
        self.orientation: int = RIGHT

    def Turn(self, direction: int):
        if direction == TURNLEFT:
            self.orientation += 1
            self.orientation %= 4
            return TURNLEFT
        if direction == TURNRIGHT:
            self.orientation -= 1
            self.orientation %= 4
            return TURNRIGHT

    def Move(self, bump: bool = False) -> int:
        """
        Moves based on current orientation
        """
        # If we bump, undo the move operation.
        if bump:
            if self.orientation == LEFT:
                # Undo Increase x by 1
                self.location[0] += 1
            elif self.orientation == RIGHT:
                # Undo Decrease x by 1
                self.location[0] -= 1
            elif self.orientation == UP:
                # Undo Increase y by 1
                self.location[1] -= 1
            elif self.orientation == DOWN:
                # Undo Decrease y by 1
                self.location[1] += 1
            return -1
        else:
            if self.orientation == LEFT:
                # Increase x by 1
                self.location[0] -= 1
            elif self.orientation == RIGHT:
                # Decrease x by 1
                self.location[0] += 1
            elif self.orientation == UP:
                # Increase y by 1
                self.location[1] += 1
            elif self.orientation == DOWN:
                # Decrease y by 1
                self.location[1] -= 1
                return GOFORWARD

    def Process(self, percept: Percept) -> int:
        """
        The main decision-making function.
        Called every turn with the agent's current percepts.
        Must return a valid action as int.
        """
        self.action = -1
        # If we bump, undo the movement and try again.
        if percept.bump:
            # Undo movement
            self.Move(bump=True)

        if percept.glitter:
            action = GRAB
            self.has_gold = True
        # If the agent is in the (1,1) location and has the gold, then CLIMB.
        elif self.location == [1, 1] and self.has_gold:
            action = CLIMB
        # If the agent has an arrow, and the agent is in the top row (Y=4),
        # and the agent’s orientation=RIGHT, then SHOOT.
        elif self.has_arrow and self.orientation == RIGHT and self.location[1] == 4:
            action = SHOOT
            self.has_arrow = False
        # If the agent has an arrow, and the agent is in the rightmost column (X=4),
        # and the agent’s orientation=UP, then SHOOT.
        elif self.has_arrow and self.orientation == UP and self.location[0] == 4:
            action = SHOOT
            self.has_arrow = False
        # If none of the above conditions are met, then the agent should randomly choose one
        # of the actions: GOFORWARD, TURNLEFT, TURNRIGHT
        else:
            choice = random.randint(0, 2)
            match choice:
                case 0:
                    action = self.Move(bump=False)
                case 1:
                    action = self.Turn(TURNLEFT)
                case 2:
                    action = self.Turn(TURNRIGHT)
                case _:
                    print(
                        "Error in none case.")
        self.last_action = self.action
        return action
