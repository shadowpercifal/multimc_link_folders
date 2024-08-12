import os
import sys
import json
from safe_call import safe 
import curseForge_instance_linking as cF

ROOT_NAME = "root_folder"
MULTIMC_NAME = "multimc_folder"

@safe(True)
def get_config():
    default_config = {ROOT_NAME: "", MULTIMC_NAME: ""}
    if os.path.isfile('./config.json'):
        with open('config.json') as f:
            config = json.load(f)
    else:
        with open('config.json', 'w') as f:
            f.write(json.dumps(default_config, indent=4))
            config = default_config
    return config


@safe(True)
def save_config(new_config):
    with open('config.json', 'w') as f:
            f.write(json.dumps(new_config, indent=4))