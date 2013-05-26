"""A Map defines an area of game space in which the primary interactions are
quantized actions (most commonly, movement). It is the canonical representation
of a portion of the game's 'reality', and it is responsible for managing all
gameplay occurring within its scope.

Maps typically quantize time into a turn or energy system and quantize space
into Cells.

Maps can be of different scales. The most typical scales are:

    * Encounter: a 'combat map' with one Actor per Cell
    * Location: a 'site map' with one 'band' or 'patrol' of Actors per Cell
    * Region: a 'country map' with one Location per Cell
    * World: a 'zoomed out' world map with one Region per Cell
"""
from collections import deque

from src.lib.data import screens
from cell import BaseCell

from src.lib.util import debug
from src.lib.util.text import *
from src.lib.util.log import Log

class BaseMap(object):
    """An area of game space partitioned into Cells."""

    cell_class = BaseCell

    def __init__(self, level, map_id):
        # Maps don't make sense without an associated Level.
        # TODO: (not actually true, what about generating a ton of levels to compare?)
        self.level = level

        # Use the provided map ID (~depth).
        self.map_id = map_id

        # Display information.
        self.name = None

        # # Map generation parameters.
        # self.layout = None
        # self.size = None
        # self.center = None
        # self.passages = None
        # self.depth = None
        # self.entry = None # Player start point. TODO: Replace by bidirectional stairs!

        # Dict of (hex) cell objects, indexed by pos.
        self.cells = {}

        # # Default information if a cell doesn't exist.
        # # TODO: Expand!
        # self.floor = None

    def get_controller(self):
        """Return the Actor serving as primary controller in this Map."""
        return self.level.get_controller()

    """Map arrival methods."""

    # By default, before_arrive tries to load the matching screen and plugs in a
    # callback to self.arrive. Otherwise, it calls it itself.
    def before_arrive(self, entrance_id, exit_id):
        entryscreen = self.level.name
        if self.name is not None:
            entryscreen  += ", " + self.name # HACK: Later it should choose different dict for different levels.
        Log.add("You enter %s's %s." % (self.level.name, self.name))
        # if screens.text.get(striptags(entryscreen)) is not None:
        #     arguments = {"header_right" : entryscreen, "footer_text" : screens.footer, "callback" : self.arrive}
        #     self.screen(striptags(entryscreen), arguments)

    def arrive(self, entrance_id, exit_id):
        for passage_id, passage_obj in self.get_passages():
            self.get_controller().highlights[passage_id] = passage_obj

    def arriving_actor(self, actor, entrance_id, exit_id):
        passage = self.get_passage(entrance_id)
        assert self.put(actor, passage.pos) is not False

    """Map departure methods."""

    def before_depart(self, map_id, entrance_id, exit_id):
        """Do anything that needs to happen before leaving this Map."""
        pass

    def depart(self, map_id, entrance_id, exit_id):
        """Do anything that needs to happen as we actually leave this Map."""
        self.get_controller().highlights = {}

    def departing_actor(self, actor, map_id, entrance_id, exit_id):
        pass

    """Map passage methods."""

    def get_passage(self, passage_id):
        """Return a passage from a passage ID."""
        return self.layout.passages.get(passage_id)

    def get_passages(self):
        """Return an iterator over all passages."""
        return self.layout.passages.items()

    def add_cell(self, pos):
        """Create a Cell, store it within this map, and return it."""
        cell = self.cell_class(pos, self)
        self.cells[pos] = cell
        return cell

    # Return a cell at a pos tuple.
    def cell(self, pos):
        return self.cells.get(pos)

    # Return a list of actors at a pos tuple.
    def actors(self, pos):
        cell = self.cell(pos)
        if cell is None:
            return []
        else:
            return cell.actors

    # Return terrain at a pos tuple.
    def terrain(self, pos):
        cell = self.cell(pos)
        if cell is None:
            return None
        else:
            return cell.terrain

    # TODO: FIGURE OUT THIS SECTION, WHAT THE FUCK
    # TODO: It's still awful. I'm scared to touch it because so much relies on it.
    # Place an object (either agent or terrain) on the map.
    def put(self, obj, pos, terrain=False):

        cell = self.cells.get(pos)

        if not cell:
            return False

        if terrain is False:
            if cell.occupied():
                return False
            # Update the map
            cell.add(obj, terrain)

            # Update the actor
            obj.pos = pos
            obj.map = self
            obj.ready()

        else:
            if cell.get_terrain():
                return False
            # Update the map
            obj.cell = cell
            obj.pos = pos
            obj.map = self
            cell.add(obj, terrain)
        return obj

    def remove_actor(self, actor):
        """Remove an Actor from this Map."""
        actor.cell().remove(actor)
        # TODO: more of a callback approach
        self.level.remove_actor(actor)

    # Decides whether a position is a valid one.
    # TODO: Handle moving into nonexistent but cell-prototyped positions.
    def valid(self, pos):
        if self.cells.get(pos) is None:
            return False
        return True

    # TODO: Move to a file output util file.
    # # Print a large text version of the map.
    # def dump(self, size=100, origin=(0,0)):
    #     import sys
    #     print "Map of %s:\n" % self.name
    #     for y in range(-size, size):
    #         line = ""
    #         blank = True
    #         for x in range(-size, size):
    #             if x % 2 == 0:
    #                 line += " "
    #                 continue
    #             cell = self.cell(((x-y)/2,y))
    #             if cell is None:
    #                 glyph = " "
    #             else:
    #                 glyph = cell.glyph
    #                 blank = False
    #             line += glyph
    #         if blank is False:
    #             sys.stdout.write(line)
    #             sys.stdout.write("\n")
    #     exit()