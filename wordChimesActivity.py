from gettext import gettext as _

import sys
import gtk
import pygame
import sugar.activity.activity
import sugar.graphics.toolbutton


sys.path.append('..') # Import sugargame package from top directory.
import sugargame.canvas
import wordChimes



_NEW_TOOLBAR_SUPPORT = True
try:
    from sugar.graphics.toolbarbox import ToolbarBox
except:
    _NEW_TOOLBAR_SUPPORT = False

class WordChimesActivity(sugar.activity.activity.Activity):
    def __init__(self, handle):
        super(WordChimesActivity, self).__init__(handle)
        self._canvas = sugargame.canvas.PygameCanvas(self)
        # Create the game instance.
        self.game = wordChimes.WordChimes()
        
        # Build the activity toolbar.
        if _NEW_TOOLBAR_SUPPORT:
            #self.create_new_toolbar()
            self.create_old_toolbar()
        else:
            self.create_old_toolbar()
   
        # Build the Pygame canvas.
        
        # Note that set_canvas implicitly calls read_file when resuming from the Journal.
        self.set_canvas(self._canvas)
        self._canvas.grab_focus()
        # Start the game running.
        self._canvas.run_pygame(self.game.run)
        
        #self.connect('visibility-notify-event', self._focus_event)
        self._canvas.connect('focus-in-event', self._focus_gain_event)
        self._canvas.connect('focus-out-event', self._focus_lose_event)
        self.connect('expose-event', self._expose_event)
        self.connect('key-press-event', self._key_press_event)
        #self.connect('_event', self._expose_event)
    def create_old_toolbar(self):        

        toolbar = gtk.Toolbar()
        
        toolbox = sugar.activity.activity.ActivityToolbox(self)
        #toolbox.add_toolbar(_("Word Chimes"), toolbar)
        
        toolbox.show_all()
        self.set_toolbox(toolbox)
        
    def create_new_toolbar(self):
        toolbar_box = ToolbarBox()
        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
    
    def _focus_gain_event(self,  event, data=None):
        self._canvas.caretOn = True
    def _focus_lose_event(self,  event, data=None):
        self._canvas.caretOn = False
    def _expose_event(self, event,  data=None):
        self._canvas.grab_focus()
        self.game.doPaint = True
    def _key_press_event(self, event,  data=None):
        self._canvas.grab_focus()

