import curses

from views.view import View
from views.screens import Screen
from views.input import *

from define import *
from hex import *
from data.skills import skill_list

from collections import deque
from random import choice

from text import *
from operator import itemgetter, attrgetter

import log

# Main tactical window class.
class Window(View):
    def __init__(self, window):
        View.__init__(self, window, TERM_X, TERM_Y)

    def ready(self):
        self.spawn(SidePane(self.screen))
        self.spawn(MainPane(self.screen))

# Larger, left-hand pane
class MainPane(View):
    def __init__(self, window):
        View.__init__(self, window, MAP_X, MAP_Y, MAP_START_X, MAP_START_Y)

    def ready(self):
        self.spawn(MainMap(self.screen, MAP_X, MAP_Y, MAP_START_X, MAP_START_Y))
        self.spawn(Status(self.screen, STATUS_X, STATUS_Y, STATUS_START_X, PANE_START_Y))
        self.spawn(Place(self.screen, STATUS_X+2, STATUS_Y, MAP_START_X, MAP_START_Y))

# Smaller, right-hand pane
class SidePane(View):
    def __init__(self, window):
        View.__init__(self, window, PANE_X, PANE_Y, PANE_START_X, PANE_START_Y)

    def ready(self):
        self.spawn(Stats(self.screen, PANE_X, STATS_Y, PANE_START_X, PANE_START_Y))
        self.spawn(LogViewer(self.screen, PANE_X, LOG_Y, PANE_START_X, LOG_START_Y))

