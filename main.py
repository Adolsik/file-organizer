import tkinter.ttk
from tkinter import *
from tkinter import filedialog
import threading
import organizer

root = Tk()
root.geometry('350x400')
root.title('File Organizer')
root.resizable(False, False)

dir_path = StringVar()


def main_menu():
    def select_path():
        global dir_path
        dir_path = filedialog.askdirectory(initialdir='/', title='Select dir',)
        label_path_info.config(text=f'{dir_path}')
        button_start.config(state='normal')

    def quit_m():
        root.destroy()

    def start():
        organize_progress_bar = tkinter.ttk.Progressbar(frame_main, orient=HORIZONTAL, length=300, mode='indeterminate')
        organize_progress_bar.place(x=10, y=140)

        label_info = Label(frame_main, text='Moving files...', font=('italic', 8))
        label_info.place(x=10, y=170)

        organize_task = threading.Thread(target=organizer.organize, args=(dir_path, organize_progress_bar, label_info,),
                                         daemon=True)
        organize_task.start()
        button_start.config(state='disabled')

    frame_main = LabelFrame(root, padx=10, pady=10)
    frame_main.place(x=2, y=2, height=350, width=348)

    button_select_path = Button(master=frame_main, text='Select path', command=select_path)
    button_select_path.place(x=5, y=10, width=100)

    label_path_info = Label(frame_main, text=f'Path: None ', font=('italic', '8'), wraplength=200, justify=LEFT)
    label_path_info.place(x=113, y=13)

    button_start = Button(master=frame_main, text='Start', command=start,)
    button_start.place(x=60, y=100, width=200)
    button_start.config(state='disabled')

    button_quit = Button(master=root, text="Quit", command=quit_m,)
    button_quit.place(x=80, y=360, height=30, width=200)


main_menu_task = threading.Thread(target=main_menu, daemon=True)
main_menu_task.start()

root.mainloop()

