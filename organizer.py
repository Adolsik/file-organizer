import tkinter
from tkinter import messagebox
import os
import shutil

file_ext_dict = {}


def config_ext():
    os.system('notepad config.txt')
    tkinter.messagebox.showinfo('Info', 'Config updated')


def organize(path: str, progress_bar, info):
    file_ext_dict.clear()
    with open('config.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(':')
                file_ext_dict[key] = value.strip()

    dir_names = set(file_ext_dict.values())

    progress_bar.start()
    info.config(state='normal')
    info.delete('1.0', tkinter.END)

    # Making folders
    try:
        for dir_name in dir_names:
            os.mkdir(path + '/' + dir_name)
    except FileExistsError:
        messagebox.showwarning('Warning', 'Folders already exist. Delete them and try again.')
        progress_bar.stop()
        info.insert(tkinter.END, f'\n Error occurred. Try again \n')
        return 0
    info.insert(tkinter.END, '\n Folders created \n')

    # Moving files to directories
    files = os.listdir(path)

    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            file_stats = os.stat(os.path.join(path, file))
            file_size_mb = file_stats.st_size / (1024 * 1024)
            name, extension = os.path.splitext(file.lower())

            info.see('end')
            try:
                dir_to_move = file_ext_dict.get(extension)
                info.insert(tkinter.END, f'\n Moving {file} into {dir_to_move} \n Size: {round(file_size_mb, 3)}'
                                         f' MB \n')
                shutil.move(os.path.join(path, file), os.path.join(path, dir_to_move))
            except TypeError:
                shutil.move(os.path.join(path, file), os.path.join(path, 'Other'))

    progress_bar.stop()
    info.insert(tkinter.END, f'\n Success! \n')
    info.see('end')
    info.config(state='disabled')
    messagebox.showinfo('Task Completed', 'All files moved into successfully')
    os.system(f'start {path}')
