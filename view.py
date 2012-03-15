import curses
import math
import hex
from lifepath import Lifepath

# Cycling selector.
class Selector():
    def __init__(self, parent, choices, initial=0):
        self.parent = parent
        self.choices = choices
        self.choice = initial

    def next(self):
        self.choice += 1
        if self.choice > self.choices:
            self.choice = 0

    def prev(self):
        self.choice -= 1
        if self.choice < 0:
            self.choice = self.choices

    def choose(self):
        self.parent.selector = self.choice

class View():
    def __init__(self, window, x, y, startx, starty):
        self.window = window.subwin(y, x, starty, startx)
        self.x = startx
        self.y = starty
        self.x_acc = 0
        self.y_acc = 0

    # Rectangular character function.
    def rd(self, x, y, glyph):
        self.window.addch(y, x, glyph)

    # Rectangular string function.
    def rds(self, x, y, string):
        self.window.addstr(y, x, string)

    # Draw a line; only relevant for text-y views.
    def line(self, str):
        self.rds(0+self.x_acc, 0+self.y_acc, str)
        self.y_acc += 1

    def reset(self):
        self.x_acc = 0
        self.y_acc = 0

class MainMap(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)
        self.map = None
        self.player = None
        # -1 to account for 0,0 start
        self.viewport = (math.floor(y/2)-1, math.floor(y/2)-1)
        self.viewrange = 11

    # Called before the map is rendered, but after it's ready to go.
    def ready(self):
        return

    # Hex character function, for maps only.
    def hd(self, x, y, glyph):
        # X/Y are offsets from the map center
        X = x - self.player.pos[0]
        Y = y - self.player.pos[1]
        # TERRIBLE HACK
        if glyph == '"':
            self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph, curses.A_DIM)
        elif glyph == '@':
            self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph, curses.A_STANDOUT)
        elif glyph == 'A':
            self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph, curses.A_STANDOUT)
        else: 
            self.window.addch(self.viewport[1]+Y, 2*(self.viewport[0]+X)+Y, glyph)

    # Accepts viewrange offsets to figure out what part of the map is visible.
    def get_glyph(self, x, y):
        return self.map.cells[min(self.map.width-1, x)][min(self.map.height-1, y)].draw()

    def draw(self):
        hexes = []
        hex.iterator(hexes, self.player.pos[0], self.player.pos[1], self.viewrange)

        minX = 0
        maxX = self.map.width-1
        minY = 0
        maxY = self.map.height-1

#        print hexes
#        exit()

        for h in hexes:
            if h[0] < minX or h[0] > maxX or h[1] < minY or h[1] > maxY:
                glyph = '"'
            else:
                glyph = self.get_glyph(h[0], h[1])

            self.hd(h[0], h[1], glyph)

        # Draw the actors
#        for actor in self.actors:
#            self.hd(self.viewrange+1+actor.pos[0]-self.player.pos[0],\
#                    self.viewrange+1+actor.pos[1]-self.player.pos[1],\
#                    actor.glyph)

        self.window.refresh()

class Stats(View):
    short = { "Speed" : "Spd.",
              "Perception" : "Per.",
              "Strength" : "ST",
              "Dexterity" : "DX",
              "Intelligence" : "IQ",
              "Health" : "HT",
              "Hit Points" : "HP",
              "Fatigue Points" : "FP",
              "Mana Points" : "MP",
}

    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)
        self.player = None

    def draw(self):
        # Col 1
        self.reset()

        self.line("-"*12)
        for x in range(10):
            self.line("-"+" "*10+"-")
        self.line("-"*12)

        # Col 2
        self.x_acc += 12
        self.y_acc = 0

        self.statline('Hit Points')
        self.statline('Mana Points')
        self.statline('Fatigue Points')
        self.line("")
        self.statline('Block')
        self.statline('Dodge')
        self.statline('Parry')

        # Col 3
        self.x_acc += 12
        self.y_acc = 0

        self.statline("Strength")
        self.statline("Dexterity")
        self.statline("Intelligence")
        self.statline("Health")
        self.line("")
        self.statline("Will")
        self.statline("Perception")
        self.line("")
        self.statline("Move")
        self.statline("Speed")

        # Combat Log
        #self.x_acc = 0
        #self.y_acc += 4

        #for x in range(10):
        #    self.line("Sample combat log text, line %d" % x)

    # Retrieve stat
    def stat(self, stat):
        return self.player.stat(stat)

    # Print a line like 'Dodge: 15' using stat()
    def statline(self, stat):
#        self.line("HP: %3d/%2d" % (-50, 10))
#        self.line("FP: %3d/%2d" % (10, 12))
#        self.line("MP: %3d/%2d" % (8, 15))

        short = Stats.short.get(stat, stat)
        if short in ["HP", "FP", "MP"]:
            self.line("%s: %3d/%2d" % (short, self.stat(stat), self.stat("Max"+stat)))
        else:
            self.line("%s: %s" % (short, self.stat(stat)))

class Chargen(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)
        self.selector = Selector(self, 5)
        self.lifepath = Lifepath()

    def draw(self):
#        self.rds(0, 10, lifepath)
        if hasattr(self.selector, 'parent'):
            self.rds(0, 23, "Currently selected option: %s" % self.selector.choice)
        else:
            self.rds(0, 23, "Final option was: %s" % self.selector)

#class MiniMap(View):
#class Health(View):

class Status(View):
    def __init__(self, window, x, y, startx, starty):
        View.__init__(self, window, x, y, startx, starty)

    def draw(self):
        self.reset()
        self.line("")
        self.line("")
        self.line("Pain")
        self.line("Shock")
