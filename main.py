from src.lib.util import debug
from src.lib.util.define import *
from src.lib.util import system

debug.log("Completed all imports.")

# Import and initialize the Unicursal kernel.
from src.lib.core.kernel import kernel

debug.log("Kernel initialization complete.")

# Set a bitmask for game-wide display modes.
displayflags = {
    "silent" : 0b1,
    "curses" : 0b10,
    "unicode" : 0b100,
    "256" : 0b1000,
}

# Set up a dictionary of game settings.
# TODO: Have the kernel parse this.
arguments = {}

# Add a folder with default configurations.
arguments["configuration"] = 'src/lib/data/configuration'

# Default to displaying with curses
arguments["displaymode"] = displayflags["curses"]

# Default to launching Meat Arena
# TODO: If not provided, always get a game launcher
# arguments["gamemode"] = "debug"

# Default to not using a save
arguments["resume"] = False

# Provide a list of module folders
arguments["module_folders"] = ["src/games"]

# Import basic kernel services.
from src.lib.core.services.command import CommandService
from src.lib.core.services.component import ComponentService
from src.lib.core.services.config import ConfigService
from src.lib.core.services.loop import LoopService

# Import the relevant input and output services.
# TODO: Have the arguments and game decide this.
if arguments["displaymode"] == displayflags["curses"]:
    # Launch the game in curses mode
    from src.lib.core.output.curses.display import CursesDisplay as Display
    from src.lib.core.services.curses.input import CursesInputService as InputService
    from src.lib.core.services.curses.output import CursesOutputService as OutputService

# Initialize the display.
display = Display()

# Initialize kernel services.
kernel.loop = LoopService()
kernel.config = ConfigService(directory=arguments["configuration"])
kernel.input = InputService(display=display)
kernel.command = CommandService(commands=kernel.config.load('commands.yaml'))
kernel.output = OutputService(display=display)
kernel.component = ComponentService()

# Assign kernel services to the kernel loop.
kernel.loop[:] = [kernel.input, kernel.command, kernel.component, kernel.output]

# Launch the game, if the game mode was provided.
if arguments.get("gamemode"):
    kernel.component.launch((arguments.get("gamemode"), None))
# Launch a menu to select the game mode.
else:
    def get_choices():
        """Yield game choices."""
        for module_folder in arguments["module_folders"]:
            for module_package in sorted(system.folders(module_folder)):
                # TODO: Convert module folder into package name via sys directory separator.
                yield module_package, __import__('src.games.%s.info' % module_package, globals(), locals(), ['name', 'version', 'description'])

    # Create a game choice menu.
    from src.lib.components.views.screens.screen import MenuScreen
    choice_menu = MenuScreen(title="Start Game!", choices=list(get_choices()),
                            choice_formatter=lambda choice: choice[1].name,
                            callback=kernel.component.launch)

    # Spawn the game choice menu from the root component.
    kernel.component.spawn(choice_menu)

# Use the output service as a context manager.
with kernel.output:
    loops = 0
    # Start the kernel's loop service.
    while kernel.component.alive:
        loops += 1
        msg = "Loop: {}".format(loops)
        debug.log("\n{:=^80}".format(msg))
        kernel.loop.run()