import tkinter
import tkinter.messagebox
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
import threading
import organizer
import os

root = Tk()
root.geometry('350x450')
root.title('File Organizer')
root.resizable(False, False)

root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")

dir_path = StringVar()


def main_menu():
    # 1.0.1b
    def change_theme():
        if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
            # Set light theme
            root.tk.call("set_theme", "light")
            switch_themes.config(text='Dark mode')
        else:
            # Set dark theme
            root.tk.call("set_theme", "dark")
            switch_themes.config(text='Light mode')

    def select_path():
        global dir_path

        try:
            dir_path = filedialog.askdirectory(initialdir='/', title='Select dir',)

            # v1.0.1 file counter
            def file_counter():
                counter = 0
                files = os.listdir(dir_path)
                for file in files:
                    if os.path.isfile(os.path.join(dir_path, file)):
                        counter += 1
                return counter

            label_file_count.config(text=f'Files: {file_counter()}')
        except FileNotFoundError:
            tkinter.messagebox.showerror('Error', 'Directory not found')

        entry_path_info.delete(0, tkinter.END)
        entry_path_info.insert(0, f'{dir_path}')
        button_start.config(state='normal')

    def quit_m():
        root.destroy()

    def start():
        button_start.config(state='disabled')

        organize_progress_bar = tkinter.ttk.Progressbar(frame_main, orient=HORIZONTAL, length=300, mode='indeterminate')
        organize_progress_bar.place(x=10, y=137)

        organize_task = threading.Thread(target=organizer.organize, args=(dir_path, organize_progress_bar,
                                                                          output_text,), daemon=True)
        organize_task.start()

    frame_main = LabelFrame(root, padx=10, pady=10)
    frame_main.place(x=2, y=40, height=350, width=348)

    button_select_path = tkinter.ttk.Button(master=frame_main, text='Select a path', command=select_path)
    button_select_path.place(x=5, y=10, width=100)

    entry_path_info = tkinter.ttk.Entry(frame_main, font=('italic', '8'), justify=LEFT)
    entry_path_info.insert(0, 'Path: None')
    entry_path_info.place(x=113, y=13, width=200, height=25)

    label_file_count = tkinter.ttk.Label(frame_main, text='Files: 0', justify=LEFT)
    label_file_count.place(x=10, y=47)

    button_start = tkinter.ttk.Button(master=frame_main, text='Start', command=start,)
    button_start.place(x=60, y=100, width=200)
    button_start.config(state='disabled')

    button_quit = tkinter.ttk.Button(master=root, text="Quit", command=quit_m,)
    button_quit.place(x=80, y=400, height=30, width=200)

    label_output = tkinter.ttk.Label(frame_main, text='Output', font=('italic', 10))
    label_output.place(x=135, y=145)

    output_text = Text(frame_main, width=52, height=11, font=('italic', 8), state='normal',)
    output_text.place(x=0, y=165)

    sb_output = tkinter.ttk.Scrollbar(frame_main, orient='vertical')
    sb_output.place(x=315, y=165, height=158)

    output_text.config(yscrollcommand=sb_output.set)
    sb_output.config(command=output_text.yview)

    sb_path = tkinter.ttk.Scrollbar(frame_main, orient='horizontal')
    sb_path.place(x=113, y=40, height=20, width=200)

    switch_themes = tkinter.ttk.Checkbutton(root, text='Dark mode', style='Switch.TCheckbutton', command=change_theme)
    switch_themes.place(x=0, y=5)

    entry_path_info.config(xscrollcommand=sb_path.set)
    sb_path.config(command=entry_path_info.xview)


main_menu_task = threading.Thread(target=main_menu, daemon=True)
main_menu_task.start()

root.mainloop()

