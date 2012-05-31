from dice import *
from generators.maps import meat
from maps.encounter import Encounter
from data import screens

class MeatArena():
    depth = 1

    def __init__(self):
        self.name = "A strange, meaty arena"
        self.floor = (".", "white-black")
        self.exits = { "down" : (MeatArena, None) }
        self.map = None
        self.generate_map()
        self.place_monsters()
        self.screens = []
        self.generate_screens()

    # Just returns depth, but can be overridden for strings/etc.
    def current_depth(self):
        return self.__class__.depth

    def check_depth(self):
        depth = self.current_depth()

        if depth == 1 or depth == 2:
            self.map.name = "Meat Arena"
            self.map.exits = self.exits
            self.map.layout = meat.MeatArena
        if depth == 3:
            self.map.name = "Grand Gate"
            self.map.exits = { "down" : (MeatArena, (25, 0)) }
            self.map.layout = meat.MeatTunnel
        if depth == 4:
            self.map.name = "Caves of Primal Meat"
            self.map.exits = self.exits
            self.map.layout = meat.MeatArena
        if depth == 5:
            self.map.name = "Sauce Vats"
            self.map.exits = self.exits
            self.map.layout = meat.MeatArena
        if depth == 6:
            self.map.name = "Tower of the Sauceror"
            self.map.exits = None
            self.map.layout = meat.MeatTower

    # Map generation.
    def generate_map(self):
        self.map = Encounter()
        self.map.level = self
        self.check_depth()
	self.map.generate_terrain()

    # TODO: Hand this off to mapgen?
    def place_monsters(self):
        # Define NPCs to be placed
        from actors.npc import MeatSlave, MeatWorm, MeatGolem, MeatHydra
        monsters = [MeatSlave, MeatSlave, MeatSlave, MeatSlave, MeatWorm, MeatWorm, MeatGolem, MeatHydra] 

        # Place monsters
        num_mons = self.map.size / 2 + r3d6()
        for x in range(num_mons):
            monster = random.choice(monsters)
            monster = monster()
            self.map.put(monster, (self.map.center[0] + flip()*random.randint(1, self.map.size), self.map.center[1] + flip() * random.randint(1,self.map.size)))

    def generate_screens(self):
        screen = screens.text.get("meat-%s" % self.current_depth())
        if screen is not None:
            screen["header_right"] = self.name
            screen["footer_text"] = screens.footer
            self.screens.append(screen)