# TODO: Make this a subclass of a Map view, to account for tactical/strategic/etc.
class MainMap(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        # -1 to account for 0,0 start
        self.viewport_pos = (int(y/2)-1, int(y/2)-1)
        self.viewport_rank = 10
        self.zoom = self.viewport_rank

        self.cursor = None

    def keyin(self, c):
        if c == ord('G') or c == ord('g'):
            self.player.get_all()
            return False

        if c == ord('}'):
            self.zoom = 2
            self.inherit()
            return False

        if c == ord('{'):
            self.zoom = self.viewport_rank
            self.inherit()
            return False

        if c == ord('N'):
#            if len(self.map.player.cell().items) > 1:
                self.spawn(TextPrompt(self.screen, self.width, self.height))
#            else:
#                self.map.player.get_all()
#            return False

        # TODO: Allow multiple open children.
        if not self.children:
            if c == ord('I') or c == ord('i'):
                self.spawn(Inventory(self.screen, self.width, self.height))
                return False

            elif c == ord('v'):
                if self.cursor is None:
                    self.cursor = self.spawn(Cursor(self.player.pos))
                    self.cursor.spawn(Examine(self.screen, self.width, 2, 0, self.BOTTOM-1))
                    return False

        if True is True:#else:
        # This is generally the last step before keys fall into oblivion.
        # TODO: Feed the keyin into a player function.
            if c == ord('7'):
                self.map.player.do(NW)
            elif c == ord('4'):
                self.map.player.do(CW)
            elif c == ord('1'):
                self.map.player.do(SW)
            elif c == ord('9'):
                self.map.player.do(NE)
            elif c == ord('6'):
                self.map.player.do(CE)
            elif c == ord('3'):
                self.map.player.do(SE)
            elif c == ord('5'):
                self.map.player.over()
            elif c == ord('>') or c == ord('<'):
                self.map.player.stairs()
            else: return True
            return False

    # Hex character function, for maps only.
    def hd(self, pos, glyph, col=None, attr=None):
        # Three sets of coords are involved:
        x, y = pos
        c_x, c_y = self.center
        v_x, v_y = self.viewport_pos

        # Offsets from the viewport center
        off_x = x - c_x
        off_y = y - c_y

        draw_x = off_y + 2*(off_x+v_x)
        draw_y = off_y + v_y

        assert self.undrawable((draw_x, draw_y)) is False, "hd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        try: self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))
        except curses.error: pass

    # Draw to offset hexes, i.e., the 'blank' ones.
    def offset_hd(self, pos, dir, glyph, col=None, attr=None):
        # Four sets of coords are involved:
        x, y = pos
        c_x, c_y = self.center
        v_x, v_y = self.viewport_pos
        d_x, d_y = dir

        # Offsets from the viewport center
        off_x = x - c_x
        off_y = y - c_y

        draw_x = off_y + 2*(off_x+v_x) + d_x
        draw_y = off_y + v_y + d_y

        assert self.undrawable((draw_x, draw_y)) is False, "offset hd function tried to draw out of bounds: %s at %s." % (self.__dict__, (draw_x, draw_y))
        try: self.window.addch(draw_y, draw_x, glyph, self.attr(col, attr))
        except curses.error: pass

    # Accepts viewport_rank offsets to figure out what part of the map is visible.
    def get_glyph(self, pos, subpositions=False):
        return self.map.cell(pos).draw(subpositions)

    def draw(self):
        if self.cursor is not None:
            self.center = self.cursor.pos
        else:
            self.center = self.player.pos

        cells = area(self.zoom, self.center)
        for cell, distance in cells.items():
            if self.map.valid(cell) is not False:
                glyph, col, subposition = self.get_glyph(cell)
            else:
                glyph = ','
                col = "red-black"
            # HACK: Multiple-zoom-level system.
            if self.zoom == self.viewport_rank:
                self.hd(cell, glyph, col)
            else:
                diff = sub(cell, self.center)
                pos = add(self.center, mult(diff, 4))
                # HACK: Move this into some generalized hex border function.
                faces = {NW: ("/", WW), NE : ("\\", EE), CE : ("|", EE), SE : ("/", EE), SW: ("\\",  WW), CW: ("|", WW)}
                for dir in dirs:
                    point = add(pos, dir)
                    self.hd(point, ".", "white-black")
                    face, offset = faces[dir]
                    self.offset_hd(point, offset, face, "white-black")
                    # NOTE: Interesting effect!
                    #self.hd(add(pos, mult(dir, 2)), faces[dir], "white-black")
                for glyph, col, subposition in self.get_glyph(cell, True):
                    self.hd(add(pos, subposition), glyph, col)

        if len(self.player.highlights) > 0:
            for highlight, pos in self.player.highlights.items():
                if dist(self.center, pos) > self.viewport_rank:
                    cells = line(self.center, pos, self.viewport_rank+2)
                    cell = cells.pop()
                    glyph, col = "*", "green-black"
                    self.hd(cell, glyph, col)

# A single line of text at the bottom of the screen describing what your
# cursor is currently over.
# TODO: Update for FOV
class Examine(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def keyin(self, c):
        if c == curses.KEY_ENTER or c == ord('\n'):
            if self.children:
                return True
            child = self.spawn(CharacterSheet(self.screen, PANE_X, PANE_Y, PANE_START_X, PANE_START_Y))
        else:
            return True
        return False

    def draw(self):
        pos = self.parent.pos
        cell = self.map.cell(pos)
        if not self.children:
            self.line("Space: Exit. Enter: Inspect. */: Style.")
        else:
            self.line("Space: Stop Inspecting. /*: Cursor style.")
        if cell is not None:
            string = cell.contents()
            self.line("Cursor: %s." % string)
        else:
            self.line("Cursor: There's... nothing. Nothing at all.")

class Stats(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        # Col 1: Skeleton/Paperdoll
        for line in self.player.paperdoll():
            self.cline(line)

        # Show the chosen weapon/attack option combination.
        weapon, attack_option = self.player.attackline()
        slot, appearance, trait, trait_level, item = weapon
        # Override this with the current value.
        trait_level = self.player.trait(trait)

        # Print reach
        # TODO: Move to weapon display function.
        reach = ""
        for dist in attack_option[3]:
            if reach:
                reach += ","
            if dist == 0:
                reach += "C"
            else:
                reach += "%s" % dist
            # TODO: selected reach for variable weaons
                #reach += "*"
        reach = "(%s)" % reach

        # HACK: Should ask the item to display a shorter appearance.
        self.cline("(/*) %s: %s" % (self.player.body.locs[slot].appearance(), appearance[:20]))

        color = "white-black"
        if self.player.base_skills.get(trait) is None:
            color = "red-black"

        self.cline("%s, <%s>%s-%s</>" % (self.player.body.locs[slot].appearance(), color, trait, trait_level))

        selector = ""
        if len(self.player.attack_options) > 1:
            selector = "(+-) "
        self.cline("%5s%s %s %s %s" % (selector, attack_option[0], self.player.damage(attack_option[1], False), attack_option[2], reach))

        # Col 2: Combat information
        self.x_acc += 12
        self.y_acc = 0
        self.statline('HP')
        self.statline('MP')
        self.statline('FP')
        self.line("")
        self.statline('Block')
        self.statline('Dodge')
        self.statline('Parry')

        # Col 3: Stats
        self.x_acc += 14
        self.y_acc = 0

        self.statline("ST")
        self.statline("DX")
        self.statline("IQ")
        self.statline("HT")
        self.line("")
        self.statline("Will")
        self.statline("Perception")
#        self.line("")
#        self.statline("Move")
#        self.statline("Speed")

        # Don't delete! Probably will reuse this for a 'health' screen.
        #self.line("Wounds:")
        #for loc in sorted(self.player.body.locs.items()):
        #    self.line("%6s: %s" % (loc[0], loc[1].wounds))

        #for x in range(10):
        #    self.line("Sample combat log text, line %d" % x)

    # Print a line like 'Dodge: 15' using stat()
    # TODO: Print colors, *s, etc. for more info.
    def statline(self, stat):
        # Always use the shortest label here.
        label = labels.get(stat)[0]
        value = self.player.stat(stat)
        if value is None:
            value = "n/a"

        # These particular stats actually have two stats to display.
        if stat in ["HP", "FP", "MP"]:
            self.line("%s: %3d/%2d" % (label, value, self.player.stat("Max"+stat)))
        else:
            self.line("%s: %s" % (label, value))

    def keyin(self, c):
        if c == ord("+"):
            self.player.choose_attack_option(1)
        elif c == ord("-"):
            self.player.choose_attack_option(-1)
        elif c == ord("*"):
            self.player.choose_weapon(1)
        elif c == ord("/"):
            self.player.choose_weapon(-1)
        else:
            return True
        return False

# TODO: Implement this
class Status(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
        shock = self.player.effects.get("Shock", 0)
        if shock > 0:
            if shock == 4:
                color = "magenta-black"
            elif shock == 3:
                color = "red-black"
            elif shock == 2:
                color = "yellow-black"
            else:
                color = "cyan-black"
            self.line("Shock", color)
        if self.player.effects.get("Stun") is not None:
            self.line("Stun", "red-black")
        if self.player.effects.get("Unconscious") is not None:
            self.line("KO'd", "red-black")
        if self.player.reeling() is True:
            self.line("Reeling", "red-black")
        if self.player.exhausted() is True:
            self.line("Exh", "yellow-black")
        return True

class Place(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def draw(self):
         self.line(self.map.level.name, "red-black")
         if self.map.name:
             self.line(self.map.name)

class LogViewer(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.autoscroll = True
        self.events = 0
        self.shrink = 2

    # Spawn a scroller and add the log to the map.
    def ready(self):
        self.scroller = self.spawn(Scroller(log.length() - self.height))

    def before_draw(self):
        if log.length() > self.events:
            max_scroll = max(0, log.length() - self.height)
            self.scroller.resize(max_scroll)
            if self.autoscroll is True:
                self.scroller.scroll(log.length() - self.events)
            self.events = log.length()

    def draw(self):
        # Start from the bottom:
        self.x_acc = 2
        self.y_acc = self.height
        index = self.scroller.max

        if self.scroller.index != self.scroller.max:
            self.y_acc -=1
            self.line("[...]")
            self.y_acc -=1
            index += 1

        everything = True
        for event in reversed(log.events()):
            index -= 1
            if index >= self.scroller.index:
                continue
            if self.logline(event) is False:
                self.y_acc = self.shrink
                self.line("[...]")
                everything = False
                break;

        if everything is False:
            self.x_acc = 0
            self.y_acc = self.shrink
            # TODO: Fix this, it's buggy!
            proportion = float(self.scroller.index) / (1+self.scroller.max)
            position = int(proportion * (self.height - self.y_acc - 1))        

            self.line("^")
            for x in range(self.height - self.y_acc - 1):
                if x+1 == position:
                    self.cline("<green-black>@</>")
                else:
                    self.line("|")
            self.line("v")

    def logline(self, event):
        lines = wrap_string([event], self.width - self.x_acc)

        # Move up by that much to offset what the line function would do.
        self.y_acc -= len(lines)

        # Couldn't fit it all.
        if self.y_acc - self.shrink < 1 and self.scroller.index != self.scroller.min:
            return False;

        # Otherwise, display the line(s):
        for line in lines:
            self.cline(line[0].capitalize() + line[1:])

        # Since we're moving in reverse.
        self.y_acc -= len(lines)

    # TODO: Fix tabbing only work when [...] or more logs.
    def keyin(self, c):
        if c == ord("\t"): # Tab
            if self.shrink > 0:
                self.shrink -= 5
            else:
                self.shrink += 5

class Inventory(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)

    def ready(self):
        self.scroller = self.spawn(Scroller())
        self.sidescroller = self.spawn(SideScroller(1))

    # Stored here for convenience.
    def before_draw(self):
        self.items = self.player.list_carried()
        self.slots = sorted(sorted(self.player.body.locs.values(), key=attrgetter("type"), reverse=True), key=attrgetter("sorting"))

        # Tabbing! (Very hackish/simple.)
        if self.sidescroller.index == 0:
            self.scroller.resize(len(self.items)-1)
        else:
            self.scroller.resize(len(self.slots)-1)

    def draw(self):
        self.window.clear()
        self.border(" ")
        self.cline("Inventory")
        self.y_acc += 1
        if len(self.items) > 0:
            for x in range(len(self.items)):
                appearance, items = self.items[x]
                if len(items) > 1:
                    string = "%d %ss" % (len(items), appearance)
                else:
                    string = appearance

                # Highlight tab, if present.
                if self.sidescroller.index == 0 and x == self.scroller.index:
                    self.cline("<green-black>%s</>" % string)
                else:
                    self.cline(string)
        else:
            self.cline("No items")

        self.y_acc += 1

        # Print what's on the ground, too.
        ground = self.map.player.cell().items
        if len(ground) > 0:
            self.cline("Ground:")
            self.y_acc += 1
            for appearance, items in ground.items():
                if len(items) > 1:
                    self.line("%d %ss" % (len(items), appearance))
                else:
                    self.line(appearance)

        self.y_acc = 0
        self.x_acc += 20

        # TODO: Fix this messaging.
        self.cline("Equipped")
        self.y_acc += 1
        for x in range(len(self.slots)):
            loc = self.slots[x]
            equipped = ""
            for appearance, items in loc.readied.items():
                for item in items: # Ick. Definitely need to move this printing!
                    if item.is_wielded():
                        equipped += "%s" % appearance # (wielded)
                    else:
                        equipped += "%s" % appearance # (readied)
            for appearance, items in loc.held.items():
                for item in items:
                    if not item.is_wielded():
                        equipped += "%s" % appearance # (held)
            for appearance, items in loc.worn.items():
                for item in items:
                    equipped += "%s" % appearance # (worn)

            # If we don't have a string yet:
            if not equipped:
                continue

            colon = "%s:" % loc.appearance()

            # Highlights.
            if self.sidescroller.index == 1 and x == self.scroller.index:
                self.cline("%-11s <green-black>%s</a>" % (colon, equipped))
            else:
                self.cline("%-11s %s" % (colon, equipped))

        self.x_acc = 0
        self.y_acc = self.BOTTOM - 2

        self.cline("Available actions:")
        actions = []
        # These actions depend on having a carried item.
        if self.sidescroller.index == 0 and len(self.items) > 0:
            appearance, items = self.items[self.scroller.index]
            if self.map.player.can_equip_item(appearance, self.player.body.locs.get(self.player.body.primary_slot)):
                actions.append("(<green-black>e</>)quip")

        elif self.sidescroller.index == 1:
            loc = self.slots[self.scroller.index]
            #for item in loc.items():
            # Hackish! Pop a random element from the set.
            items = loc.items()
            if len(items) > 0:
                item = loc.items().pop()
                if self.player._can_unequip_item(item):
                    actions.append("(<green-black>u</>)nequip")

        item = self.selected()
        if item is not None:
            if self.sidescroller.index == 0:
                if self.player.can_drop_item(item):
                    actions.append("(<green-black>d</>)rop")
            elif self.sidescroller.index == 1:
                if self.player._can_drop_item(item):
                    actions.append("(<green-black>d</>)rop")

        # Always visible, if there are items to get.
        if self.player.can_get_items():
            actions.append("(<green-black>G</>)et all")

        if actions:
            self.cline("  %s." % commas(actions))

    # HACK: Returns the seletected item (or appearance).
    def selected(self):
        if self.sidescroller.index == 0 and len(self.items) > 0:
            appearance, items = self.items[self.scroller.index]
            return appearance
        elif self.sidescroller.index == 1:
            loc = self.slots[self.scroller.index]
            #for item in loc.items():
            # Hackish! Pop a random element from the set.
            items = loc.items()
            if len(items) > 0:
                return items.pop()

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
        # Hack.
        elif c == ord('d'):
            if self.scroller.index == 0:
                self.player.drop(self.selected())
            else:
                self.player._drop(self.selected())
        elif c == ord('e'):
            self.player.equip(self.selected())#, self.player.body.locs.get(self.player.body.primary_slot))
        elif c == ord('u'):
            # This is also a hack.
            self.player._unequip(self.selected())
#        else: return True
        elif c == ord('G') or c == ord('g'):
            self.player.get_all()
            return False
        return False

class CharacterSheet(View):
    def __init__(self, window, x, y, start_x=0, start_y=0):
        View.__init__(self, window, x, y, start_x, start_y)
        self.actor = None
        self.text = []

    def ready(self):
        self.scroller = self.spawn(Scroller())
        self.sidescroller = self.spawn(SideScroller())

    def keyin(self, c):
        if c == ord(' '):
            self.suicide()
        else:
            return True
        return False

    def draw(self):
        self.border(" ")
        pos = self.cursor.pos
        actors = self.map.actors(pos)

        # Abort early if no actor.
        if not actors:
            self.cline("There's nothing interesting here.")
            return False

        self.actor = actors[self.cursor.selector.index]

        if len(actors) > 1:
            scroller = "<green-black>"
        else:
            scroller = "<red-black>"

        self.cline('%s(+-)</> %s' % (scroller, self.actor.appearance()))
        self.cline("-"*self.width)

        self.text = wrap_string(self.actor.character_sheet(), self.width)
        self.scroller.resize(len(self.text)-self.height + 2) # To account for the possibility of hidden lines

        offset = 0

        if self.scroller.index > 0:
            self.cline('[...]')
            offset += 1

        maxlines = self.height - self.y_acc

# TODO: Generalize this.
        for x in range(maxlines):
            if self.y_acc+1 == self.height and self.scroller.index < self.scroller.max:
                self.cline('[...]')
                break;

            index = self.scroller.index + x + offset
            line = self.text[index]
            self.cline(line)
        return False # Block further drawing if we drew.

# TODO: Add a minimap and a health screen.
#class MiniMap(View):
#class Health(View):