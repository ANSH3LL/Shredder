import sys
import ttk
import ctypes
from Tkinter import *
from TkinterDnD2 import TkinterDnD

class AL3(Tk):
    def __init__(self, **kwargs):
        Tk.__init__(self)
        #General routines
        self.overrideredirect(True)
        #Values for window iconification
        self.GWL_EXSTYLE = -20
        self.WS_EX_APPWINDOW = 0x00040000
        self.WS_EX_TOOLWINDOW = 0x00000080
        self._visibility = 0
        #Icon holder
        self._iconpath = 'Ai.ico'
        #Title holder
        self._Th = kwargs['title'] if kwargs.get('title') else 'AL3'
        #Values for colours
        self._clscolor = kwargs['clscolor'] if kwargs.get('clscolor') else 'red'
        self._mincolor = kwargs['mincolor'] if kwargs.get('mincolor') else 'cyan'
        self.wmcolor = kwargs['wmcolor'] if kwargs.get('wmcolor') else '#3A6FFF'
        self.wmcolor2 = kwargs['wmcolor2'] if kwargs.get('wmcolor2') else 'black'
        self.wincolor = kwargs['wincolor'] if kwargs.get('wincolor') else 'black'
        #Values for window geometry
        self._width = 200
        self._height = 200
        self._xpos = 0
        self._ypos = 0
        #Offsets for window movement
        self._offsetx = 0
        self._offsety = 0
        #Window manager frame
        self.wmframe = Frame(self, bg = self.wmcolor)
        self.wmframe.pack(side = 'top', fill = X)
        self.wmframe.bind('<1>', self.__clickwin)
        self.wmframe.bind('<B1-Motion>', self.__dragwin)
        self.wmframe.bind("<Map>", self.__wmframe_mapped)
        #Window manager window frame
        self.winframe = Frame(self, bg = self.wincolor)
        self.winframe.pack(side = 'top', fill = BOTH, expand = True)
        #Window title
        self.Title = Label(self.wmframe, bg = self.wmcolor, fg = self.wmcolor2, text = self._Th, font = 'Arial 15')
        self.Title.pack(side = 'left')
        self.Title.bind('<1>', self.__clickwin)
        self.Title.bind('<B1-Motion>', self.__dragwin)
        #Window manager 'buttons'
        #Close
        self.close = Label(self.wmframe, bg = self.wmcolor, fg = self.wmcolor2, text = chr(215), anchor = 'center', font = 'Helvetica 20', width = 2)
        self.close.pack(side = 'right')
        self.close.bind('<1>', self.__cleanexit)
        self.close.bind('<Enter>', self.__clshover)
        self.close.bind('<Leave>', self.__clsunhover)
        #Minimise
        self.minimise = Label(self.wmframe, bg = self.wmcolor, fg = self.wmcolor2, text = u'\U00002013', anchor = 'center', font = 'Helvetica 20', width = 2)
        self.minimise.pack(side = 'right')
        self.minimise.bind('<1>', self.__minify)
        self.minimise.bind('<Enter>', self.__minhover)
        self.minimise.bind('<Leave>', self.__minunhover)

    def set_geometry(self, width, height, xpos, ypos):
        self._width = width
        self._height = height
        self._xpos = xpos
        self._ypos = ypos
        self.geometry('%dx%d+%d+%d' %(width, height, xpos, ypos))

    def set_icon(self, iconpath):
        self._iconpath = iconpath

    def __dragwin(self,event):
        x = self.winfo_pointerx() - self._offsetx
        y = self.winfo_pointery() - self._offsety
        self.geometry('+{x}+{y}'.format(x = x,y = y))
        self._xpos = x
        self._ypos = y

    def __clickwin(self, event):
        self._offsetx = event.x
        self._offsety = event.y
        
    def __clshover(self, event):
        event.widget.config(bg = self._clscolor)

    def __clsunhover(self, event):
        event.widget.config(bg = self.wmcolor)

    def __minhover(self, event):
        event.widget.config(bg = self._mincolor)

    def __minunhover(self, event):
        event.widget.config(bg = self.wmcolor)

    def __cleanexit(self, event):
        self.destroy()
        sys.exit()

    def __minify(self, event):
        self.update_idletasks()
        self.state('withdrawn')
        self.overrideredirect(False)
        self.title(self._Th)
        self.iconbitmap(self._iconpath)
        self.state('iconic')
        self._visibility = 0

    def __wmframe_mapped(self, event):
        #print(self, event)
        self.update_idletasks()
        self.overrideredirect(True)
        self.state('normal')
        if self._visibility == 0:
            self._setx()
        else:
            pass

    def __setvisiblex(self):
        #Set our native icon & title
        self.wm_title(self._Th)
        self.wm_iconbitmap(self._iconpath)
        #Force iconification
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        res = ctypes.windll.user32.SetWindowLongW(hwnd, self.GWL_EXSTYLE, style)
        self.wm_withdraw()
        self.after(1, lambda: self.wm_deiconify())
        self._visibility = 1

    def _setx(self):
        self.after(1, lambda: self.__setvisiblex())

class DropFrame(Label):
    '''Just an ordinary label with superlabel capabilities.\nRequires TkDnD2.8'''
    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)
        #Do not touch...
        self.tk.call('package', 'require', 'tkdnd')
        self.tk.call('tkdnd::drop_target', 'register', self._w, 'DND_Files')

    def _dnd_bind(self, what, sequence, func, add, needcleanup = True):
        """Do not modify me. I was copied directly from unknown territory."""
        if isinstance(func, str):
            self.tk.call(what + (sequence, func))
        elif func:
            funcid = self._register(func, self._substitute_dnd, needcleanup)
            cmd = '%s%s %s' %(add and '+' or '', funcid, self._subst_format_str_dnd)
            self.tk.call(what + (sequence, cmd))
            return funcid
        elif sequence:
            return self.tk.call(what + (sequence,))
        else:
            return self.tk.splitlist(self.tk.call(what))

    def dnd_bind(self, sequence=None, func=None, add=None):
        """Do not modify me. I was copied directly from unknown territory."""
        return self._dnd_bind(('bind', self), sequence, func, add)
