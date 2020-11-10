# Hi, i maked this mod for your program to use it directly from cmd, thanks!

import os
import platform
import shutil
import sys
import ctypes
import click
import configparser
from pathlib import Path

# funtion for click
@click.group()
def cli():
    pass

# Checking the name of os for creating a folder for minecraft_instance_manager and minecraft_parent_directory
if platform.system() == 'Linux':
    minecraft_parent_directory = os.getenv('HOME') + '/.'
elif platform.system() == 'Darwin':
    minecraft_parent_directory = os.getenv('HOME') + '/Library/Application Support/'
elif platform.system() == 'Windows':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    minecraft_parent_directory = os.getenv('APPDATA') + '\\.'

# Variables for paths
minecraft_directory = minecraft_parent_directory + 'minecraft'
minecraft_instance_manager_directory = minecraft_parent_directory + 'minecraft_instance_manager/'
instances_directory = minecraft_instance_manager_directory + 'instances/'
backups_directory = minecraft_instance_manager_directory + 'backups/'

# Checking for existing minecraft folders and minecraft instance manager
if not os.path.exists(minecraft_instance_manager_directory):
    os.mkdir(minecraft_instance_manager_directory)
if not os.path.exists(instances_directory):
    os.mkdir(instances_directory)

# Function to view list
@cli.command()
def list_instances():
    # if instances_directory exist, i guess
    if len(os.listdir(instances_directory)) > 0:
        # for instance name print instance name with cute view
        for instance_name in os.listdir(instances_directory):
            print(' ' + instance_name, end='')
            if os.path.exists(minecraft_directory):
                # if minecraft directory path exist try reading link and add "active" to instance
                try:
                    if instance_name == os.path.split(os.readlink(minecraft_directory))[1]:
                        print(' (active)', end='')
                except OSError:
                    pass
            print()
    else:
        print('No available instances found.')

@cli.command()
@click.argument("instance")
def select_instance(instance):
    # if instances directory exist, then
    if len(os.listdir(instances_directory)) > 0:
        # if path of minecraft exist
        if os.path.exists(minecraft_directory):
            # if minecraft directory is not a link, then
            if not os.path.islink(minecraft_directory):
                # if backups directory not exist, then
                if not os.path.exists(backups_directory):
                    # create dir with backups
                    os.mkdir(backups_directory)

                # backup name seted to "minecraft.backup"
                backup_name = 'minecraft.backup'
                index = 1
                # while backup exist, index++
                while os.path.exists(backups_directory + backup_name):
                    backup_name = 'minecraft.backup({})'.format(str(index))
                    index += 1
                print(f'\nSeems like you have an existing Minecraft folder {minecraft_directory}. It needs to be deleted, backuped or moved first.\n')

        else:
            try:
                os.stat(minecraft_directory)
            except OSError:
                try:
                    os.remove(minecraft_directory)
                except FileNotFoundError:
                    pass

        instance_name = instance

        if os.path.exists(minecraft_directory):
            if os.path.islink(minecraft_directory):
                os.unlink(minecraft_directory)
        os.symlink(instances_directory + instance_name, minecraft_directory)
        print('The instance "' + instance_name + '" was selected successfully.')
    else:
        print('No available instances found.')

@cli.command()
@click.argument("instance")
def unselect_instance(instance):
    if os.path.exists(minecraft_directory) and os.path.islink(minecraft_directory):
        instance_name = os.path.split(os.readlink(minecraft_directory))[1]
        os.unlink(minecraft_directory)
        print(f'The instance {instance_name} was successfully unselected.')
    else:
        print('None of the instances are selected.')

@cli.command()
@click.argument("instance")
def create_instance(instance):
    instance_name = instance

    while os.path.exists(instances_directory + instance_name):
        if instance_name == '':
            print("The name of the instance cannot be blank. Try again (type_without_spaces) (type 'list_instances' to list available instances)")
        else:
            print('An instance with the same name already exists. Choose another name')

    os.mkdir(instances_directory + instance_name)
    os.mkdir(instances_directory + instance_name + '/mods')
    os.mkdir(instances_directory + instance_name + '/resourcepacks')
    os.mkdir(instances_directory + instance_name + '/saves')

    # Not necessary, just for indication purposes
    Path(instances_directory + instance_name + '/' + instance_name + '.mp3').touch()

@cli.command()
@click.argument("instance")
@click.argument("new_name")
def rename_instance(instance, new_name):
    if len(os.listdir(instances_directory)) > 0:
        was_active = False
        if os.path.exists(minecraft_directory):
            if os.path.islink(minecraft_directory):
                if instance == os.path.split(os.readlink(minecraft_directory))[1]:
                    os.unlink(minecraft_directory)
                    was_active = True
        try:
            os.rename(instances_directory + instance, instances_directory + new_name)
            if was_active:
                os.symlink(instances_directory + new_name, minecraft_directory)
                print(f'Instance "{instance}" was successfully renamed to "{new_name}".')
            else:
                print('No available instances found.')
        except FileNotFoundError:
            print('No such instance, change name and try again type (type "list-instances" to list available instances)')

@cli.command()
@click.argument("instance")
def delete_instance(instance):
    if len(os.listdir(instances_directory)) > 0:
        instance_name = instance
        while not os.path.exists(instances_directory + instance_name):
            print("The instance with such name does not exist. Try again (type 'list-instances' to list available instances)")

        was_active = False
        if os.path.exists(minecraft_directory):
            if os.path.islink(minecraft_directory):
                if instance_name == os.path.split(os.readlink(minecraft_directory))[1]:
                    os.unlink(minecraft_directory)
                    was_active = True

        shutil.rmtree(instances_directory + instance_name)

        print(f'The instance "{instance}" was deleted successfully.')
    else:
        print('No available instances found.')

if __name__ == '__main__':
    cli()