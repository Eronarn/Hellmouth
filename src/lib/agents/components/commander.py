from src.lib.agents.components.action import Action
from src.lib.agents.components.component import Component
from src.lib.agents.components.phase import Phase
from src.lib.agents.contexts.context import action_context, command_context
from src.lib.agents.components.faction import NeutralFaction

from src.lib.util.command import Command, CommandRegistry as CMD
from src.lib.util import debug
from src.lib.util.log import Log
from src.lib.util.trait import Trait

"""Actions."""

class TakeMentalCommand(Action):
    """Take telepathic command of a target."""
    @action_context
    def get_phases(self, ctx):
        yield Phase("take_command", "target")

class IssueMentalCommand(Action):
    """Issue a telepathic command to a target."""
    @action_context
    def get_phases(self, ctx):
        yield Phase("issue_command", "target", "command")

"""Commands."""

class TakeCommand(Command):
    """Take command of a target."""
    description = "take command of a target"
    defaults = ("t",)

    @command_context
    def get_actions(self, ctx):
        yield TakeMentalCommand

class IssueCommand(Command):
    """Issue a command to a target."""
    description = "issue a command to a target"
    defaults = ("C",)

    @command_context
    def get_actions(self, ctx):
        yield IssueMentalCommand

CMD.register(TakeCommand, IssueCommand)

"""Components."""

class Commander(Component):
    """Component that handles an Agent's command capabilities."""

    commands = []
    domain = "Command"

    def __init__(self, owner, commanded=[]):
        super(Commander, self).__init__(owner)

        self.commanded = commanded

    def get_commands(self, context):
        """Yield the Commands this Component makes available to its Agent
        within a Context.
        """
        if "Command" in context.get_domains():
            if "Combat" in context.get_domains() and self.has_commanded():
                yield CMD("IssueCommand", command="attack")

            for participant in context.get_participants():
                if self.can_command(participant):
                    yield CMD("IssueCommand", target=participant)
                elif self.can_commanded(participant):
                    yield CMD("TakeCommand", target=participant)

    """Commanded getter functions."""

    def get_commanded(self):
        for commanded in self.commanded:
            yield commanded

    """Commanded setter functions."""

    # TODO: Triggers

    def add_commanded(self, agent):
        """Command an Agent."""
        agent.append_component(Commanded(owner=agent, controller=self.owner))
        agent.append_component(CommandedFaction(owner=agent, controller=self.owner))
        self.commanded.append(agent)
        return True

    def remove_commanded(self, agent):
        """Uncommand an Agent."""
        self.grasped.remove(agent)
        # TODO: 7drl
        for component in agent.get_controlled_components(self.owner, "Commanded"):
            agent.remove_component(component)
        for component in agent.get_controlled_components(self.owner, "Faction"):
            agent.remove_component(component)
        return True

    """Commanded helper methods."""

    def can_commanded(self, agent):
        """Return whether an Agent can be set as commanded."""
        if agent.has_domain("Commanded"):
            return False
        return True

    def has_commanded(self):
        """Return whether this Component is commanding any Agents."""
        for agent in self.get_commanded():
            return True
        return False

    def is_commanded(self, agent):
        """Return whether this Component's Agent is commanding another Agent."""
        for component in agent.get_controlled_components(self.owner, "Commanded"):
            return True
        return False

    """Command helper methods."""

    def can_command(self, agent):
        """Return whether this Component's Agent can issue commands to another Agent."""
        if self.is_commanded(agent):
            return True
        return False

class Commanded(Component):
    """Component that handles a commanded Agent's functionality."""
    def __init__(self, owner, controller):
        super(Commanded, self).__init__(owner)

        self.controller = controller

class CommandedFaction(NeutralFaction):
    """Commanded faction."""
    def get_target(self):
        """default to player"""
        return self.get_faction()

"""Traits."""
class Leading(Trait):
    """Provides methods to lead followers."""

    def could_take_command(self):
        """Whether the Agent could take command of an unspecified target."""
        return True

    def can_take_command(self, target):
        """Whether the Agent can take command of a target."""
        return True

    def do_take_command(self, target):
        """Take command of a target."""
        if self.call("Command", "add_commanded", target).get_result():
            Log.add("%s takes command of %s!" % (self.appearance(), target.appearance()))
            return True
        return False

class Ordering(Trait):
    """Provides methods to order followers."""

    def could_issue_command(self):
        """Whether the Agent could issue a command to an unspecified target."""
        return True

    def can_issue_command(self, target, command):
        """Whether the Agent can issue a command to a target."""
        return True

    def do_issue_command(self, target, command):
        """Issue a command to a target."""
        return True

CommandingTraits = {Leading, Ordering}