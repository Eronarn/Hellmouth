"""Components are the minimal base user interface class. They participate in
keyin and draw loops, but do not have direct access to drawing methods."""

from src.lib.agents.contexts.context import Context

from src.lib.util import debug
from src.lib.util.trait import Traitable

class Component(object):
    """An interface Component taking part in UI control flow."""
    __metaclass__ = Traitable

    def __init__(self, **kwargs):
        self.alive = True
        self.children = []
        self.parent = None
        self.blocking = False

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return "<" + self.__str__() + ">"

    def get_controller(self):
        """Return the controller of this Component."""
        if self.parent:
            return self.parent.get_controller()

    """Child getter methods."""

    def get_parental_siblings(self, cls):
        if self.parent:
            for child in self.parent.get_children(cls):
                if child != self:
                    yield child

            for child in self.parent.get_parental_siblings(cls):
                yield child

    def get_first_parental_sibling(self, cls):
        for sibling in self.get_parental_siblings(cls):
            return sibling

    def get_ancestors(self):
        """Return a list of ancestors."""
        if self.parent:
            yield self.parent
            for ancestor in self.parent.get_ancestors():
                yield ancestor

    def get_descendents(self):
        """Return a nested (object, list) representation of all descendents."""
        descendents = [child.get_descendents() for child in self.children] if self.children else []
        return self, descendents

    def get_first_descendent(self, cls):
        for child in self.get_children(cls):
            return child
        for child in self.get_children():
            match = child.get_first_descendent(cls)
            if match is not None:
                return match

    def get_children(self, cls=None):
        """Yield all children matching a provided class."""
        for child in self.children:
            if cls and not isinstance(child, cls):
                continue
            yield child

    def get_first_child(self, cls=None):
        """Return the first child matching a provided class."""
        for child in self.get_children(cls):
            return child

    def has_child(self, cls=None):
        """Return whether this Component has a child (optionally, matching a provided class)."""
        if self.get_first_child(cls) is not None:
            return True
        return False

    """Child setter methods."""

    def spawn(self, child, index=False):
        """Spawn a child and return it."""
        # TODO: Deprecate this.
        if index is False:
            self.children.append(child)
        else:
            self.children.insert(index, child)
        child.parent = self
        child.ready()
        child.inherit()
        return child

    def add_blocking_component(self, component_class, **component_arguments):
        """Set a Component as blocking."""
        # TODO: Probably this should only go as high as Game, and not
        # RootComponent... it's plausible that you could have a blocking component
        # start a game-within-a-game, which would never be accessible, currently.
        if self.parent:
            self.parent.add_blocking_component(component_class, **component_arguments)
        else:
            blocker = self.spawn(component_class(**component_arguments))
            blocker.blocking = True

    def inherit(self):
        """Pass on values that need to be shared across components."""
        # TODO: Dependency injection?
        # TODO: Remove entirely?

        if self.parent:
            if hasattr(self.parent, 'window'):
                self.window = self.get_window(self.parent.window)
            for attr in ('kernel', 'map', 'level', 'zoom', 'layer'):
                if hasattr(self.parent, attr):
                    setattr(self, attr, getattr(self.parent, attr))

        for child in self.children:
            child.inherit()

    def ready(self):
        """Abstract. Perform actions that the child couldn't during init."""
        return True

    def suicide(self, *args, **kwargs):
        """Recursively kill this Component's children, and then itself."""
        for child in self.children:
            child.suicide()
        if self.parent is not None:
            self.parent.children.remove(self)
        self.alive = False

    def input(self, command):
        """Recurse through children trying their keyin functions until you've
        done your own."""
        debug.log("{} received command: {}.".format(self, command))
        for child in reversed(self.children):
            if child.input(command) is False or child.blocking is True:
                return False
        return self.process(command)

    def process(self, command):
        """Abstract. Handle commands."""
        return True

    def get_context(self, **kwargs):
        """Build a Context for this Component."""
        # TODO: Rename?
        context_class = kwargs.pop("context_class", Context)

        kwargs["agent"] = kwargs.get("agent", self.get_controller())
        kwargs["intent"] = kwargs.get("intent", {"attempt" : True})
        kwargs["component"] = kwargs.get("component", self)

        return context_class(**kwargs)

    def get_window(self, window):
        """Components pass along their parent's window. Views override this
        method and create subwindows."""
        return window