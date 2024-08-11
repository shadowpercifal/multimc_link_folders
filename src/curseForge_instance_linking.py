import os
import json


def instance_linking(config):
    curseforge_folder = os.path.join(os.environ['USERPROFILE'], 'curseforge/minecraft')
    curseforge_instances_folder = os.path.join(curseforge_folder, 'Instances')
    multimc_instances_folder = config['multimc_instances_folder']

    instances_dict = {}
    instance_i = 1
    while not os.path.isfile('C:/Launchers/MultiMC/icons/curseforge.png'):
        os.system('curl -o curseforge.png --output-dir C:/Launchers/MultiMC/icons https://i.imgur.com/NjSxb50.png')
    for instance in os.listdir(curseforge_instances_folder):
        print(f'{instance_i}. {instance}')
        instances_dict[f"{instance_i}"] = instance
        instance_i += 1


    def instance_linking(folder):
        print(folder)
        
        # folder and linking
        instance_folder = os.path.join(multimc_instances_folder, folder)
        instance_subfolder = os.path.join(instance_folder, '.minecraft')
        os.mkdir(instance_folder)
        os.symlink(os.path.join(curseforge_instances_folder, folder), instance_subfolder)

        # mmc-pack.json
        with open(os.path.join(curseforge_instances_folder, folder, 'manifest.json')) as manifest:
            manifest = json.load(manifest)['minecraft']
        modloader, modloader_version = manifest['modLoaders'][0]['id'].split('-', 1)
        version = f"{manifest['version']}"
        pack_properties = {
            "components": [
            {
                "cachedName": "Minecraft",
                "cachedVersion": version,
                "important": True,
                "uid": "net.minecraft",
                "version": version
                }
            ],
            "formatVersion": 1
        }   
        match modloader:
            case 'forge':
                modloader = 'Forge'
                cachedRequires = {'equals': version, 'uid': 'net.minecraft'}
                uid = "net.minecraftforge"
            case 'fabric':
                modloader = 'Fabric Loader'
                cachedRequires = {'uid': "net.fabricmc.intermediary"}
                uid = "net.fabricmc.fabric-loader"
            case 'neoforge':
                modloader = 'NeoForge'
                cachedRequires = {'equals': version, 'uid': "net.minecraft"}
                uid = "net.neoforged"
            case 'quilt':
                modloader = 'Quilt Loader'
                cachedRequires = {'uid': "net.fabricmc.intermediary"}
                uid = "org.quiltmc.quilt-loader"
        temp_pack_properties = {
            'cachedName': modloader,
            'cachedRequires': [cachedRequires],
            'cachedVersion': modloader_version,
            'uid': uid,
            'version': modloader_version
        }
        pack_properties['components'].append(temp_pack_properties)
        with open(os.path.join(instance_folder, 'mmc-pack.json'), 'x') as pack:
            pack.write(json.dumps(pack_properties, indent=3))

        # instgroups.json
        with open(os.path.join(multimc_instances_folder, 'instgroups.json')) as file:
            instgroups = json.load(file)
        try:
            instgroups['groups']['CurseForge']['instances'].append(folder)
        except:
            instgroups['groups']['CurseForge'] = {'hidden': False, 'instances': [folder]}
        print(instgroups)
        with open(os.path.join(multimc_instances_folder, 'instgroups.json'), 'w') as file:
            instgroups = json.dumps(instgroups, indent=3)
            file.write(instgroups)

        # cfg file for MultiMC
        if float(version[2:]) < 17:
            java = curseforge_folder + '/Install/java/Jre_8/bin/javaw.exe'
        elif float(version[2:]) <= 20.4:
            java = curseforge_folder + '/Install/runtime/java-runtime-gamma/windows-x64/java-runtime-gamma/bin/javaw.exe'
        else:
            java = curseforge_folder + '/Install/runtime/java-runtime-delta/windows-x64/java-runtime-delta/bin/javaw.exe'
        cfg_properties = f'''InstanceType=OneSix
    JavaPath={java}
    OverrideJavaLocation=true
    iconKey=curseforge
    name={folder}'''
        with open(os.path.join(instance_folder, 'instance.cfg'), 'x', encoding='utf-8') as cfg:
            cfg.write(cfg_properties)


    exit = False
    while not exit:
        selected_cf_instance = input('Select instance by name or index: ')
        if selected_cf_instance.lower() == 'exit':
            exit = True
        elif selected_cf_instance in instances_dict:
            instance_linking(instances_dict[selected_cf_instance])
        elif selected_cf_instance in instances_dict.values():
            instance_linking(selected_cf_instance)
        else:
            print('Instance not found. Please try again.')
