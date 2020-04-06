import unicurses as curses
from curses import panel, wrapper
from curses.textpad import Textbox, rectangle
from client.menu import Menu
from client.data_manager import DataManager

TAB = 9

def show_search_screen(stdscr):
    curses.curs_set(1)
    stdscr.addstr(1, 2, 'Artist name: (Enter to search)')

    editwin = curses.newwin(1, 40, 3, 3)
    rectangle(stdscr, 2, 2, 4, 44)
    stdscr.refresh()

    box = Textbox(editwin)
    box.edit()

    criteria = box.gather()
    return criteria

def clear_screen(stdscr):
    stdscr.clear()
    stdscr.refresh()

def main(stdscr):
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    height, width = stdscr.getmaxyx()

    suffix_text = ' (TAB to search by artist)'
    albums_panel = Menu(
        'Album(s) for the selected artist' + suffix_text,
        (height, width, 0, 0)
    )

    tracks_panel = Menu(
        'Track(s) for the selected album' + suffix_text,
        (height, width, 0, 0)
    )

    criteria = show_search_screen(stdscr)
    _data_manager = DataManager()
    artist = _data_manager._search_artist(criteria)
    albums = _data_manager.get_artist_albums(artist['id'])
    
    clear_screen(stdscr)

    albums_panel.items = albums
    albums_panel.init()
    albums_panel.update()
    albums_panel.show()

    current_panel = albums_panel
    is_running = True

    while is_running:
        curses.doupdate()
        current_panel.update()

        key = stdscr.getch()
        action = current_panel.handle_events(key)

        if action is not None:
            action_result = action()
            if current_panel == albums_panel and action_result is not None:
                _id, uri = action_result
                tracks = _data_manager.get_album_tracklist(_id)
                current_panel.hide()
                current_panel = tracks_panel
                current_panel.items = tracks
                current_panel.init()
                current_panel.show()
            elif current_panel == tracks_panel and action_result is not None:
                _id, uri = action_result
                _data_manager.play(uri)

        if key == TAB:
            current_panel.hide()
            criteria = show_search_screen(stdscr)
            artist = _data_manager._search_artist(criteria)
            albums = _data_manager.get_artist_albums(artist['id'])

            clear_screen(stdscr)
            current_panel = albums_panel
            current_panel.items = albums
            current_panel.init()
            current_panel.show()

        if key == ord('q') or key == ord('Q'):
            is_running = False
        
        current_panel.update()

try:
    wrapper(main)
except KeyboardInterrupt:
    print('Exiting...')