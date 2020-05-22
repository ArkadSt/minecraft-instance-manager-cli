import os
import platform
import shutil
import sys
import ctypes
from pathlib import Path

if platform.system() == 'Linux':
    minecraft_parent_directory = os.getenv('HOME') + '/.'
elif platform.system() == 'Darwin':
    minecraft_parent_directory = os.getenv('HOME') + '/Library/Application Support/'
elif platform.system() == 'Windows':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    minecraft_parent_directory = os.getenv('APPDATA') + '\\.'

minecraft_directory = minecraft_parent_directory + 'minecraft'
minecraft_instance_manager_directory = minecraft_parent_directory + 'minecraft_instance_manager'
instances_directory = minecraft_parent_directory + 'minecraft_instance_manager/instances/'
backups_directory = minecraft_parent_directory + 'minecraft_instance_manager/backups/'


if not os.path.exists(minecraft_instance_manager_directory):
    os.mkdir(minecraft_instance_manager_directory)
if not os.path.exists(instances_directory):
    os.mkdir(instances_directory)

def list_instances():
    if len(os.listdir(instances_directory)) > 0:
        for instance_name in os.listdir(instances_directory):
            if instance_name == '.DS_Store':
                continue
            print(' ' + instance_name, end='')
            if os.path.exists(minecraft_directory):
                try:
                    if instance_name == os.path.split(os.readlink(minecraft_directory))[1]:
                        print(' (active)', end='')
                except OSError:
                    pass
            print()
    else:
        print('No available instances found.')
def select_instance():
    if len(os.listdir(instances_directory)) > 0:
        if os.path.exists(minecraft_directory):
            if not os.path.islink(minecraft_directory):

                if not os.path.exists(backups_directory):
                    os.mkdir(backups_directory)
                
                backup_name = 'minecraft.backup'
                index = 1
                while os.path.exists(backups_directory + backup_name):
                    backup_name = 'minecraft.backup(' + str(index) + ')'
                    index += 1
                print('\nSeems like you have an existing Minecraft folder (' + minecraft_directory + '). It needs to be deleted first.\n')
                print('Choose the next step:')
                print('* Make a backup of the Minecraft folder and continue (b)')
                print("* Continue without making a backup. YOUR MINECRAFT FOLDER'S CONTENTS WILL BE LOST FOREVER!!! (nb)")
                print('* Cancel (c)\n')
                print('>>> ', end='')
                action = input()
                while action != 'b' and action != 'nb' and action != 'c':
                    print('Seems like you are drunk as well. Sober up and try again')
                    print('>>> ', end='')
                    action = input()
                if action == 'b':
                    os.rename(minecraft_directory, backups_directory + backup_name)
                    print('The backup (' + backups_directory + backup_name + ') was successfully created.')
                elif action == 'nb':
                    shutil.rmtree(minecraft_directory)
                elif action == 'c':
                    main()
        else:
            try:
                os.stat(minecraft_directory)
            except OSError:
                try:
                    os.remove(minecraft_directory)
                except FileNotFoundError:
                    pass

        print("Enter the name of the instance you want to select (type 'l' to list available instances, or 'c' to cancel): ", end='')
        instance_name = input()
        while (not os.path.exists(instances_directory + instance_name)
                or instance_name == '' or instance_name == 'l'
                or instance_name == 'c' or instance_name == '.DS_Store'):
            if instance_name == 'l':
                list_instances()
                select_instance()
                main()
            elif instance_name == 'c':
                main()
            elif instance_name == '.DS_Store':
                print("Are you kidding me? Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                instance_name = input()
            else:
                print("The instance with such name does not exist. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                instance_name = input()

        if os.path.exists(minecraft_directory):
            if os.path.islink(minecraft_directory):
                os.unlink(minecraft_directory)
        os.symlink(instances_directory + instance_name, minecraft_directory)
        print('The instance "' + instance_name + '" was selected successfully.')
    else:
        print('No available instances found.')
def unselect_instance():
    if os.path.exists(minecraft_directory):
        if os.path.islink(minecraft_directory):
            instance_name = os.path.split(os.readlink(minecraft_directory))[1]
            os.unlink(minecraft_directory)
            print('The instance "' + instance_name + '" was successfully unselected.')
    else:
        print('None of the instances are selected.')
def create_instance():
    print("Enter the name of the instance you want to create (without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
    instance_name = input()

    while (os.path.exists(instances_directory + instance_name)
            or instance_name == 'l' or instance_name == 'c'
            or instance_name == '.DS_Store'):
        if instance_name == '':
            print("The name of the instance cannot be blank. Try again (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
            instance_name = input()
        elif instance_name == 'l':
            list_instances()
            create_instance()
            main()
        elif instance_name == 'c':
            main()
        elif instance_name == '.DS_Store':
            print("Are you kidding me? Just choose a normal name (type 'l' to list available instances, or 'c' to cancel): ", end='')
            instance_name = input()
        else:
            print('An instance with the same name already exists. Do you want to override the instance? (y/n): ', end = '')
            action = input()
            while action != 'y' and action != 'n':
                print('Invalid input. Alright... So what, do you want to override the instance? (y/n): ', end = '')
                action = input()
            if action == 'y':
                shutil.rmtree(instances_directory + instance_name)
            elif action == 'n':
                main()

    os.mkdir(instances_directory + instance_name)
    os.mkdir(instances_directory + instance_name + '/mods')
    os.mkdir(instances_directory + instance_name + '/resourcepacks')
    os.mkdir(instances_directory + instance_name + '/saves')
    
    # Not necessary, just for indication purposes
    Path(instances_directory + instance_name + '/' + instance_name + '.mp3').touch() 
    
    print('The "' + instance_name + '" instance was successfully created.')
def delete_instance():
    if len(os.listdir(instances_directory)) > 0:
        print("Enter the name of the instance you want to delete (type 'l' to list available instances, or 'c' to cancel): ", end='')
        instance_name = input()
        while (not os.path.exists(instances_directory + instance_name)
                or instance_name == '' or instance_name == 'l'
                or instance_name == 'c' or instance_name == '.DS_Store'):
            if instance_name == 'l':
                list_instances()
                delete_instance()
                main()
            elif instance_name == 'c':
                main()
            elif instance_name == '.DS_Store':
                print("I work with Minecraft instances, not with this Apple related shit. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                instance_name = input()
            else:
                print("The instance with such name does not exist. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                instance_name = input()

        if os.path.exists(minecraft_directory):
            if os.path.islink(minecraft_directory):
                if instance_name == os.path.split(os.readlink(minecraft_directory))[1]:
                    os.unlink(minecraft_directory)

        shutil.rmtree(instances_directory + instance_name)
        print('The instance "' + instance_name + '" was deleted successfully')
    else:
        print('No available instances found.')
def menu():
    print('\nMenu: ')
    print('* Display this menu (m)')
    print('* List available instances (l)')
    print('* Select instance (s)')
    print('* Unselect instance (u)')
    print('* Create instance (c)')
    print('* Delete instance (d)')
    print('* Exit (q)\n')
    print('Enter the appropriate letter.')

def main():
    print(">>> (type 'm' to display the menu): ", end='')

    action = input()

    if action == 'm':
        menu()
    elif action == 'l':
        list_instances()
    elif action == 's':
        select_instance()
    elif action == 'u':
        unselect_instance()
    elif action == 'c':
        create_instance()
    elif action == 'd':
        delete_instance()
    elif action == 'q':
        sys.exit(0)

    else:
        print('Invalid input')
    main()

menu()
main()
