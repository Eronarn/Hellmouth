import random
from objects.items.modifiers import *

# Items.
class Item():
    def __init__(self):
        # Flavor
        self.name = "debugger"
        self.description = "Debug description"
        self.glyph = "?"
        self.color = "red-black"

        # Basic characteristics
        self.size = None
        self.hp = None
        self.hp_max = None
        self.dr = None
        self.effects = None
        self.slots = None

        # Construction
        self.quality = None
        self.material = None
        self.construction = None

        # References. These just need to be lists, not dicts, because we don't care about the appearances involved.
        self.held = []
        self.readied = []
        self.worn = []

    # STUB: Figure out appearance here, based on provided precision options, statuses, etc.
    def appearance(self):
        return "%s %s" % (self.material.appearance, self.name)

    # STUB: Preferred slot for this kind of item.
    def preferred_slot(self):
        return 'RHand'

    # STUB: Hit an item.
    def hit(self):
        return False

    # STUB: Do damage to an item.
    def damage(self, amt):
        return False

    def DR(self):
        dr = self.dr
        if self.construction:
            dr += self.construction.dr
        if self.material:
            dr += self.material.dr
        if self.quality:
            dr += self.quality.dr
        return dr
    # Whether the item is intended to be used as a weapon. Note that
    # some objects, like torches or shields, fit into this category
    # despite not being 'weapon' objects.
    def can_be_weapon(self):
        return False

    # Whether this particular weapon needs an emmpty 'hand' to be used. True for almost everything.
    def requires_empty_location(self):
        return False
	
    # Whether the item is intended to be worn. Note that some objects,
    # like bags, might be perfectly serviceable wearables without being
    # armor or clothing.
    def can_be_worn(self):
        return False

    # Return true if the item is held, or with optional loc parameter,
    # if the item is held by a specific location.
    def is_held(self, loc=None):
        if loc is None:
            if len(self.held) > 0:
                return True
        else:
            if held.count(loc) > 0:
                return True
        return False

    # Return true if the item is being readied, or with optional loc parameter,
    # if the item is readied by a specific location.
    def is_readied(self, loc=None):
        if loc is None:
            if len(self.readied) > 0:
                return True
        else:
            if readied.count(loc) > 0:
                return True
        return False

    # Return true if the item is being worn, or with optional loc parameter,
    # if the item is worn by a specific location.
    def is_worn(self, loc=None):
        if loc is None:
            if len(self.worn) > 0:
                return True
        else:
            if worn.count(loc) > 0:
                return True
        return False

    # Return true if the item is being wielded - held and readied (possibly
    # in a specific location), and not worn (anywhere).
    def is_wielded(self, loc=None):
        if self.is_worn():
            return False
        if self.is_held(loc) and self.is_readied(loc):
            return True
        return False

    # Is the item being worn or held (optionally in a specific loc)?
    def is_equipped(self, loc=None):
        if self.is_worn(loc) or self.is_held(loc):
            return True
        assert self.is_readied(loc) is False, "Item wasn't worn or held, but still managed to be readied."
        return False

    # Return spike damage.
    def spikes(self):
        if hasattr(self, 'spikes'):
            return self.spikes
        else:
            return None

class Armor(Item):
    def __init__(self):
        Item.__init__(self)
        self.material = Bone
        self.glyph = "["

    def can_be_worn(self):
        return True

    def can_be_weapon(self):
        return False

class Weapon(Item):
    def __init__(self):
        Item.__init__(self)
        self.material = Bone
        self.glyph = "/"
        self.color = "cyan-black"

        # Combat-only stats
        self.primary_skill = None # Primary skill, for descriptions - there can be others.
        self.attack_options = {} # Min ST in attackline

    def can_be_weapon(self):
        return True

    def requires_empty_location(self):
        return True

class Broadsword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Broadsword"

class Shortsword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Shortsword"
        self.glyph = ","

class Knife(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Knife"
        self.glyph = ","

class Dagger(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Knife"
        self.glyph = ","

class Axe(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Axe/Mace"
        self.glyph = "{"
        self.color = "red-black"

class Mace(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Axe/Mace"
        self.glyph = "{"
        self.color = "blue-black"

class Pick(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Axe/Mace"
        self.glyph = "{"
        self.color = "red-black"

class Hammer(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Axe/Mace"
        self.glyph = "{"
        self.color = "blue-black"

class Club(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Broadsword"
        self.glyph = "/"
        self.color = "yellow-black"

class Flail(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Flail"
        self.glyph = "{"
        self.color = "cyan-black"

class Pollaxe(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Polearm"
        self.glyph = "|"
        self.color = "red-black"

class Spear(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Spear"
        self.glyph = "|"
        self.color = "yellow-black"

class Staff(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Staff"
        self.glyph = "|"
        self.color = "green-black"

class Natural(Weapon):
    def __init__(self):
        Weapon.__init__(self)
        self.primary_skill = "Brawling"

    # HACK: Not true of all!
    def requires_empty_location(self):
        return True

class Tool(Item):
    def __init__(self):
        Item.__init__(self)