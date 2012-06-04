from copy import deepcopy

from objects.items.item import Item
from text import *

# Corpses!
class Corpse(Item):
    def __init__(self, actor):
        Item.__init__(self)

        # Basic characteristics.
        # TODO: Derive these from the actor.
        #self.size = None
        #self.hp = None
        #self.hp_max = None
        #self.dr = None
        #self.effects = None
        #self.slots = None

        self.actor = deepcopy(actor)

    def appearance(self):
        return self.actor.appearance() + " corpse"

class PartialCorpse(Corpse):
    def __init__(self, actor):
        Corpse.__init__(self, actor)

    def appearance(self):
        return self.actor.appearance() + " " + commas(self.actor.body.locs.keys())