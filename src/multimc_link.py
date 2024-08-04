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
            selector(config)
        elif not os.path.isdir(user_input) or not os.path.isdir(os.path.join(user_input, "instances")):
            print('Enter a valid path')
            continue
        else:
            config['multimc_folder_i'] = True
            config['multimc_folder'] = user_input
            config['multimc_instances_folder'] = user_input + '/instances'
            if config['root_folder_i'] == False:
                root_folder_select(config)
            else:
                selector(config)


def root_folder_select(config):
    while True:
        user_input = input('''1. Enter a path to miecraft root folder;
2. Select default minecraft folder;
3. Create main folder in multimc;
0. Exit:
''')
        match user_input.lower():
            case '0':
                selector(config)
            case 'exit':
                selector(config)
            case '1':
                while True:
                    root_folder = input('Enter a minecraft folder, like "/.minecraft" or exit:\n').replace('\\', '/')
                    if root_folder == 'exit':
                        break
                    elif not os.path.isdir(root_folder):
                        print('Enter a valid path')
                        continue
                    config['root_folder'] = root_folder
                    config['root_folder_i'] = True
                    selector(config)
            case '2':
                root_folder = os.environ['USERPROFILE'] + '/AppData/Roaming/.minecraft'
                config['root_folder'] = root_folder
                config['root_folder_i'] = True
                selector(config)
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
                selector(config)


def link(config):
    dir_list = []
    for name in os.listdir(config['multimc_instances_folder']):
        if name != 'instgroups.json':
            if name != '_LAUNCHER_TEMP':
                print(name)
                dir_list.append(name)
    while True:
        user_input = input('Choose a minecraft instance or exit:\n')
        folder = config['multimc_instances_folder'] + '/' + user_input
        if user_input == 'exit':
            selector(config)
        elif not os.path.isdir(folder):
            print('Enter a valid path')
            continue
        else:
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
                except OSError:
                    print('Privilage error, run program with a administrator privilages')
                    break


def selector(config):
    while True:
        selector = (input('1. Link folders | 2. Change multimc folder | 3. Change root folder | 0. Exit:\n'))
        if selector.isdigit() and int(selector) < 4 or int(selector) == 0:
            match int(selector):
                case 1:
                    link(config)
                case 2:
                    multimc_folder_select(config)
                case 3:
                    root_folder_select(config)
                case 0:
                    os.chdir(multimc)
                    config = json.dumps(config)
                    with open('config.json', 'w') as f:
                        f.write(config)
                    break
        elif selector.isalpha():
            print(f"{selector} is not a number")
        else:
            print(f'{selector} is not a selector menu')


if config['multimc_folder_i'] is False:
    multimc_folder_select(config)
selector(config)

os.system('pause')