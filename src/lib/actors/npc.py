# Derived from the Actor class, NPCs:
# 1) Do not check keyin
# 2) Have AI to control them
# 3) Do need any interface niceties (e.g., figuring out item letters)

from actor import Actor
import ai.astar
from hex import *
import body

class NPC(Actor):
    def __init__(self):
        Actor.__init__(self)

        # TODO: Make an AI class.

        # AI-related properties.
        self.target = None

        self.astar = None
        self.destination = None
        self.distance = None
        self.path = False

        self.attempts = 0

    # AI actions. Currently: move in a random direction.
    def act(self):
        assert self == self.map.acting, "An actor tried to act when not the acting actor."
        assert self.controlled is not True, "A player-controlled actor tried to hit AI code."

        repath = False
        if self.target is None:
            return self.retarget()

        self.attempts += 1
        if self.attempts > 10:
            self.over()
            return False

        self.distance = dist(self.pos, self.target.pos)
        if self.preferred_reach(self.distance) is True:
            self.do(sub(self.target.pos, self.pos))
            return False

        # TODO: Refactor some of this so that it is less buggy, but for now, it kinda-sorta-works.
        if self.distance > 1 and self.path is False:
            repath = True
        if self.destination != self.target.pos:
            if random.randint(1, dist(self.destination, self.target.pos)) == 1:
                repath = True

        # TODO: More intelligently decide when to re-path
        if repath is True:
            # TODO: Get target stuff in here.
            if self.target is not None:
                self.destination = self.target.pos
                self.repath()

            # i.e., a list with no entries
        if not self.path:
            self.path = False # Remove the empty list
        else:
            pos = self.path.pop()
            dir = sub(pos, self.pos)
            # HACK
            if dir not in dirs:
                self.path.append(pos)
                dir = CC
            elif self.map.cell(pos).blocked(dir) is True:
                for alt_dir in arc(dir):
                    alt_pos = add(self.pos, alt_dir)
                    # Prefer unoccupied cells, but accept sharing.
                    if self.map.cell(alt_pos).occupied() is False:
                        dir = alt_dir
                        break
                    elif self.map.cell(alt_pos).blocked(alt_dir) is False:
                        dir = alt_dir

            if self.do(dir) is False:
                # Chance to flat out abandon the path
                if r1d6() == 6:
                    self.path = False
                else:
                    # Try again
                    self.path.append(pos)

        # This should only happen if stuff is adjacent and without a path.
#        else:
#            dir = sub(self.target.pos, self.pos)
#            self.do(dir)

    # Reset A* and generate a new path.
    def repath(self):
        self.astar = ai.astar.AStar(self.map)
        self.path = self.astar.path(self.pos, self.destination)

    def retarget(self):
        if self.map.player is not None:
            if random.randint(1, dist(self.pos, self.map.player.pos)) == 1:
                self.target = self.map.player
                self.destination = self.target.pos
                self.repath()
                return True
        return False
            

# Monster definitions. TODO: Move elsewhere.

class MeatSlave(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '@'
        self.name = 'meat slave'
        self.color = 'yellow'
        self.description = "A pitiful wretch who long ago abandoned all hope of escaping the arena. It has covered itself in lunchmeat to hide its scent from the other occupants."

        self.loadouts = ["light armor", "knives"]
        self.generator = "slave"
        self.build(25)

class MeatGolem(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '8'
        self.name = 'meat golem'
        self.color = 'blue'
        self.description = "A lumbering construct made of a great many pieces of spoiled meat. They appear to have been stapled together."
        self.voice = None
        self.generator = "wild"
        self.build(50)

    # HACK: To be removed when the advantage works.
    def DR(self):
        return 3

class MeatWorm(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.body = body.Vermiform(self)
        self.glyph = '~'
        self.name = 'meat worm'
        self.color = 'magenta'
        self.description = "This worm looks like a large stick of pepperoni. A trail of grease glistens behind it."
        self.voice = "screech"

        self.generator = "wild"
        self.build(10)

class MeatHydra(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = 'D'
        self.name = 'meat hydra'
        self.color = 'magenta'
        self.description = 'A hydra made from the meat of lesser beings. Each "head" is a cracked ribcage.'
        self.voice = "roar"

        self.generator = "wild"
        self.build(50)

class MeatCommander(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = 'C'
        self.name = 'Meat Commander'
        self.color = 'magenta'
        self.description = "This beefy champion wears a full set of bone armor decorated with dozens of veal medallions and bacon ribbons. A crown roast rests atop its noble brow."

        self.generator = "elite"
        self.build(700)
        self.loadouts = ["heavy weapon", "heavy armor"]

class Sauceror(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '@'
        self.name = 'Sauceror'
        self.color = 'magenta'
        self.description = "A slight figure clad in dark cloth robes. Its flesh is pale and unappetizing, but its brain is perhaps the meatiest of all."

        self.generator = "sauceror"
        self.build(400)