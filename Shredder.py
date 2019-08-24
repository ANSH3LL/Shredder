import os
import threading
import tkFileDialog
from Addons import *
from Tkinter import *
from Abstraktion import *
from Lib import ShredderCore

shdescription = '''
Drop files or folders here to add them to the shred list.
When ready, click the button to shred files in the shred list.
To remove an entry from the shred list, highlight the line and press delete.'''

default_bg = 'black'
default_fg = '#bdbdbd'

def hover(event):
    event.widget.config(bg = 'grey50', fg = '#2196F3')

def unhover(event):
    event.widget.config(bg = 'grey35', fg = '#3A6FFF')

def dropped(event):
    xt = event.widget.tk.splitlist(event.data)
    for x in xt:
        shlistbox.insert('insert', '%s\n'%(x))

def browse(event):
    if addbox.get():
        shlistbox.insert('insert', '%s\n'%(addbox.get()))
    else:
        ftuple = tkFileDialog.askopenfilenames()
        for entry in ftuple:
            shlistbox.insert('insert', '%s\n'%(entry))

def shproxy(event):
    sht = threading.Thread(target = shred)
    sht.start()

def shred():
    currentcount.config(text = '0')
    ftp = []
    x = ShredderCore.FileShredder(currentcount)
    flist = shlistbox.get('1.0', 'end')
    if len(flist) > 1:
        for binding in ['<1>', '<Enter>', '<Leave>']:#Disable buttons
            addbtn.unbind(binding)
            actionbtn.unbind(binding)
        actionbtn.config(bg = 'grey35', fg = '#3A6FFF')
        currentstate.config(text = 'Shredding...')
        ftp = flist.split('\n')
        ftp.pop()
        ftp.pop()
        for ex in ftp:
            if os.path.isdir(ex):
                x.shred_multiple(ex, pfvar.get())
            else:
                x.shred_single(ex)
        currentstate.config(text = 'Idle...')
        shlistbox.delete('1.0', 'end')
        for bindings in [('<1>', browse), ('<Enter>', hover), ('<Leave>', unhover)]:#Enable buttons
            addbtn.bind(bindings[0], bindings[1])
        for bindings in [('<1>', shproxy), ('<Enter>', hover), ('<Leave>', unhover)]:#Enable buttons
            actionbtn.bind(bindings[0], bindings[1])
    else:
        pass
            
shwin = AL3(title = 'Shredder', wmcolor = default_bg, wmcolor2 = 'white', wincolor = default_bg)
shwin.attributes('-alpha', 0.9)
shwin.set_geometry(800, 500, 300, 150)
shwin.set_icon('Shredder.ico')

#Section 0.5
pfvar = IntVar()

#Section 1
desc_frame = Frame(shwin.winframe, bg = default_bg)
description = DropFrame(desc_frame, bg = default_bg, fg = default_fg, text = shdescription, font = 'Consolas 12', pady = 0, justify = 'left')

sh_lblframe = LabelFrame(shwin.winframe, bg = default_bg, fg = default_fg, text = 'Shred List', font = 'Consolas', pady = 10)
shlist_frame = Frame(sh_lblframe, bg = default_bg)
shlist_frame2 = Frame(shlist_frame)
shlistbox = NumberedText(shlist_frame2, bg = 'grey', font = 'Consolas 12', height = 4, insertbackground = 'grey')

pad = Label(shlist_frame, bg = default_bg, pady = 5)
addlabel = Label(shlist_frame, bg = default_bg, fg = default_fg, text = 'Add to shred list', font = 'Consolas 12')
addbox = Entry(shlist_frame, bg = 'grey', font = 'Consolas 12', width = 59, relief = 'flat')
addbtn = Label(shlist_frame, bg = 'grey35', fg = '#3A6FFF', text = 'Add/Browse', font = 'Consolas 12 bold')#Button

op_lblframe = LabelFrame(shwin.winframe, bg = default_bg, fg = default_fg, text = 'Options', font = 'Consolas', pady = 15)
option_frame = Frame(op_lblframe, bg = default_bg)
pflabel = Label(option_frame, bg = default_bg, fg = default_fg, text = 'Preserve folders', font = 'Consolas 12')
pfchbtn = Checkbutton(option_frame, variable = pfvar, bg = default_bg, activebackground = default_bg)

st_lblframe = LabelFrame(shwin.winframe, bg = default_bg, fg = default_fg, text = 'Status', font = 'Consolas', pady = 10)
status_frame = Frame(st_lblframe, bg = default_bg)
statelabel = Label(status_frame, bg = default_bg, fg = default_fg, text = 'Status', font = 'Consolas 12')
currentstate = Label(status_frame, bg = default_bg, fg = default_fg, text = 'Idle...', font = 'Consolas 12 bold')

countlabel = Label(status_frame, bg = default_bg, fg = default_fg, text = 'Files Shredded', font = 'Consolas 12')
currentcount = Label(status_frame, bg = default_bg, fg = default_fg, text = '0', font = 'Consolas 12 bold')

actionbtn = Label(shwin.winframe, bg = 'grey35', fg = '#3A6FFF', text = 'Shred files', font = 'Consolas 12 bold', pady = 3)#Button

#Section 2
description.dnd_bind('<<Drop>>', dropped)

addbtn.bind('<Enter>', hover)
addbtn.bind('<Leave>', unhover)
addbtn.bind('<1>', browse)

actionbtn.bind('<Enter>', hover)
actionbtn.bind('<Leave>', unhover)
actionbtn.bind('<1>', shproxy)

#Section 2.5
desc_frame.pack(fill = 'x')
description.pack(anchor = 'nw')

sh_lblframe.pack(fill = 'both')
shlist_frame.pack(fill = 'both', expand = True)
shlist_frame2.pack(fill = 'both', expand = True)
shlistbox.pack(fill = 'both', expand = True)

pad.pack()
addlabel.pack(side = 'left')
addbox.pack(side = 'left')
addbtn.pack()

op_lblframe.pack(fill = 'both')
option_frame.pack(fill = 'both', expand = True)
pflabel.pack(side = 'left')
pfchbtn.pack(side = 'left')

st_lblframe.pack(fill = 'both')
status_frame.pack(fill = 'both', expand = True)
statelabel.grid(row = 0, column = 0, sticky = 'w')
currentstate.grid(row = 0, column = 1)

countlabel.grid(row = 1, column = 0, sticky = 'w')
currentcount.grid(row = 1, column = 1)

actionbtn.pack(pady = 5)

#Section 3
shwin.mainloop()
