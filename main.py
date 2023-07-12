import tkinter
import tkinter.messagebox
import tkinter.ttk
from tkinter import *
from tkinter import filedialog
import threading
import organizer
import os

root = Tk()
root.geometry('350x400')
root.title('File Organizer')
root.resizable(False, False)

dir_path = StringVar()


def main_menu():
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
        organize_progress_bar.place(x=10, y=140)

        organize_task = threading.Thread(target=organizer.organize, args=(dir_path, organize_progress_bar,
                                                                          output_text,), daemon=True)
        organize_task.start()

    frame_main = LabelFrame(root, padx=10, pady=10)
    frame_main.place(x=2, y=2, height=350, width=348)

    button_select_path = Button(master=frame_main, text='Select a path', command=select_path)
    button_select_path.place(x=5, y=10, width=100)

    entry_path_info = Entry(frame_main, font=('italic', '8'), justify=LEFT)
    entry_path_info.insert(0, 'Path: None')
    entry_path_info.place(x=113, y=13, width=200, height=20)

    label_file_count = Label(frame_main, text='Files: 0',  font=('italic', '8'), justify=LEFT)
    label_file_count.place(x=10, y=40)

    button_start = Button(master=frame_main, text='Start', command=start,)
    button_start.place(x=60, y=100, width=200)
    button_start.config(state='disabled')

    button_quit = Button(master=root, text="Quit", command=quit_m,)
    button_quit.place(x=80, y=360, height=30, width=200)

    label_output = Label(frame_main, text='Output', font=('italic', 10))
    label_output.place(x=135, y=140)

    output_text = Text(frame_main, width=50, height=11, font=('italic', 8), state='normal',)
    output_text.place(x=0, y=165)

    sb = Scrollbar(frame_main)
    sb.place(x=305, y=165, height=160)

    output_text.config(yscrollcommand=sb.set)
    sb.config(command=output_text.yview)


main_menu_task = threading.Thread(target=main_menu, daemon=True)
main_menu_task.start()

root.mainloop()

