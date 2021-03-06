import curses

from src.lib.components.component import Component
from src.lib.components.views.view import View

from src.lib.util.define import *
from src.lib.util.geometry.hexagon import Hexagon as H
from src.lib.util import text

# TODO: Rewrite Scroller and Selector in a more OO way with more flexible input options

class Input(Component):
    """Basic input Component. Does not render itself."""
    def __init__(self, **kwargs):
        super(Input, self).__init__(**kwargs)

# Scroll up/down.
class Scroller(Input):
    def __init__(self, max=0, min=0, initial=0, **kwargs):
        super(Scroller, self).__init__(**kwargs)
        self.min = min
        self.max = max
        self.index = initial

    def resize(self, max_sz, min_sz=0):
        self.min = max(0,min_sz)
        self.max = max(0,max_sz)
        self.scroll(0)

    def scroll(self, amt):
        self.index += amt
        if self.min is not None:
            if self.index < self.min:
                self.index = self.min
        if self.max is not None:
            if self.index > self.max:
                self.index = self.max

    # TODO: Convert into an input Trait.
    def process(self, command):
        if command("up"):
            self.scroll(-1)
            command.done()
        elif command("down"):
            self.scroll(1)
            command.done()

# Same as a scroller, but only left/right.
class SideScroller(Scroller):
    # TODO: Convert into an input Trait.
    def process(self, command):
        if command("left"):
            self.scroll(-1)
            command.done()
        elif command("right"):
            self.scroll(1)
            command.done()

# Scroller that initializes with a set of choices.
class Chooser(Scroller):
    def __init__(self, choices=[], initial=0, **kwargs):
        self.choices = choices
        super(Chooser, self).__init__(max=len(self.choices)-1, min=0, initial=initial, **kwargs)

    def resize(self):
        super(Chooser, self).resize(len(self.choices)-1)

    def get_choice(self):
        """Return the currently selected choice."""
        if self.choices and self.index is not None:
            return self.choices[self.index]

    def get_choices(self):
        """Return the available choices."""
        return self.choices

    def set_choices(self, choices):
        """Set a new list of choices and resize accordingly."""
        self.choices = choices
        self.resize()

# Same as a Chooser, but only left/right.
class SideChooser(Chooser):
    # TODO: Convert into an input Trait.
    def process(self, command):
        if command("left"):
            self.scroll(-1)
            command.done()
        elif command("right"):
            self.scroll(1)
            command.done()

# Chooser that tabs back and forth.
class Tabber(Chooser):
    def process(self, command):
        if command("previous tab"):
            self.scroll(-1)
            command.done()
        elif command("next tab"):
            self.scroll(1)
            command.done()

# Primary cycling selector, controlled with + and -.
class Selector(Scroller):
    def process(self, command):
        if command("previous choice"):
            self.scroll(-1)
            command.done()
        elif command("next choice"):
            self.scroll(1)
            command.done()

    # Jump to a specific value, if it's valid.
    def scroll_to(self, choice):
        if choice <= self.max and choice >= self.min:
            self.index = choice

    # Scroll, but loop back if necessary.
    def scroll(self, amt):
        self.index += amt
        if self.min is not None:
            if self.index < self.min:
                self.index = self.max
        if self.max is not None:
            if self.index > self.max:
                self.index = self.min

# Secondary cycling selector, controlled with / and *.
class SecondarySelector(Selector):
    def process(self, command):
        if command("previous mode"):
            self.scroll(-1)
            command.done()
        elif command("next mode"):
            self.scroll(1)
            command.done()

class Cursor(Input):
    styles = {
        "<>"  : [("<", H.WW), (">", H.EE)],
        "{}"  : [("{", H.WW), ("}", H.EE)],
        "[]"  : [("[", H.WW), ("]", H.EE)],
        "()"  : [("(", H.WW), (")", H.EE)],
        # TODO: Make 1hex prettier using unicode.
        "1hex" : [("^", H.NN), ("v", H.SS), ("|", H.EE), ("|", H.WW)],
        "2hex" : [
            ("/", H.NW + 2*H.WW),#add(H.NW, add(H.NW, H.NW))),
            ("\\", H.NE + H.EE),
            ("|", H.EE + 2*H.EE),
            ("|", 3*H.WW),
            ("\\", H.SW + H.WW),
            ("/", H.SE + 2*H.EE)
        ],
    }

