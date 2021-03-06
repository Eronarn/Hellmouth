from src.lib.util.dice import *
from src.lib.generators.maps import meat
from src.lib.generators.items import ItemGenerator, generate_item
from src.lib.data.generators.items import generators
from src.lib.maps.encounter import Encounter
from src.lib.data import screens
from src.lib.util.hex import *

# TODO: Genericize this class.
class MeatArena():
    def __init__(self, player):
        # References.
        self.player = player
        self.map = None
        self.destination = None

        # DISPLAY:
        # Descriptive information about the level itself.
        self.name = "The Meat Arena"
        self.screens = []

        # Handle anything that should happen before arriving at this level is guaranteed.
        self.before_arrive()

    # The level portion of the game loop.
    def loop(self):
        if self.map is not None:
            # If the map has a destination, go to it.
            if self.map.loop() is False:
                self.go(self.map.destination)

        # Don't continue looping if we have a destination.
        if self.destination is not None:
            return False

        # Get screens from the map.
        self.screens.extend(self.map.screens)
        self.map.screens = []

    # Go to a specific map.
    def go(self, destination):
        # If this is called with False as a destination, there are no more maps.
        if destination is False:
            return self.before_leave(destination)

        # Otherwise, generate the map and trigger before_arrive() in it.
        self.generate_map(destination)
        self.map.before_arrive()

    # Functions called (before/when) (arriving at/leaving) the level.
    def before_arrive(self):
        self.arrive()

    def arrive(self):
        # When arriving at a level, go to its first map.
        self.go(1)

    def before_leave(self, destination):
        return self.leave(destination)

    def leave(self, destination):
        self.destination = destination

    # Generate a map. The destination parameter can be anything, but depth makes a
    # lot of sense. It's up to you to use it (or not).
    def generate_map(self, destination):
        # Create the map.
        self.map = Encounter(self)

        # Configure map settings, typically based on depth (destination).
        self.configure_map(destination)

        # Call the map's terrain generator
        self.map.generate_terrain()

        # Monster placement.
        self.place_monsters(destination)

        # Loot placement.
        self.place_items(destination)

    # Configure the map. (Here, we use destination as a depth parameter.)
    def configure_map(self, destination):
        self.map.depth = destination

        # Map properties that are the same for all depths.
        self.map.name = "Floor %s" % self.map.depth
        self.map.floor = (".", "white-black")
        self.map.layout = meat.MeatArena

        if self.map.depth < 5:
            self.map.exits = { "down" : (self.map.depth+1, ANYWHERE) }

        # TODO: Move these to other level classes.
        if self.map.depth == 5:
            self.name = "The Grand Gate"
            self.map.name = None
            self.map.exits = {}# "down" : (MeatArena, (25, 0)) }
            self.map.layout = meat.MeatTunnel
#        if depth == 4:
#            self.map.name = "Caves of Primal Meat"
#            self.map.exits = self.exits
#            self.map.layout = meat.MeatArena
#        if depth == 5:
#            self.map.name = "Sauce Vats"
#            self.map.exits = self.exits
#            self.map.layout = meat.MeatArena
#        if depth == 6:
#            self.map.name = "Tower of the Sauceror"
#            self.map.exits = None
#            self.map.layout = meat.MeatTower

    # TODO: Hand this off to mapgen?
    def place_monsters(self, depth):
        if depth == 5:
            from actors.npc import MeatCommander
            monster = MeatCommander()
            monster.generate_equipment()
            self.map.put(monster, (25, 0))
            return True

        # Define NPCs to be placed
        from src.games.meat_arena.agents.actors.monsters import MeatSlave, MeatWorm, MeatGolem, MeatHydra
        monsters = [MeatSlave] * 10
        for x in range(depth-1 * 3):
            monsters.append(MeatWorm)
        for x in range(depth-1 * 2):
            monsters.append(MeatGolem)
        for x in range(depth-1 * 1):
            monsters.append(MeatHydra)

        # Place monsters
        num_mons = sum(roll(r1d6, depth+1))
        cells = area(self.map.center, self.map.size)
        while num_mons > 0:
            monster = random.choice(monsters)()
            monster.generate_equipment()
            monster.trigger("spawned")
            pos = random.choice(cells)
            if self.map.put(monster, pos) is not False:
                num_mons -= 1

    def place_items(self, depth):
        item_count = r3d6() + 10 + depth
        generator = ItemGenerator(generators)
        for x in range(item_count):
            item = generator.random_item("weapons")
            random.choice(self.map.cells.values()).put(item)