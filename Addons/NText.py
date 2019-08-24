import ttk
import lncnv
from Tkinter import Text, Frame

class NumberedText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)
        self.config(wrap = 'none')
        #Scrollbar
        self.yscrollframe = Frame(self.master)
        self.yscroll = ttk.Scrollbar(self.yscrollframe, orient = 'vertical', cursor = 'arrow', command = self.yview)
        self.config(yscrollcommand = self.yscroll.set)
        self.yscrollframe.pack(side = 'right', fill = 'y')
        self.yscroll.pack(expand = True, fill = 'y')

        #Line Numbers
        self.lnframe = Frame(self.master)
        self.linenotify = lncnv.LineCanvas(self.lnframe)
        self.linenotify.subscribe(self)
        self.lnframe.pack(side = 'left', fill = 'y')
        self.linenotify.pack(expand = True, fill = 'y')
        self.add_intercept()
        self.bind('<Configure>', self.linenotify.update)
        self.bind('<<Changed>>', self.linenotify.update)
        self.bind('<KeyRelease>', self.linenotify.update)

    def add_intercept(self):
        self.tk.eval('''
            proc widget_interceptor {widget command args} {

                set orig_call [uplevel [linsert $args 0 $command]]

              if {
                    ([lindex $args 0] == "insert") ||
                    ([lindex $args 0] == "delete") ||
                    ([lindex $args 0] == "replace") ||
                    ([lrange $args 0 2] == {mark set insert}) || 
                    ([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {

                    event generate  $widget <<Changed>>
                }

                #return original command
                return $orig_call
            }
            ''')
        self.tk.eval('''
            rename {widget} new
            interp alias {{}} ::{widget} {{}} widget_interceptor {widget} new
        '''.format(widget = str(self)))
