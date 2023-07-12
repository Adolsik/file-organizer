import tkinter
from tkinter import messagebox
import os
import shutil

file_ext_dict = {
    '.m4a': "Music",
    '.flac': "Music",
    '.mp3': "Music",
    '.mp4': "Music",
    '.wav': "Music",
    '.wma': "Music",
    '.aac': "Music",
    '.jpg': "Images",
    '.jpeg': "Images",
    '.png': "Images",
    '.gif': "Images",
    '.tiff': "Images",
    '.psd': "Images",
    '.eps': "Images",
    '.ai': "Images",
    '.ico': "Images",  # v 1.0.1
    '.mov': "Videos",
    '.wmv': "Videos",
    '.avi': "Videos",
    '.avchd': "Videos",
    '.flv': "Videos",
    '.f4v': "Videos",
    '.swf': "Videos",
    '.mkv': "Videos",
    '.webm': "Videos",
    '.html5': "Videos",
    '.pdf': "PDFs",
    '.exe': 'Executables',
    '.txt': 'Text files',
    '.rar': 'Archives',
    '.zip': 'Archives',
    'default': 'Other',
}

dir_names = set(file_ext_dict.values())


def organize(path: str, progress_bar, info):
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

            # If mp4's size is more than 10MB, app move it into Videos instead of Music
            if extension == '.mp4' and file_size_mb > 10:
                dir_to_move = 'Videos'
                info.insert(tkinter.END, f'\n Moving {file} into {dir_to_move} \n Size: {round(file_size_mb,3)} MB \n')
                shutil.move(os.path.join(path, file), os.path.join(path, dir_to_move))
            else:
                try:
                    dir_to_move = file_ext_dict.get(extension)
                    info.insert(tkinter.END, f'\n Moving {file} into {dir_to_move} \n Size: {round(file_size_mb,3)}'
                                             f' MB \n')
                    shutil.move(os.path.join(path, file), os.path.join(path, dir_to_move))
                except TypeError:
                    shutil.move(os.path.join(path, file), os.path.join(path, 'Other'))

    progress_bar.stop()
    info.insert(tkinter.END, f'\n Success! \n')
    info.see('end')
    info.config(state='disabled')
    messagebox.showinfo('Task Completed', 'All files moved into successfully')
