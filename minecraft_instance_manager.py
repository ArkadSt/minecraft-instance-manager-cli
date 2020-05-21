import os
import platform
import shutil
import sys
import ctypes
from pathlib import Path

if platform.system() == 'Linux':
    minecraft_parent_directory = os.getenv('HOME') + '/.'
elif platform.system() == 'Windows':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    minecraft_parent_directory = os.getenv('APPDATA') + '\\.'
elif platform.system() == 'Darwin':
    minecraft_parent_directory = os.getenv('HOME') + '/'

if not os.path.exists(minecraft_parent_directory + 'minecraft_instance_manager'):
    os.mkdir(minecraft_parent_directory + 'minecraft_instance_manager')
if not os.path.exists(minecraft_parent_directory + 'minecraft_instance_manager/instances'):
    os.mkdir(minecraft_parent_directory + 'minecraft_instance_manager/instances')

def list_instances():
    if len(os.listdir(minecraft_parent_directory + 'minecraft_instance_manager/instances')) > 0:
        for instance_name in os.listdir(minecraft_parent_directory + 'minecraft_instance_manager/instances'):
            print(instance_name, end='')
            if os.path.exists(minecraft_parent_directory + 'minecraft'):
                try:
                    if instance_name == os.path.split(os.readlink(minecraft_parent_directory + 'minecraft'))[1]:
                        print(' (active)', end='')
                except OSError:
                    pass
            print()
    else:
        print('No available instances found.')
def select_instance():
    if len(os.listdir(minecraft_parent_directory + 'minecraft_instance_manager/instances')) > 0:
        print("Enter the name of the instance you want to select (type 'l' to list available instances, or 'c' to cancel): ", end='')
        instance_name = input()
        while not os.path.exists(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name) or instance_name == '' or instance_name == 'l' or instance_name == 'c':
            if instance_name == 'l':
                list_instances()
                select_instance()
                main()
            elif instance_name == 'c':
                main()
            else:
                print("The instance with such name does not exist. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                instance_name = input()
        if os.path.exists(minecraft_parent_directory + 'minecraft'):
            if os.path.islink(minecraft_parent_directory + 'minecraft'):
                os.unlink(minecraft_parent_directory + 'minecraft')
            else:
                print('All the contents of the ' + minecraft_parent_directory + 'minecraft will be lost. Make sure that you have made a backup of your worlds. Do you want to continue? (y/n): ', end='')
                action = input()
                while action != 'y' and action != 'n':
                    print('Invalid input. Alright... So what, do you want to continue? (y/n): ', end = '')
                    action = input()
                if action == 'y':
                    shutil.rmtree(minecraft_parent_directory + 'minecraft')
                elif action == 'n':
                    main()
        else:
            try:
                os.stat(minecraft_parent_directory + 'minecraft')
            except OSError:
                try:
                    os.remove(minecraft_parent_directory + 'minecraft')
                except FileNotFoundError:
                    pass
                
        os.symlink(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name, minecraft_parent_directory + 'minecraft')
        print('The instance "' + instance_name + '" was selected successfully.')
    else:
        print('No available instances found.')
def unselect_instance():
    if os.path.exists(minecraft_parent_directory + 'minecraft'):
        if os.path.islink(minecraft_parent_directory + 'minecraft'):
            instance_name = os.path.split(os.readlink(minecraft_parent_directory + 'minecraft'))[1]
            os.unlink(minecraft_parent_directory + 'minecraft')
            print('The instance "' + instance_name + '" was successfully unselected.')
    else:
        print('None of the instances are selected.')
def create_instance():
    print("Enter the name of the instance you want to create (without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
    instance_name = input()

    while os.path.exists(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name) or instance_name == 'l' or instance_name == 'c':
        if instance_name == '':
            print("The name of the instance cannot be blank. Try again (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
            instance_name = input()
        elif instance_name == 'l':
            list_instances()
            create_instance()
            main()
        elif instance_name == 'c':
            main()
        else:
            print('An instance with the same name already exists. Do you want to override the instance? (y/n): ', end = '')
            action = input()
            while action != 'y' and action != 'n':
                print('Invalid input. Alright... So what, do you want to override the instance? (y/n): ', end = '')
                action = input()
            if action == 'y':
                shutil.rmtree(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name)
            elif action == 'n':
                main()

    os.mkdir(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name)
    os.mkdir(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name + '/mods')
    os.mkdir(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name + '/resourcepacks')
    os.mkdir(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name + '/saves')
    Path(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name + '/' + instance_name + '.mp3').touch() # Not necessary, just for testing purposes
    
    print('The "' + instance_name + '" instance was successfully created.')
def delete_instance():
    print("Enter the name of the instance you want to delete (type 'l' to list available instances, or 'c' to cancel): ", end='')
    instance_name = input()
    while not os.path.exists(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name) or instance_name == '' or instance_name == 'l' or instance_name == 'c':
        if instance_name == 'l':
            list_instances()
            delete_instance()
            main()
        elif instance_name == 'c':
            main()
        else:
            print("The instance with such name does not exist. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
            instance_name = input()

    if os.path.exists(minecraft_parent_directory + 'minecraft'):
        if os.path.islink(minecraft_parent_directory + 'minecraft'):
            if instance_name == os.path.split(os.readlink(minecraft_parent_directory + 'minecraft'))[1]:
                os.unlink(minecraft_parent_directory + 'minecraft')

    shutil.rmtree(minecraft_parent_directory + 'minecraft_instance_manager/instances/' + instance_name)
    print('The instance "' + instance_name + '" was deleted successfully')

def menu():
    print('\nMenu: ')
    print('Display this menu (m)')
    print('List available instances (l)')
    print('Select instance (s)')
    print('Unselect instance (u)')
    print('Create instance (c)')
    print('Delete instance (d)')
    print('Exit (q)\n')
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
