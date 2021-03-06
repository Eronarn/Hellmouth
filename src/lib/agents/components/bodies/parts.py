import random

from src.lib.agents.components.manipulation import Grasped, Wielded
from src.lib.objects.items.item import Natural
from src.lib.objects.items.carrion import PartialCorpse

from src.lib.util.define import *

# Hit location
class BodyPart(object):
    def __init__(self, type, owner):
        self.type = type
        self.owner = owner

        # Combat stats
        self.hp = 0
        self.dr = 0
        self.wounds = []
        self.natural_weapons = []
        """Natural weapons."""

        self.multipliers = {
            "pi-" : .5,
            "cut" : 1.5,
            "pi+" : 1.5,
            "imp" : 2,
            "pi++" : 2,
        }

        # Connectivity
        self.parent = None
        self.children = []
        self.sublocations = []

        # Item-related
        self.grasped = []
        self.worn = []

        # A layer can have multiple items (like several rings).
        self.layers = [[]]

        self.sorting = 0
        self.crippleable = True
        self.manipulator = False

        self.min_reach = 0
        self.max_reach = 0

    def trigger(self, *triggers):
        """Respond to triggers."""
        if "added_natural_weapon" or "removed_natural_weapon" or "wielded" or "unwielded" or "grasped" or "ungrasped" in triggers:
            for natural_weapon in self.natural_weapons:
                natural_weapon.trigger("rebuild")
            self.owner.call("Combat", "trigger", "rebuild")

    def appearance(self):
        appearance = hit_locations.get(self.type)
        if self.severed() is True:
            appearance = "severed " + appearance
        elif self.dismembered() is True:
            appearance = "maimed " + appearance
        elif self.crippled() is True:
            appearance = "crippled " + appearance
        return appearance

    def descendants(self):
        descendants = [self]
        if self.children:
            for child in self.children:
                descendants.extend(child.descendants())
        return descendants

    # Return a list of unique items.
    def items(self):
        # DARK MAGIC
        items = set()

        for itemlist in self.held.values():
            items.update(itemlist)
        for itemlist in self.readied.values():
            items.update(itemlist)
        for itemlist in self.worn.values():
            items.update(itemlist)

        return items

    """Natural weapon getter methods."""

    def get_natural_weapons(self):
        """Yield this Part's natural weapons."""
        for natural_weapon in self.natural_weapons:
            yield natural_weapon

    def has_natural_weapon(self):
        """Return whether this Part has any natural weapons."""
        if self.natural_weapons:
            return True
        return False

    """Natural weapon setter methods."""

    def add_natural_weapon(self, natural_weapon, trigger=True):
        """Add a natural weapon to this Part."""
        natural_weapon.append_component(Wielded(owner=natural_weapon, controller=self.owner, manipulator=self))
        self.natural_weapons.append(natural_weapon)
        if trigger:
            self.trigger("added_natural_weapon")

    def remove_natural_weapon(self, natural_weapon, trigger=True):
        """Remove a natural weapon from this Part."""
        self.natural_weapons.remove(natural_weapon)
        for component in self.get_wielded_components(natural_weapon):
            natural_weapon.remove_component(component)
        if trigger:
            self.trigger("removed_natural_weapon")

    """Grasping getter methods."""

    def get_grasped(self):
        for agent in self.grasped:
            yield agent

    """Grasping setter methods."""

    def do_grasp(self, agent, trigger=True):
        """Grasp an Agent."""
        agent.append_component(Grasped(owner=agent, controller=self.owner, manipulator=self))
        self.grasped.append(agent)
        if trigger:
            self.trigger("grasped")
        return True

    def do_ungrasp(self, agent, trigger=True):
        """Ungrasp an Agent."""
        self.grasped.remove(agent)
        for component in agent.get_controlled_components(self.owner, "Grasped"):
            agent.remove_component(component)
        if trigger:
            self.trigger("ungrasped")
        return True

    """Grasping helper methods."""

    def has_grasped(self):
        """Return whether this Part has any grasped Agents."""
        for agent in self.get_grasped():
            return True
        return False

    def can_grasp(self, agent):
        """Return whether an Agent can be grasped."""
        if agent in self.get_grasped():
            return False
        return True

    def could_grasp(self):
        """Return whether an unspecified Agent could be grasped."""
        if self.has_grasped():
            return False
        return True

    def can_ungrasp(self, agent):
        """Return whether an Agent can be ungrasped."""
        if agent in self.get_grasped():
            return False
        return True

    def could_ungrasp(self):
        """Return whether an unspecified Agent could be ungrasped."""
        if self.has_grasped():
            return False
        return True

    def is_grasp(self, agent):
        if agent in self.get_grasped():
            return True
        return False

    def is_ungrasp(self, agent):
        return not self.is_grasp(agent)

    """Wielding getter methods."""

    def get_wielded(self):
        """Yield this Part's wielded Agents."""
        for agent in self.get_grasped():
            for component in agent.get_controlled_components(self.owner, "Wielded"):
                yield agent
                break

    """Wielding setter methods."""

    def do_wield(self, agent, trigger=True):
        """Set a grasped Agent as wielded."""
        agent.append_component(Wielded(owner=agent, controller=self.owner, manipulator=self))
        agent.call("Wielded", "trigger", "rebuild")
        if trigger:
            self.trigger("wielded")
        return True

    def do_unwield(self, agent, trigger=True):
        """Set a grasped Agent as unwielded."""
        for component in agent.get_controlled_components(self.owner, "Wielded"):
            agent.remove_component(component)
        if trigger:
            self.trigger("unwielded")
        return True

    """Wielding helper methods."""

    def has_wielded(self):
        """Return whether this part has any wielded Agents."""
        for agent in self.get_wielded():
            return True
        return False

    def can_wield(self, agent):
        """Return whether an Agent can be wielded."""
        if agent in self.get_wielded():
            return False
        return True

    def could_wield(self):
        """Return whether an unspecified Agent could be wielded."""
        if self.has_wielded():
            return False
        return True

    def can_unwield(self, agent):
        """Return whether an Agent can be unwielded."""
        if agent not in self.get_wielded():
            return False
        return True

    def could_unwield(self):
        """Return whether an unspecified Agent could be unwielded."""
        if not self.has_wielded():
            return False
        return True

    def is_wield(self, agent):
        if agent in self.get_wielded():
            return True
        return False

    def is_unwield(self, agent):
        return not self.is_wield(agent)

    """Manipulator getter methods."""

    def get_manipulate(self):
        """Return whether the Part is a manipulator."""
        return self.manipulator

    """Manipulator helper methods."""

    # STUB
    def can_manipulate(self):
        """Return whether a Part can serve as a manipulator."""
        if not self.manipulator:
            return False

        if self.crippled():
            return False

        return True

    def get_reach(self):
        """Returns the min and max reach of this BodyPart, exclusive of other factors."""
        return self.min_reach, self.max_reach

    # def weapons(self, natural=True, wielded=True, improvised=False):
    #     found_weapons = {}
    #     if natural is True:
    #         for appearance, weapons in self.attack_options.items():
    #             if self.holding() is False or random.choice(weapons).requires_empty_location is False:
    #                 found_weapons[appearance] = weapons
    #     if wielded is True:
    #         for appearance, weapons in self.readied.items():
    #             found_weapons[appearance] = weapons
    #     return found_weapons

    # Information about this location.
    def get_view_data(self, view=None):
        yield self.appearance()
        wielded = [wielded for wielded in self.get_wielded()]

        # TODO: formatting function here
        for agent in wielded:
            yield "  " + "%s (wielded)" % agent.appearance()

        for agent in self.get_grasped():
            if agent not in wielded:
                yield "  " + "%s (grasped)" % agent.appearance()

        for agent in self.get_natural_weapons():
            yield "  " + "%s (natural)" % agent.appearance()

        # TODO: worn items
        # for agent in self.get_worn():
        #     yield "%s (worn)" % agent.appearance()

    # Return the healthiness of the limb
    # TODO: Injured status for extremities, rather than using 'major wound'.

    def status(self):
        wounds = sum(self.wounds)
        if wounds == 0:
            return UNHURT
        elif self.crippleable is True:
            if self.severed() is True:                    return SEVERED
            elif self.dismembered() is True:              return DISMEMBERED
            elif self.crippled() is True:                 return CRIPPLED
            elif sum(self.wounds) > 1:                    return INJURED
            else:                                         return SCRATCHED
        else:
            if wounds > self.owner.MaxHP() * 2:           return DISMEMBERED
            elif wounds > self.owner.MaxHP():             return CRIPPLED
            elif wounds > self.owner.MaxHP() / 2:         return INJURED
            else:                                         return SCRATCHED

    # Set up a parent/child relationship.
    def add_child(parent, child):
        parent.children.append(child)
        child.parent = parent

    # Add a sublocation of this part.
    def sublocation(self, part):
        self.sublocations.append(part)

    # # ITEMS
    # # Return whether we're holding anything.
    # def holding(self):
    #     if len(self.held) > 0:
    #         return True
    #     return False

    # # STUB: Can we hold the item?
    # def can_hold(self, item):
    #     # HACK: It's possible to hold multiple items.
    #     if self.holding():
    #         return False
    #     return True

    # def hold(self, item):
    #     held = self.held.get(item.appearance(), [])
    #     held.append(item)
    #     self.held[item.appearance()] = held
    #     item.held.append(self)

    # def ready(self, item):
    #     readied = self.readied.get(item.appearance(), [])
    #     readied.append(item)
    #     self.readied[item.appearance()] = readied
    #     item.readied.append(self)

    # def wear(self, item):
    #     worn = self.worn.get(item.appearance(), [])
    #     worn.append(item)
    #     self.worn[item.appearance()] = worn
    #     item.worn.append(self)

    # def unhold(self, item):
    #     held = self.held.pop(item.appearance(), [])
    #     held.remove(item)
    #     if held:
    #         self.held[item.appearance()] = held
    #     item.held.remove(self)

    # def unready(self, item):
    #     readied = self.readied.pop(item.appearance(), [])
    #     readied.remove(item)
    #     if readied:
    #         self.readied[item.appearance()] = readied
    #     item.readied.remove(self)

    # def unwear(self, item):
    #     worn = self.worn.pop(item.appearance(), [])
    #     worn.remove(item)
    #     if worn:
    #         self.worn[item.appearance()] = worn
    #     item.worn.remove(self)

    # COMBAT

    # Calculate what happens when a limb is hit, but don't actually apply the
    # effects, in order to handle simultaneous actions.
    def prepare_hurt(self, attack):
        # TODO: (Source, DR blocked) for messaging
        # TODO: Damage to items.
        # TODO: Min damage properly
        attack["basic_damage_blocked"] = self.DR()
        attack["penetrating_damage"] = max(0, attack["basic_damage"] - attack["basic_damage_blocked"])
        attack["multiplier"] = self.multiplier(attack["damage_type"])
        # No wound is necessarily no injury.
        if attack["penetrating_damage"] <= 0:
            attack["wound"] = 0
            attack["injury"] = 0
        else:
            # Wounds are always at least one damage, but they may not cause injury.
            attack["wound"] = max(1, int(attack["penetrating_damage"] * attack["multiplier"]))

            # Any hit location can suffer a major wound.
            if attack["wound"] > self.owner.MaxHP()/2:
                attack["major_wound"] = True

            # Less complicated case.
            if self.crippling() is False:
                attack["injury"] = attack["wound"]

            # More complicated case: some hit locations can be crippled.
            else:
                if attack["wound"] > self.crippling():
                    attack["major_wound"] = True
                    attack["crippling_wound"] = True
                    if attack["wound"] > 2*self.crippling():
                        attack["dismembering_wound"] = True

                # Further damage to a crippled limb causes wounds - but it
                # doesn't cause further injury over the crippling amount!
                if self.crippled() is True:
                    attack["injury"] = 0

                # Cap damage based on max crippling damage, then figure out
                # if this attack caused crippling or dismemberment.

                # This *won't* cause a major wound because it represents the
                # slow build-up of injury rather than a large wound.
                else:
                    attack["injury"] = min(attack["wound"] + sum(self.wounds), 1 + self.crippling()) - sum(self.wounds)

                    # If the wound itself wouldn't have caused crippling, but
                    # it's pushed the limb over the edge to become crippled:
                    if attack["wound"] + sum(self.wounds) > self.crippling():
                        attack["crippled"] = True

                    # Likewise, but for dismemberment.
                    if attack["wound"] + sum(self.wounds) > 2*self.crippling():
                        attack["dismembered"] = True

    # TODO: Remove.
    def DR(self):
        dr = 0
        for item in self.worn:
            dr += item.DR()
        dr += self.dr + self.owner.DR()
        return dr

    def get_dr_glyph(self):
        """Display a glyph representing this part's DR."""
        dr = self.DR()
        if dr == 0:
            return " "
        elif dr < 10:
            return dr
        else:
            return "+"

    def get_dr_colors(self, fg=True, bg=True):
        """Display a color representing this part's DR."""
        dr = self.DR()

        if self.severed() or dr == 0:
            if fg and bg:
                return "black-black"
            else:
                return "black"
        else:
            if fg and bg:
                return "cyan-black"
            elif fg:
                return "cyan"
            else:
                return "black"

    # TODO: Make this more useful for display
    def multiplier(self, type):
        return self.multipliers.get(type, 1)

    # Add a wound to this location.
    # TODO: Better tracking of wounds.
    def hurt(self, attack):
        self.wounds.append(attack["wound"])

        # BLOOD EVERYWHERE
        if attack.get("severing wound") is True:
            self.sever(attack)
            if self.owner.controlled is True:
                self.owner.screen("ouch", {"body_text" : self.owner.limbloss(attack)})

    def sever(self, attack):
        # Store the original.
        original = self.owner
        # Generate a corpse.
        corpse = PartialCorpse(original)
        # Get affected parts.
        parts = self.descendants()
        # Reset the corpse's locations.
        corpse.actor.body.locs = {}
        # Stick the affected parts in the corpse and change their owner.
        for part in parts:
            # Change the part's owner.
            part.owner = corpse.actor
            # Store the same part object in the copy's locations.
            corpse.actor.body.locs[part.type] = part
            # Delete the part from the original actor.
            # TODO: Just mark as severed instead?
            del original.body.locs[part.type]
        # Put the corpse in the cell.
        original.cell().put(corpse)

    # Return a color for the limb status.
    def get_color(self, fg=True, bg=True):
        status = self.status()
        if fg:
            if status == SEVERED:       fg = "black"
            elif status == DISMEMBERED: fg = "magenta"
            elif status == CRIPPLED:    fg = "red"
            elif status == INJURED:     fg = "yellow"
            elif status == SCRATCHED:   fg = "cyan" # TODO: Change color.
            else:                       fg = "green"
        if fg and bg:
            return "%s-black" % fg
        if fg:
            return fg
        elif bg:
            return "black"

    # Returns the damage that must be *exceeded* to cripple a limb.
    def crippling(self):
        return False

    # Is the limb crippled yet?
    def crippled(self):
        if self.crippling() is not False:
            if sum(self.wounds) > self.crippling():
                return True
        return False

    # Is the limb dismembered yet?
    def dismembered(self):
        if self.crippling() is not False:
            if sum(self.wounds) > 2*self.crippling():
                return True
        return False

    # STUB: Better severed status.
    def severed(self):
        return False
        if self.status() == SEVERED:
            return True
        if self.parent is not None:
            return self.parent.severed()
        else:
            return False

