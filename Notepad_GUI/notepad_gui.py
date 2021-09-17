import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import os

def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    text_area.delete(1.0, tk.END)

def openFile():
    global file
    file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), \
        ("Text Documents", "*.txt")])

    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        # clear text area before read text from file
        text_area.delete(1.0, tk.END) 

        with open(file, 'r') as f:
            # read text from file
            text_area.insert(1.0, f.read())

def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(defaultextension='Untitled.txt', \
            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])

        if file == "":
            file = None
        else:
            with open(file, 'w') as f:
                f.write(text_area.get(1.0, tk.END))

            root.title(os.path.basename(file) + ' - Notepad')

    else:
        with open(file, 'w') as file:
            file.write(text_area(1.0, tk.END))

def exitNotepad():
    root.destroy()

def cut():
    text_area.event_generate(("<<Cut>>"))

def copy():
    text_area.event_generate(("<<Copy>>"))

def paste():
    text_area.event_generate(("<<Paste>>"))

def create_menubar():
    menuBar = tk.Menu(root) # create menu bar

    # create file menu
    fileMenu = tk.Menu(menuBar, tearoff=0)
    fileMenu.add_command(label="New", command=newFile) # to open new file
    fileMenu.add_command(label="Open", command=openFile) # to open existing file
    fileMenu.add_command(label="Save", command=saveFile) # save current file
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=exitNotepad)
    menuBar.add_cascade(label="File", menu=fileMenu)

    # create edit menu
    editMenu = tk.Menu(menuBar, tearoff=0)
    editMenu.add_command(label="Cut", command=cut) # cut text
    editMenu.add_command(label="Copy", command=copy) # copy text
    editMenu.add_command(label="Paste", command=paste) # paste text
    menuBar.add_cascade(label="Edit", menu=editMenu)
        
    root.config(menu=menuBar)

def create_text_area():
    # create text area
    textArea = tk.Text(root, font=(set_font_type, set_font_size), padx=10, pady=10)
    textArea.pack(fill=tk.BOTH, expand=True)

    # add scrollbar
    scrollbar = tk.Scrollbar(textArea)
    scrollbar.pack(side=tk.RIGHT, fill='y')
    scrollbar.config(command=textArea.yview)
    textArea.config(yscrollcommand=scrollbar.set)

    return textArea

def change_font_type(event):
    global set_font_type
    get_text = font.Font(font=text_area["font"]).actual()
    set_font_type = font_family.get()
    text_area.configure(font=(set_font_type, set_font_size, get_text["weight"], get_text["slant"]))

def change_font_size(event):
    global set_font_size
    get_text = font.Font(font=text_area["font"]).actual()
    set_font_size = font_size.get()
    text_area.configure(font=(set_font_type, set_font_size, get_text["weight"], get_text["slant"]))

def change_font_weight():
    get_text = font.Font(font=text_area["font"]).actual()
    if get_text["weight"] == 'normal':
        text_area.configure(font=(set_font_type, set_font_size, 'bold', get_text["slant"]))
        bold_button.configure(bg='black', fg='white')

    if get_text["weight"] == 'bold':
        text_area.configure(font=(set_font_type, set_font_size, 'normal', get_text["slant"]))
        bold_button.configure(bg='white', fg='black')

def change_font_style():
    get_text = font.Font(font=text_area["font"]).actual()
    if get_text["slant"] == 'roman':
        text_area.configure(font=(set_font_type, set_font_size, get_text["weight"], 'italic'))
        italic_button.configure(bg='black', fg='white')

    if get_text["slant"] == 'italic':
        text_area.configure(font=(set_font_type, set_font_size, get_text["weight"], 'roman'))
        italic_button.configure(bg='white', fg='black')

def create_footer():
    footer_label = tk.Label(text=f'Char {total_char}', padx=5, pady=5)
    footer_label.pack(fill="both", side=tk.RIGHT)
    return footer_label

def count_character(event):
    global total_char
    if text_area.edit_modified():
        total_char = len(text_area.get(1.0, tk.END).replace(" ", ""))
        get_total_char.configure(text=f'Char {total_char - 1}')

    text_area.edit_modified(False)

if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap("Notepad_GUI/notepad.ico")
    root.title("Untitled - Notepad")
    root.geometry('600x450')
    root.minsize(400,300)

    file = None

    set_font_type = "Arial"
    set_font_size = 12

    total_char = 0

    # create menu bar
    create_menubar()
    
    # create tool bar
    tb_label = tk.Label(root, bg='light gray')
    tb_label.pack(side=tk.TOP, fill=tk.BOTH)

    # create combo box for font type
    font_tuple = font.families()
    font_family = tk.StringVar()
    chooseFont = ttk.Combobox(tb_label, width=20, textvariable=font_family, state="readonly")
    chooseFont["values"] = font_tuple
    chooseFont.current(font_tuple.index("Arial"))
    chooseFont.grid(column=0, row=0, padx=5, pady=4)
    chooseFont.bind("<<ComboboxSelected>>", change_font_type)

    # create combo box for font size
    font_size = tk.IntVar()
    chooseFontSize = ttk.Combobox(tb_label, width=8, textvariable=font_size, state="readonly")
    chooseFontSize['values'] = tuple(range(8, 49, 2))
    chooseFontSize.current(2)
    chooseFontSize.grid(column=1, row=0, padx=5, pady=4)
    chooseFontSize.bind("<<ComboboxSelected>>", change_font_size)

    # create bold button
    bold_button = tk.Button(tb_label, text='B', font="Arial 8 bold", padx=5, pady=0)
    bold_button.grid(column=2, row=0, padx=5, pady=4)
    bold_button.configure(command=change_font_weight)

    # create italic button
    italic_button = tk.Button(tb_label, text='I', font="Arial 8 italic bold", padx=6, pady=0)
    italic_button.grid(column=3, row=0, padx=5, pady=4)
    italic_button.configure(command=change_font_style)

    # create text area
    text_area = create_text_area()

    # create footer
    get_total_char = create_footer()

    # count character
    text_area.bind("<<Modified>>", count_character)

    root.mainloop()
