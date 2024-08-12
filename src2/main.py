import os
import sys
import json
import curseForge_instance_linking as cF
from config import get_config, save_config, ROOT_NAME, MULTIMC_NAME
from question import GetInputOrExit
from safe_call import safe, safe_mkdir
from admin_elevation import get_admin

ROOT_FOLDERS = ["resourcepacks", "saves", "screenshots", "shaderpacks"]

@safe(False)
def check_multimc_main_dir(path):
    return os.path.isdir(path) and os.path.isdir(os.path.join(path, "instances"))

@safe(False)
def check_root_dir(path):
    return os.path.isdir(path) and all([os.path.isdir(os.path.join(path, folder)) for folder in ROOT_FOLDERS])

def get_minecraft_root():
    user_root = os.environ['USERPROFILE']
    match sys.platform:
        case "win32":
            return os.path.join(user_root, "AppData", "Roaming", ".minecraft")
        case "darwin":
            return os.path.join(user_root, "Library", "Application Support", "minecraft")
        case "linux":
            return os.path.join(user_root, ".minecraft")


def main():
    print("At any point type \"exit\" to exit program")
    if sys.platform == "win32": get_admin()
    config = get_config()
    multimc = config[MULTIMC_NAME]
    if not (check_multimc_main_dir(multimc)):
        multimc = GetInputOrExit("Specify MultiMC root directory: ", check_multimc_main_dir)
        if multimc == None: return ""
        config[MULTIMC_NAME] = multimc
        save_config(config)
    root_dir = config[ROOT_NAME]
    if not (check_root_dir(root_dir)):
        print('''1. Create main folder in multimc (Recommended)
            2. Select default minecraft folder
            3. Enter a path to miecraft root folder
            ''')
        option = GetInputOrExit("Selected option: ", lambda x: x in ["1", "2", "3"])
        match option:
            case None: return ""
            case "1":
                root_dir = os.path.join(multimc, "instance_root")
                if not safe_mkdir(root_dir): return "Error creating root directory in MultiMC folder! Check folder existance"
                for folder in ROOT_FOLDERS:
                    if not safe_mkdir(os.path.join(root_dir, folder)): return f"Error creating {folder} folder! Check MultiMC and instance_root folders existance!"
            case "2":
                root_dir = get_minecraft_root()
                if not os.path.isdir(root_dir): return "Default minecraft dir does not exist or does not contain required folders! Try initializing minecraft first!"
                if root_dir == None: return "Minecraft root dir can not be found automatically! Specify the path with option 3!"
            case "3":
                root_dir = GetInputOrExit("Specify minecraft root directory: ", check_root_dir)
                if root_dir == None: return ""
        config[MULTIMC_NAME] = root_dir
        save_config(config)
    # TODO: folder linking



if __name__ == "__main__":
    return_value = main()
    print(return_value)
    os.system("pause")