# Arms, legs, pseudopods, etc.
class Limb(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["pi++"] = 1
        self.multipliers["pi+"] = 1
        self.multipliers["imp"] = 1

        self.crippleable = True

    # Returns the damage that must be *exceeded* to cripple a limb.
    def crippling(self):
        return self.owner.MaxHP()/2

class Leg(Limb):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

    def sever(self, attack):
        self.owner.knockdown()
        Limb.sever(self, attack)

# Hands, feet, etc.
class Extremity(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["pi++"] = 1
        self.multipliers["pi+"] = 1
        self.multipliers["imp"] = 1

        self.crippleable = True

    # Returns the damage that must be *exceeded* to cripple an extremity.
    def crippling(self):
        return self.owner.MaxHP()/3

class Hand(Extremity):
    def __init__(self, type, owner):
        super(Hand, self).__init__(type, owner)
        self.manipulator = True

class Foot(Extremity):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

    def sever(self, attack):
        self.owner.knockdown()
        Extremity.sever(self, attack)

# Brain containment
class Skull(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.dr = 2

        self.multipliers["tox"] = 1

    # QUAD DAMAGE
    def multiplier(self, type):
        return self.multipliers.get(type, 4)

# Internal organs.
class Vitals(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["pi-"] = 3
        self.multipliers["pi"] = 3
        self.multipliers["pi+"] = 3
        self.multipliers["pi++"] = 3
        self.multipliers["imp"] = 3

# Squishy seeing organs
class Eye(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["tox"] = 1

    # QUAD DAMAGE
    def multiplier(self, type):
        return self.multipliers.get(type, 4)

    # Eyes are very easy to cripple.
    def crippling(self):
        return self.owner.MaxHP()/10

# Face.
class Face(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["corr"] = 1.5

# Neck
class Neck(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["cr"] = 1.5
        self.multipliers["corr"] = 1.5
        self.multipliers["cut"] = 2
