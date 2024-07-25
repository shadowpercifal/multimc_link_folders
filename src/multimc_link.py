import os
import sys

minecraft_folder = os.environ['USERPROFILE'] + '/AppData/Roaming/.minecraft'
folder_raw = input('Enter a file path:\n')
folder = ''
for char in folder_raw:
    folder += char.replace('\\', '/')
subfolders = [f'{folder}/saves', f'{folder}/shaderpacks', f'{folder}/screenshots', f'{folder}/resourcepacks']
minecraft_subfolders = [f'{minecraft_folder}/saves', f'{minecraft_folder}/shaderpacks', f'{minecraft_folder}/screenshots', f'{minecraft_folder}/resourcepacks']
for subfolder, minecraft_subfolder in zip(subfolders, minecraft_subfolders,):
    if os.path.isdir(subfolder) is True:
        try:
            os.rmdir(subfolder)
        except OSError:
            print(subfolder, ' is not empty')
            os.system('pause')
            sys.exit()
    os.symlink(minecraft_subfolder, subfolder)
os.system('pause')