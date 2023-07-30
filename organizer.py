import tkinter
from tkinter import messagebox
import os
import shutil

file_ext_dict = {}


def config_ext():
    os.system('notepad config.txt')
    tkinter.messagebox.showinfo('Info', 'Config updated')


def organize(path: str, progress_bar, info):
    # Returns error if selected path is empty or not found
    try:
        files = os.listdir(path)
    except FileNotFoundError:
        return messagebox.showerror('Error', 'Selected path not found')

    file_ext_dict.clear()
    with open('config.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split(':')
                file_ext_dict[key] = value.strip()

    # Progress bar and info
    progress_bar.start()
    info.config(state='normal')
    info.delete('1.0', tkinter.END)
    info.insert(tkinter.END, f'Organizing files in {path} \n')


    # Organize files
    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            file_stats = os.stat(os.path.join(path, file))
            file_size_mb = file_stats.st_size / (1024 * 1024)
            name, extension = os.path.splitext(file.lower())

            info.see('end')
            try:
                dir_to_move = file_ext_dict.get(extension)

                # Create labeled folder
                is_exist = os.path.exists(path + '/' + dir_to_move)
                if not is_exist:
                    os.mkdir(path + '/' + dir_to_move)
                    info.insert(tkinter.END, f'\n Folder {dir_to_move} created  \n')

                # Moving files to directories
                info.insert(tkinter.END, f'\n Moving {file} into {dir_to_move} \n Size: {round(file_size_mb, 3)}'
                                         f' MB \n')
                shutil.move(os.path.join(path, file), os.path.join(path, dir_to_move))
            except TypeError:
                is_exist = os.path.exists(path + '/Other')
                if not is_exist:
                    os.mkdir(path + '/Other')
                    info.insert(tkinter.END, f'\n Folder Other created  \n')
                shutil.move(os.path.join(path, file), os.path.join(path, 'Other'))

    progress_bar.stop()
    info.insert(tkinter.END, f'\n Success! \n')
    info.see('end')
    info.config(state='disabled')
    progress_bar.stop()
    messagebox.showinfo('Task Completed', 'All files moved into successfully')
    os.system(f'start {path}')
