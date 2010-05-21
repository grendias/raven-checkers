from Tkinter import *
import Tkinter as tk
from multiprocessing import freeze_support
from globalconst import *
from aboutbox import AboutBox
from setupboard import SetupBoard
from gamemanager import GameManager
from centeredwindow import CenteredWindow

class MainFrame(object, CenteredWindow):
    def __init__(self, master):
        self.root = master
        self.root.withdraw()
        self.root.wm_iconbitmap('_raven.ico')
        self.root.title("Raven "+VERSION)
        self.frame = Frame(self.root)
        self.frame.pack(fill=X)
        self.thinkTime = IntVar(value=5)
        self.manager = GameManager(root=self.root, parent=self)
        gameMenu = self.create_game_menu()
        movesMenu = self.create_moves_menu()
        optionsMenu = self.create_options_menu()
        helpMenu = self.create_help_menu()
        self.frame.tk_menuBar(gameMenu, helpMenu)
        CenteredWindow.__init__(self, self.root)
        self.root.minsize(self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        self.root.maxsize(self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        self._bind_events()
        self.root.deiconify()
        
    def _bind_events(self):
        # TODO: Move these events to PlayerController?
        self.root.bind('<Home>', self._undo_all_moves)
        self.root.bind('<End>', self._redo_all_moves)
        self.root.bind('<Left>', self._undo_single_move)
        self.root.bind('<Right>', self._redo_single_move)

    def _undo_all_moves(self, *args):
        #self.manager._controller1.stop_process()
        #self.manager._controller2.stop_process()
        self.manager.model.undo_all_moves()
        self.manager._controller1.remove_highlights()
        self.manager._controller2.remove_highlights()
        self.manager.view.update_statusbar()

    def _redo_all_moves(self, *args):
        #self.manager._controller1.stop_process()
        #self.manager._controller2.stop_process()
        self.manager.model.redo_all_moves()
        self.manager._controller1.remove_highlights()
        self.manager._controller2.remove_highlights()
        self.manager.view.update_statusbar()

    def _undo_single_move(self, *args):
        #self.manager._controller1.stop_process()
        #self.manager._controller2.stop_process()
        self.manager.model.undo_move()
        self.manager._controller1.remove_highlights()
        self.manager._controller2.remove_highlights()
        self.manager.view.update_statusbar()

    def _redo_single_move(self, *args):
        #self.manager._controller1.stop_process()
        #self.manager._controller2.stop_process()
        self.manager.model.redo_move()
        self.manager._controller1.remove_highlights()
        self.manager._controller2.remove_highlights()
        self.manager.view.update_statusbar()

    def create_game_menu(self):
        gameBtn = Menubutton(self.frame, text='Game', underline=0)
        gameBtn.pack(side=LEFT)
        gameBtn.menu = Menu(gameBtn, tearoff=0)
        gameBtn.menu.add_command(label='New game', underline=0,
                                 command=self.manager.new_game)
        gameBtn.menu.add_command(label='Load game', underline=0,
                                 command=self.manager.load_game)
        gameBtn.menu.add_separator()
        gameBtn.menu.add_command(label='Set up board ...', underline=0,
                                 command=self.show_setup_board_dialog)
        gameBtn.menu.add_command(label='Flip board', underline=0,
                                 command=self.flip_board)
        gameBtn.menu.add_separator()
        gameBtn.menu.add_command(label='Exit', underline=0, command=gameBtn.quit)
        gameBtn['menu'] = gameBtn.menu
        return gameBtn

    def create_moves_menu(self):
        movesBtn = Menubutton(self.frame, text='Moves', underline=0)
        movesBtn.pack(side=LEFT)
        movesBtn.menu = Menu(movesBtn, tearoff=0)
        movesBtn.menu.add_command(label='Undo one move',
                                  command=self._undo_single_move,
                                  accelerator='<-')
        movesBtn.menu.add_command(label='Redo one move',
                                  command=self._redo_single_move,
                                  accelerator='->')
        movesBtn.menu.add_command(label='Undo all moves',
                                  command=self._undo_all_moves,
                                  accelerator='Home')
        movesBtn.menu.add_command(label='Redo all moves',
                                  command=self._redo_all_moves,
                                  accelerator='End')

        movesBtn['menu'] = movesBtn.menu
        return movesBtn

    def create_options_menu(self):
        optBtn = Menubutton(self.frame, text='Options', underline=0)
        optBtn.pack(side=LEFT)
        optBtn.menu = Menu(optBtn, tearoff=0)
        thinkMenu = Menu(optBtn.menu, tearoff=0)
        thinkMenu.add_radiobutton(label="1 second", underline=None,
                                  command=self.set_think_time,
                                  variable=self.thinkTime,
                                  value=1)
        thinkMenu.add_radiobutton(label="2 seconds", underline=None,
                                  command=self.set_think_time,
                                  variable=self.thinkTime,
                                  value=2)
        thinkMenu.add_radiobutton(label="5 seconds", underline=None,
                                  command=self.set_think_time,
                                  variable=self.thinkTime,
                                  value=5)
        thinkMenu.add_radiobutton(label="10 seconds", underline=None,
                                  command=self.set_think_time,
                                  variable=self.thinkTime,
                                  value=10)
        thinkMenu.add_radiobutton(label="30 seconds", underline=None,
                                  command=self.set_think_time,
                                  variable=self.thinkTime,
                                  value=30)
        thinkMenu.add_radiobutton(label="1 minute", underline=None,
                                  command=self.set_think_time,
                                  variable=self.thinkTime,
                                  value=60)
        optBtn.menu.add_cascade(label='CPU think time', underline=0,
                                menu=thinkMenu)
        optBtn['menu'] = optBtn.menu
        return optBtn

    def create_help_menu(self):
        helpBtn = Menubutton(self.frame, text='Help', underline=0)
        helpBtn.pack(side=LEFT)
        helpBtn.menu = Menu(helpBtn, tearoff=0)
        helpBtn.menu.add_command(label='About Raven ...', underline=0,
                                 command=self.show_about_box)
        helpBtn['menu'] = helpBtn.menu
        return helpBtn

    def show_about_box(self):
        AboutBox(self)

    def show_setup_board_dialog(self):
        # stop alphabeta thread from making any moves
        self.manager.model.curr_state.ok_to_move = False
        self.manager._controller1.stop_process()
        self.manager._controller2.stop_process()
        SetupBoard(self, self.manager)

    def set_think_time(self):
        self.manager._controller1.set_search_time(self.thinkTime.get())
        self.manager._controller2.set_search_time(self.thinkTime.get())

    def flip_board(self):
        if self.manager.model.to_move == BLACK:
            self.manager._controller1.remove_highlights()
        else:
            self.manager._controller2.remove_highlights()
        self.manager.view.flip_board(not self.manager.view.flip_view)
        if self.manager.model.to_move == BLACK:
            self.manager._controller1.add_highlights()
        else:
            self.manager._controller2.add_highlights()

def start():
    root = Tk()
    mainframe = MainFrame(root)
    mainframe.root.update()
    mainframe.root.mainloop()

if __name__=='__main__':
    freeze_support()
    start()
