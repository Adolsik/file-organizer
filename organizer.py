from tkinter import messagebox
import threading
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

    # Making folders
    try:
        for dir_name in dir_names:
            os.mkdir(path + '/' + dir_name)
    except FileExistsError:
        messagebox.showwarning('Warning', 'Folders already exist. Delete them and try again.')
        progress_bar.stop()
        info.config(text='Error occurred. Try again')

    # Moving files to directories
    files = os.listdir(path)

    for file in files:
        if os.path.isfile(os.path.join(path, file)):
            extension = file[file.find('.'):len(file)]
            try:
                dir_to_move = file_ext_dict.get(extension)
                info.config(text=f'Moving {file}...')
                shutil.move(os.path.join(path, file), os.path.join(path, dir_to_move))
            except TypeError:
                shutil.move(os.path.join(path, file), os.path.join(path, 'Other'))

    progress_bar.stop()
    info.config(text=f'Success')
    messagebox.showinfo('Task Completed', 'All files moved successfully')
