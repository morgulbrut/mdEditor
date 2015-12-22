__author__ = 't800'

import tkinter
from tkinter import *
import tkinter.scrolledtext as tkst
import tkinter.filedialog as tkFileDialog
import tkinter.messagebox as tkMessageBox

import pypandoc

root = tkinter.Tk(className="mdEditor")
textPad = tkst.ScrolledText(root, width=100, height=50)
template = 'templates/default.tex'


def select_template():
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select a template')
    if file != None:
        global template
        template = str(file.name)


def open_command():
    file = tkFileDialog.askopenfile(parent=root, mode='rb', title='Select a file')
    if file != None:
        contents = file.read()
        textPad.insert('1.0', contents)
        file.close()


def save_command():
    file = tkFileDialog.asksaveasfile(mode='w', defaultextension='md', title='Save markdown...')
    if file != None:
        # slice off the last character from get, as an extra return is added
        data = textPad.get('1.0', END + '-1c')
        file.write(data)
        file.close()


def save_as_pdf():
    try:
        file = tkFileDialog.asksaveasfile(mode='w', defaultextension='pdf', title='Save pdf...')
    except PermissionError:
        tkMessageBox.showwarning('Error', 'Maybe the file is open')
    if file != None:
        text = textPad.get('1.0', END + '-1c')
        try:
            pypandoc.convert(text, 'latex-yaml_metadata_block', outputfile=file.name, format='md',
                             extra_args=['-s', '--template=' + template, '--listings', '--latex-engine=xelatex'])
        finally:
            file.close()


def exit_command():
    if tkMessageBox.askokcancel('Quit', 'Do you really want to quit?'):
        root.destroy()


def about_command():
    label = tkMessageBox.showinfo('About', 'Just Another TextPad \n Copyright \n No rights left to reserve')


def dummy():
    pass


menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='New', command=dummy)
filemenu.add_command(label='Open...', command=open_command)
filemenu.add_command(label='Save as MD', command=save_command)
filemenu.add_separator()
filemenu.add_command(label='Render PDF', command=save_as_pdf)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=exit_command)

templatemenu = Menu(menu)
menu.add_cascade(label='Template', menu=templatemenu)
templatemenu.add_command(label='Select template', command=select_template)

helpmenu = Menu(menu)
menu.add_cascade(label='Help', menu=helpmenu)
helpmenu.add_command(label='About...', command=about_command)

textPad.pack()
root.mainloop()
