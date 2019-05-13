import curses
from curses import panel

class Menu(object):

    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(0,0)
        self.window.keypad(True)

        # avoids flickering on refresh
        self.panel = panel.new_panel(self.window)
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(('exit','exit'))
        self.item_length = max([len(i[0]) for i in self.items]) + 11
        self.item_height = 5
        self.item_windows = [curses.newwin(self.item_height, self.item_length, self.item_height * i, 1) for i in range(len(items))]

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items)-1

    def display(self):
        self.window.clear()

        while True:
            self.window.refresh()

            # draw menu
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                # draw menu box
                msg = item[0]
                self.item_windows[index].box()
                self.item_windows[index].addstr(self.item_height // 2, (self.item_length - len(msg)) // 2, msg, mode)
                self.item_windows[index].refresh()

            # wait on input
            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.position == len(self.items)-1:
                    break
                else:
                    self.items[self.position][1]()

            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

class MyApp(object):

    def __init__(self, stdscreen):
        self.screen = stdscreen
        curses.curs_set(0)

        submenu_items = [
                ('beep', curses.beep),
                ('flash', curses.flash)
                ]
        submenu = Menu(submenu_items, self.screen)

        main_menu_items = [
                ('beep', curses.beep),
                ('flash', curses.flash),
                ('submenu', submenu.display)
                ]
        main_menu = Menu(main_menu_items, self.screen)
        main_menu.display()

if __name__ == '__main__':
    curses.wrapper(MyApp)
