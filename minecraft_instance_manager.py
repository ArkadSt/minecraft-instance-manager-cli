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
minecraft_instance_manager_directory = minecraft_parent_directory + 'minecraft_instance_manager/'
instances_directory = minecraft_instance_manager_directory + 'instances/'
backups_directory = minecraft_instance_manager_directory + 'backups/'


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
                    backup_name = 'minecraft.backup({})'.format(str(index))
                    index += 1
                print('\nSeems like you have an existing Minecraft folder ({}). It needs to be deleted first.\n'.format(minecraft_directory))
                print('Choose the next step:')
                print('* Make a backup of the Minecraft folder and continue (b)')
                print("* Continue without making a backup. YOUR MINECRAFT FOLDER'S CONTENTS WILL BE LOST FOREVER!!! (nb)")
                print('* Cancel (c)\n')
                print('>>> ', end='')
                action = input()
                while action != 'b' and action != 'nb' and action != 'c':
                    print('Seems like you are drunk as well. Sober up and try again.')
                    print('>>> ', end='')
                    action = input()
                if action == 'b':
                    os.rename(minecraft_directory, backups_directory + backup_name)
                    print('The backup ({}) was successfully created.'.format(backups_directory + backup_name))
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
    if os.path.exists(minecraft_directory) and os.path.islink(minecraft_directory):
        instance_name = os.path.split(os.readlink(minecraft_directory))[1]
        os.unlink(minecraft_directory)
        print('The instance "{}" was successfully unselected.'.format(instance_name))
    else:
        print('None of the instances are selected.')
