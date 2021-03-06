# The player character(s).
from src.lib.agents.actors.actor import Actor
from src.lib.agents.components.equipment import Equipment
from src.lib.agents.components.manipulation import ManipulatingAgent
from src.lib.agents.components.status import Status

class PC(Actor):
    def __init__(self, components=[]):
        super(PC, self).__init__(components)
        self.glyph = '@'
        self.name = 'adventurer'
        self.color = 'cyan'
        self.description = "Some hapless adventurer who stumbled across the arena. It looks pretty feeble."
        self.highlights = {}

        self.points["traits"]["DX"] += 100
        self.points["traits"]["ST"] += 100
        self.build(200)
        self.recalculate()
        self.controlled = True