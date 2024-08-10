import os
import sys
import json

multimc = os.getcwd()

config_status = os.path.isfile('./config.json')
if config_status is False:
    with open('config.json', 'x') as f:
        f.write('{"multimc_folder_i": false, "root_folder_i": false, "root_folder": "", "multimc_folder": "", "multimc_instances_folder": ""}')

with open('config.json') as f:
    config = json.load(f)


def multimc_folder_select(config):
    while True:
        user_input = input('Enter a path to multimc root folder, like "/MultiMC" or exit:\n').replace('\\', '/')
        if user_input == 'exit':
            break
        elif not os.path.isdir(user_input) or not os.path.isdir(os.path.join(user_input, "instances")):
            print('Enter a valid path')
            continue
        else:
            config['multimc_folder_i'] = True
            config['multimc_folder'] = user_input
            config['multimc_instances_folder'] = user_input + '/instances'
            print('Multimc folder selected')
            if config['root_folder_i'] == False:
                root_folder_select(config)
                break
            else:
                break


def root_folder_select(config):
    root_selected = 'Root folder selected'
    exit_main = False
    exit = False
    while not exit_main:
        user_input = input('''1. Enter a path to miecraft root folder;
2. Select default minecraft folder;
3. Create main folder in multimc;
0. Exit:
''')
        match user_input.lower():
            case '0':
                exit_main = True
            case 'exit':
                exit_main = True
            case '1':
                while not exit:
                    root_folder = input('Enter a minecraft folder, like "/.minecraft" or exit:\n').replace('\\', '/')
                    if root_folder == 'exit':
                        exit = True
                    elif not os.path.isdir(root_folder):
                        print('Enter a valid path')
                        continue
                    config['root_folder'] = root_folder
                    config['root_folder_i'] = True
                    exit = True
                    print(root_selected)
            case '2':
                root_folder = os.environ['USERPROFILE'] + '/AppData/Roaming/.minecraft'
                config['root_folder'] = root_folder
                config['root_folder_i'] = True
                exit_main = True
                print(root_selected)
            case '3':
                os.chdir(config['multimc_folder'])
                instances_folders = ['instances_root_folder', 'instances_root_folder/saves', 'instances_root_folder/shaderpacks',
                                      'instances_root_folder/screenshots', 'instances_root_folder/resourcepacks']
                for folder in instances_folders:
                    try:
                        os.mkdir(folder)
                        print(folder + ' created')
                    except FileExistsError:
                        print(folder + ' already exist')
                config['root_folder'] = config['multimc_folder'] + '/instances_root_folder'
                config['root_folder_i'] = True
                print(root_selected)


def link(config):
    dir_list = []
    for name in os.listdir(config['multimc_instances_folder']):
        if name not in ['instgroups.json', '_LAUNCHER_TEMP']:
            print(name)
            dir_list.append(name)
    while True:
        user_input = input('Choose a minecraft instance or exit:\n')
        folder = config['multimc_instances_folder'] + '/' + user_input + '/.minecraft'
        print(folder)
        if user_input == 'exit':
            break
        if user_input in dir_list:
            subfolders = [f'{folder}/saves', f'{folder}/shaderpacks', f'{folder}/screenshots', f'{folder}/resourcepacks']
            minecraft_subfolders = [f'{config['root_folder']}/saves', f'{config['root_folder']}/shaderpacks', f'{config['root_folder']}/screenshots', f'{config['root_folder']}/resourcepacks']
            for subfolder, minecraft_subfolder in zip(subfolders, minecraft_subfolders):
                if os.path.isdir(subfolder) is True:
                    try:
                        os.rmdir(subfolder)
                    except OSError:
                        print(subfolder, ' is not empty')
                        os.system('pause')
                        sys.exit()
                try:
                    os.symlink(minecraft_subfolder, subfolder)
                    print(subfolder + " linked")
                except OSError:
                    print('Privilage error, run program with a administrator privilages')
                    break
        elif not os.path.isdir(folder):
            print('Enter a valid version')


def selector(config):
    exit = False
    while not exit:
        selector = (input('1. Link folders | 2. Change multimc folder | 3. Change root folder | 0. Exit:\n'))
        match selector:
            case '1':
                link(config)
            case '2':
                multimc_folder_select(config)
            case '3':
                root_folder_select(config)
            case '0':
                os.chdir(multimc)
                config = json.dumps(config)
                with open('config.json', 'w') as f:
                    f.write(config)
                exit = True
            case 'exit':
                os.chdir(multimc)
                config = json.dumps(config)
                with open('config.json', 'w') as f:
                    f.write(config)
                exit = True


if config['multimc_folder_i'] is False:
    multimc_folder_select(config)
if not os.path.isdir(config['multimc_instances_folder']):
    print('Cant find multimc folder')
    multimc_folder_select(config)
if not os.path.isdir(config['root_folder']):
    print('Cant find root folder')
    root_folder_select(config)
selector(config)

os.system('pause')