def create_instance(reset):
    if reset == '':
        print("Enter the name of the instance you want to create (without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
        instance_name = input()
    else:
        instance_name = reset

    while (os.path.exists(instances_directory + instance_name)
            or instance_name == 'l' or instance_name == 'c'
            or instance_name == '.DS_Store'):
        if instance_name == '':
            print("The name of the instance cannot be blank. Try again (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
            instance_name = input()
        elif instance_name == 'l':
            list_instances()
            create_instance(reset)
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
    
    if reset == '':
        print('The "{}" instance was successfully created.'.format(instance_name))

old_name = ''
new_name = ''
def rename_instance():
    if len(os.listdir(instances_directory)) > 0:
        global old_name
        global new_name
        if new_name != 'is being choosed already':
            print("Enter the name of the instance you want to rename (type 'l' to list available instances, or 'c' to cancel): ", end='')
            old_name = input()
            while (not os.path.exists(instances_directory + old_name)
                    or old_name == '' or old_name == 'l'
                    or old_name == 'c' or old_name == '.DS_Store'):
                if old_name == 'l':
                    list_instances()
                    rename_instance()
                    main()
                elif old_name == 'c':
                    main()
                elif old_name == '.DS_Store':
                    print("I work with Minecraft instances, not with this Apple related shit. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                    old_name = input()
                else:
                    print("The instance with such name does not exist. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                    old_name = input()

        print("Enter the new name of the instance (without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
        new_name = input()
        while (os.path.exists(instances_directory + new_name)
                or new_name == 'l' or new_name == 'c'
                or new_name == '.DS_Store'):
            if new_name == '':
                print("The name of the instance cannot be blank. Try again (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
                new_name = input()
            elif new_name == 'l':
                list_instances()
                new_name = 'is being choosed already'
                rename_instance()
                main()
            elif new_name == 'c':
                new_name = ''
                main()
            elif new_name == '.DS_Store':
                print("Are you kidding me? Just choose a normal name (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
                new_name = input()
            elif new_name == old_name:
                print("What for did you come here at all? Choose another name please (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
                new_name = input()
            else:
                print("An instance with the same name already exists. Choose another name please (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
                new_name = input()
        
        was_active = False
        if os.path.exists(minecraft_directory):
            if os.path.islink(minecraft_directory):
                if old_name == os.path.split(os.readlink(minecraft_directory))[1]:
                    os.unlink(minecraft_directory)
                    was_active = True
        
        os.rename(instances_directory + old_name, instances_directory + new_name)

        if was_active:
            os.symlink(instances_directory + new_name, minecraft_directory)
        print('Instance "{}" was successfully renamed to "{}".'.format(old_name, new_name))
    else:
        print('No available instances found.')
def duplicate_instance():
    if len(os.listdir(instances_directory)) > 0:
        global old_name
        global new_name
        if new_name != 'is being choosed already':
            print("Enter the name of the instance you want to make a duplicate of (type 'l' to list available instances, or 'c' to cancel): ", end='')
            old_name = input()
            while (not os.path.exists(instances_directory + old_name)
                    or old_name == '' or old_name == 'l'
                    or old_name == 'c' or old_name == '.DS_Store'):
                if old_name == 'l':
                    list_instances()
                    duplicate_instance()
                    main()
                elif old_name == 'c':
                    main()
                elif old_name == '.DS_Store':
                    print("I work with Minecraft instances, not with this Apple related shit. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                    old_name = input()
                else:
                    print("The instance with such name does not exist. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                    old_name = input()

        print("Enter the name of the duplicate (without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
        new_name = input()
        while (os.path.exists(instances_directory + new_name)
                or new_name == 'l' or new_name == 'c'
                or new_name == '.DS_Store'):
            if new_name == '':
                print("The name of the instance cannot be blank. Try again (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
                new_name = input()
            elif new_name == 'l':
                list_instances()
                new_name = 'is being choosed already'
                duplicate_instance()
                main()
            elif new_name == 'c':
                new_name = ''
                main()
            elif new_name == '.DS_Store':
                print("Are you kidding me? Just choose a normal name (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
                new_name = input()
            elif new_name == old_name:
                print("You cannot use the same name for the duplicate. Choose another name please (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
                new_name = input()
            else:
                print("An instance with the same name already exists. Choose another name please (type_without_spaces) (type 'l' to list available instances, or 'c' to cancel): ", end='')
                new_name = input()
                
        shutil.copytree(instances_directory + old_name, instances_directory + new_name)
        print('The duplicate of "{}" named "{}" was successfully created.'.format(old_name, new_name))
    else:
        print('No available instances found.')
def delete_instance(action, action_2nd_form):
    if len(os.listdir(instances_directory)) > 0:
        print("Enter the name of the instance you want to {} (type 'l' to list available instances, or 'c' to cancel): ".format(action), end='')
        instance_name = input()
        while (not os.path.exists(instances_directory + instance_name)
                or instance_name == '' or instance_name == 'l'
                or instance_name == 'c' or instance_name == '.DS_Store'):
            if instance_name == 'l':
                list_instances()
                delete_instance(action, action_2nd_form)
                main()
            elif instance_name == 'c':
                main()
            elif instance_name == '.DS_Store':
                print("I work with Minecraft instances, not with this Apple related shit. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                instance_name = input()
            else:
                print("The instance with such name does not exist. Try again (type 'l' to list available instances, or 'c' to cancel): ", end='')
                instance_name = input()

        was_active = False
        if os.path.exists(minecraft_directory):
            if os.path.islink(minecraft_directory):
                if instance_name == os.path.split(os.readlink(minecraft_directory))[1]:
                    os.unlink(minecraft_directory)
                    was_active = True

        shutil.rmtree(instances_directory + instance_name)

        if action == 'reset':
            create_instance(instance_name)
            if was_active:
                os.symlink(instances_directory + instance_name, minecraft_directory)

        print('The instance "{}" was {} successfully.'.format(instance_name, action_2nd_form))
    else:
        print('No available instances found.')
def menu():
    print('\nMenu: ')
    print('* Display this menu (m)')
    print('* List available instances (l)')
    print('* Select instance (s)')
    print('* Unselect instance (u)')
    print('* Create instance (c)')
    print('* Rename instance (r)')
    print('* Duplicate instance (d)')
    print('* Reset instance (R) - DANGER ZONE!!!')
    print('* Delete instance (D) - DANGER ZONE!!!')
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
        create_instance('')
    elif action == 'r':
        rename_instance()
    elif action == 'd':
        duplicate_instance()
    elif action == 'R':
        delete_instance('reset', 'reset')
    elif action == 'D':
        delete_instance('delete', 'deleted')
    elif action == 'q':
        sys.exit(0)

    else:
        print('Invalid input.')
    main()

menu()
main()
