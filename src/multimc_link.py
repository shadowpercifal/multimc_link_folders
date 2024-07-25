import os
import sys

minecraft_folder = os.environ['USERPROFILE'] + '/AppData/Roaming/.minecraft'
folder_raw = input('Enter a file path:\n')
folder = ''
for char in folder_raw:
    folder += char.replace('\\', '/')
if os.path.isdir(f'{folder}/saves') is True:
    try:
        os.rmdir(f'{folder}/saves')
    except OSError:
        print(f'{folder}/saves is not empty')
        os.system('pause')
        sys.exit()
os.symlink(f'{minecraft_folder}/saves', f'{folder}/saves')
if os.path.isdir(f'{folder}/shaderpacks') is True:
    try:
        os.rmdir(f'{folder}/shaderpacks')
    except OSError:
        print(f'{folder}/shaderpacks is not empty')
        os.system('pause')
        sys.exit()
os.symlink(f'{minecraft_folder}/shaderpacks', f'{folder}/shaderpacks')
if os.path.isdir(f'{folder}/screenshots') is True:
    try:
        os.rmdir(f'{folder}/screenshots')
    except OSError:
        print(f'{folder}/screenshots is not empty')
        os.system('pause')
        sys.exit()
os.symlink(f'{minecraft_folder}/screenshots', f'{folder}/screenshots')
if os.path.isdir(f'{folder}/resourcepacks') is True:
    try:
        os.rmdir(f'{folder}/resourcepacks')
    except OSError:
        print(f'{folder}/resourcepacks is not empty')
        os.system('pause')
        sys.exit()
os.symlink(f'{minecraft_folder}/resourcepacks', f'{folder}/resourcepacks')
os.system('pause')