# Makes a cool hex-y radial menu thing. Useless for now.
#        if self.style == "2hex":
#            for dir in dirs:
#                dir = (dir[0]*3, dir[1]*3)
#                for glyph, offset in Cursor.styles[self.style]:
#                    self.parent.offset_hd(add(self.pos, dir), offset, glyph, color)

    def __init__(self, coords, **kwargs):
        super(Cursor, self).__init__(**kwargs)
        self.coords = coords
        self.styles = ["[]", "1hex", "<>", "{}", "()"]

    def ready(self):
        self.selector = self.spawn(Selector())
        self.secondary = self.spawn(SecondarySelector(len(self.styles)-1))

    def process(self, command):
        if command("cancel"):
            self.parent.cursor = None
            self.suicide()
            command.done()
        elif command.name.startswith("move"):
            self.move(H.command_headings[command.name])
            command.done()

    # Move the cursor (hexagonally).
    def move(self, heading):
        self.coords += heading
        self.resize()

    def draw(self, display):
        coords = self.coords
        cell = self.level.get_map().cell(coords)
        color = "black-black"

        if cell is not None:
            if cell.actors:
                actor = cell.actors[self.selector.index]
                color = actor.cursor_color()
                # HACK: Magic number
                if self.zoom == 2:
                    coords += actor.subposition
            elif cell.terrain or cell.items:
                color = "yellow-black"
            else:
                color = "magenta-black"

        for glyph, offset in Cursor.styles[self.styles[self.secondary.index]]:
            display.hd(view, coords, glyph, color, offset=offset)

    # Resize based on features.
    def resize(self):
        cell = self.map.cell(self.coords)
        self.selector.resize(len(cell.actors)-1) if cell else self.selector.resize(0)

# Generic prompt.
class Prompt(View):
    """A Prompt is a View responsible for collecting input and sending it to a
    callback. They are typically blocking."""
    def __init__(self, **kwargs):
        super(Prompt, self).__init__(**kwargs)
        # TODO: fix prompt size.
#        View.__init__(self, window, x, y/2, start_x, start_y + y/4)
        self.input = None
        self.callback = kwargs.pop("callback", self.suicide)

    def draw(self, display):
        self.window.clear()
        self.border("/")

    def process(self, command):
        if command("confirm"):
            self.callback(self.input)
            self.suicide()
            command.done()
        elif command("cancel"):
            self.suicide()
            command.done()

class ListPrompt(Prompt):
    """A Prompt that provides a list of options to choose from."""
    def __init__(self, choices=[], initial=0, **kwargs):
        super(ListPrompt, self).__init__(**kwargs)
        self.input = self.spawn(Chooser(choices, initial))

    def draw(self, display):
        super(ListPrompt, self).draw(display)
        for choice in self.input.get_choices():
            if choice == self.input.get_choice():
                display.cline(self, text.highlight(choice))
            else:
                display.cline(self, choice)
        display.cline(self, "Choices: %s" % self.input.choices)
        display.cline(self, "Index: %s" % self.input.index)
        display.cline(self, "Max: %s" % self.input.max)
        display.cline(self, "Min: %s" % self.input.min)

class TextPrompt(Prompt):
    """A Prompt that provides a text entry form."""
    def __init__(self, **kwargs):
        super(TextPrompt, self).__init__(**kwargs)
        # TODO: fix prompt size
        # x, y/2, start_x, start_y + y/4
        self.input = ""
        self.max = 0

    def ready(self):
        self.scroller = self.spawn(SideScroller())

    def draw(self, display):
        Prompt.draw(self, display)
        # HACK: This is a guesstimate until I make the text functions more consistent.
        self.max = self.width * (self.height - 1)

        text = self.input[:self.scroller.index]
        if self.scroller.index < self.scroller.max:
            text += "<black-white>%s</>" % self.input[self.scroller.index]
        if len(self.input) > 1:
            text += self.input[self.scroller.index+1:]
        if self.scroller.index == self.scroller.max:
            text += "<black-white>_</>"
        display.cline(self, text)

    # TODO: Split this into a 'handle text entry' Trait
    def process(self, command):
        if command("confirm"): self.suicide()
        elif command("backspace"): self.backspace()
        elif command("delete"): self.delete()
        # TODO: Clumsy...
        elif command.key < 256: self.write(command.key)
        # Never let the command fall through, even if it didn't do anything.
        command.done()

    def write(self, c):
        if len(self.input) == self.max:
            return False
        left = self.input[:self.scroller.index]
        right = self.input[self.scroller.index:]
        self.input = left + chr(c) + right
        self.scroller.resize(len(self.input))
        self.scroller.index += 1

    def backspace(self):
        if self.scroller.index == 0:
            return False
        left = self.input[:self.scroller.index-1]
        right = self.input[self.scroller.index:]
        self.input = left + right

        self.scroller.resize(len(self.input))
        if self.scroller.index != self.scroller.max:
            self.scroller.index -= 1

    def delete(self):
        if self.scroller.index == self.scroller.max:
            return False

        left = self.input[:self.scroller.index]
        right = self.input[self.scroller.index+1:]
        self.input = left + right

        self.scroller.resize(len(self.input))

# TODO: Tree navigator.