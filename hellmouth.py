def main(stdscr):

    # HACK: Define termsize rather than figuring it out.
    term_x = 80
    term_y = 24

    # Make the cursor invisible.
    curses.curs_set(0)
    # Use raw input.
    curses.raw()

    # Handle game-related imports.
    import random
    import dice 
    import hex
    from describe import Descriptions
    from define import NW, NE, CE, SE, SW, CW
    from actor import Actor
    from player import *
    from map import Map, Terrain
    from view import MainMap, Stats, Chargen, Status, Log, View
    from key import keyin

    # HACK: Display an intro screen.
    intro = View(stdscr, term_x, term_y, 0, 0)
    intro.x_acc = 10
    intro.line("")
    intro.line('7DRL 2012 ENTRY "HELLMOUTH" HAS BEEN TURNED INTO MEAT')
    intro.line('BASED ROGUELIKE "MEAT ARENA", WITH FABULOUS FEATURES:')
    intro.line("")
    intro.line("  * A MEAT ARENA")
    intro.line("")
    intro.line("  * HEXAGONS")
    intro.line("")
    intro.line("  * A MEAT PLAYER")
    intro.line("")
    intro.line("  * SIX DIRECTIONS OF MOVEMENT.")
    intro.line("")
    intro.line("  * HEXAGONS")
    intro.line("")
    intro.line("  * UP TO FOUR KINDS OF MEAT ENEMIES")
    intro.line("")
    intro.line("  * HEXAGONS")
    intro.line("")
    intro.line("  * A MEAT ARENA")
    intro.line("")
    intro.line("")
    intro.line("PRESS SPACE TO ENTER THE MEAT ARENA")
    intro.line("")
    intro.line("PRESS ESC TO COWARDLY LEAVE")
    # Wait for player input.
    while 1:
        c = stdscr.getch()
        if c == ord(' '):
            break;
        if c == 27:
            exit("COWARD.")

    # Very basic map init - 50x50.
    map = Map()
    map.loadmap(50, 50)

    # Define the map center.
    center_x = map.width/2 - 1
    center_y = map.height/2 - 1

    # Mega hack to draw a hexagonal map: draw a hex from hex_start to hex_max.
    hex_max = 25
    hex_start = 15

    # Arena walls
    walls = hex.iterator(map, center_x, center_y, hex_max, True, True, False, hex_start)
    for pos in walls:
        terrain = map.put(Terrain(), pos, True)

    # Randomly placed columns
    colnum = 10
    for x in range(colnum):
        colsize = random.randint(1, 3)
        pos = (center_x + dice.flip()*random.randint(4, hex_start)-colsize, center_y + dice.flip() * random.randint(4,hex_start)-colsize)
        col = hex.iterator(map, pos[0], pos[1], colsize, True, True, False, 0)
        for loc in col:
            map.put(Terrain(), loc, True)       

    # Place our friendly @
    player = map.put(Player(), (center_x, center_y))
    map.player = player

    # Define monsters to be placed
    monsters = [MeatSlave, MeatSlave, MeatSlave, MeatSlave, MeatWorm, MeatWorm, MeatGolem, MeatHydra] 

    # Place monsters
    num_mons = 100
    for x in range(num_mons):
        monster = random.choice(monsters)
        map.put(monster(), (center_x + dice.flip()*random.randint(1, hex_start), center_y + dice.flip() * random.randint(1,hex_start)))

    # HACK:
    mainmap_width = 45

    # Map screen init
    mainmap = MainMap(stdscr, mainmap_width, term_y, 0, 0)
    mainmap.map = map
    mainmap.player = player
    # Just a hook. Does nothing now.
    mainmap.ready()

    # Status window init
    status_size = 5
    status = Status(stdscr, 80-mainmap_width-status_size, status_size, mainmap_width-status_size, 0)

    # Chargen window init
    chargen = Chargen(stdscr, term_x, term_y, 0, 0)

    # Stats window init
    # HACK:
    spacing = 2
    stat_height = 11
    stats = Stats(stdscr, 80-mainmap_width-spacing, stat_height, mainmap_width+spacing, 0)
    stats.player = player

    # Log window init
    log = Log(stdscr, 80-mainmap_width-status_size, term_y-stat_height, mainmap_width+spacing, stat_height)
    map.log = log
    map.log.add("WELCOME TO THE ARENA OF MEAT")

    # DEBUG: Generate log entries
    #for x in range(50):
    #    map.log.add("Log Entry %s" % x)

    # Initialize views and append the current windows.
    views = []
    # TODO: Move these into a function.
    views.append(chargen)
    views.append(stats)
    views.append(log)
    # TODO: Make status a child of mainmap.
    views.append(status)
    views.append(mainmap)

    gameplay = False

    # Main game loop
    while 1:

        # Chargen, between-map screens, etc.
        while gameplay is False:
            # TODO: Turn this into a function since it's used elsewhere.
            # Before the player's turn, clear the screen and tell views to redraw themselves.
            stdscr.clear()
            for view in views:
                if view.draw() is False:
                    break

            # Handle all player keyboard input
            if keyin(stdscr, views) is True:
            # HACK PART 2: Done with chargen.
                gameplay = True

        # If nobody is acting, let the first in the queue act.
        if map.acting is None:
            map.acting = map.queue.popleft()

            # End the game if there is nobody else left to act, or if the player is dead.
            if len(map.queue) == 0:
                break;
            if player.hp <= 0:
                break;

        # DEBUG: Print currently acting actor name.
        # Has to be here for it to work properly.
        #stdscr.addstr(19, 59, "QUEUE")
        #if map.acting is not None:
        #    stdscr.addstr(20, 59, "Curr: %s" % map.acting.name)
        #else:
        #    stdscr.addstr(20, 59, "Curr: NONE")
        #stdscr.addstr(21, 59, "Next: %s" % map.queue[0].name)

        # NPCs act until the player's turn comes up.
        if map.acting is not player:
            map.acting.act()
            continue
    
        # Before the player's turn, clear the screen and tell views to redraw themselves.
        stdscr.clear()
        for view in views:
            if view.draw() is False:
                break

        # Handle all player keyboard input
        keyin(stdscr, views)

        # All non-component (i.e., debug) drawing is handled below.

        # DEBUG: Print current position.
        #stdscr.addstr(10, 59, "POSITION", curses.color_pair(1))
        #stdscr.addstr(11, 59, '(%s, %s)' % player.pos, curses.A_REVERSE)

        # DEBUG: Print distance from starting point.
        #stdscr.addstr(13, 59, "DIST FROM (%s, %s)" % (center_x, center_y))
        #stdscr.addstr(14, 59, "[%d]" % hex.dist(player.pos[0], player.pos[1], center_x, center_y))

        # DEBUG: Print current key.
        #stdscr.addstr(16, 59, "KEYIN")
        #if c < 256 and c > 31: # i.e., ASCII glyphs
        #    stdscr.addch(17, 59, chr(c))

        # DEBUG: Print current torso wounds.
        #stdscr.addstr(16, 59, "TORSO WOUNDS")
        #stdscr.addstr(17, 59, "%s" % player.body.locs.get("Torso").wounds)

        # Refresh the display.
        stdscr.refresh()

    # HACK: If we get here, we're displaying the win screen.
    stdscr.clear()

    intro = View(stdscr, term_x, term_y, 0, 0)
    intro.x_acc = 10
    intro.line("")
    if player.hp > 0:
        intro.line('YOU HAVE CONQUERED THE MEAT BASED ROGUELIKE "MEAT ARENA"')
        intro.line("")
        intro.line("YOU ARE HUNGRY AFTER YOUR BATTLE AND MANAGE TO EAT YOUR WAY OUT")
        intro.line("")
        intro.line("CONGRATULATIONS!")
    else:
        intro.line('YOU HAVE BEEN SLAIN IN THE MEAT BASED ROGUELIKE "MEAT ARENA"')
        intro.line("")
        intro.line("YOU ARE USED TO FURTHER FORTIFY ITS MEAT WALLS!")
        intro.line("")
        intro.line("CONGRATULATIONS!")
    intro.line("")
    intro.line("")
    intro.line("")
    intro.line("THANKS FOR PLAYING AND MAKE SURE TO FOLLOW HELLMOUTH ON GITHUB:")
    intro.line("")
    intro.line("        https://github.com/Eronarn/Hellmouth")
    intro.line("")
    intro.line("THE REAL GAME WILL BE MUCH BETTER, I PROMISE")
    intro.line("")
    intro.line("")
    intro.line("")
    intro.line("HUGS & KISSES,")
    intro.line("")
    intro.line("    -ERONARN")
    intro.line("")
    intro.line("")
    if player.hp > 0:
        intro.line("PRESS SPACE OR ESC TO EXIT THE ARENA IN TRIUMPH")
    else:
        intro.line("PRESS SPACE OR ESC TO EXIT THE ARENA IN IGNOMINY")

    # Wait for the player to quit.
    while 1:
        c = stdscr.getch()
        if c == ord(' ') or c == 27:
            exit("THANKS FOR PLAYING!")

# Curses import.
import curses

# Initialize the curses wrapper, which calls the main function after setting up curses.
curses.wrapper(main)
