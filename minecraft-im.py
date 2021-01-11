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
minecraft_instance_manager_directory = minecraft_parent_directory + 'minecraft-instance-manager/'
instances_directory = minecraft_instance_manager_directory + 'instances/'

# Needed in order to reactivate the reset instance if it was activated before
was_active = False 

# Checking for existing minecraft and minecraft-instance-manager folders
if not os.path.exists(minecraft_instance_manager_directory):
    os.mkdir(minecraft_instance_manager_directory)
if not os.path.exists(instances_directory):
    os.mkdir(instances_directory)

# Function to view list
@cli.command()
def list_instances():
    # if there is at least 1 instance
    if len(os.listdir(instances_directory)) > 0:
        # for instance name print instance name with cute view
        for instance in os.listdir(instances_directory):
            if instance == '.DS_Store':
                continue
            if os.path.exists(minecraft_directory):
                if os.path.islink(minecraft_directory):
                    if instance == os.path.split(os.readlink(minecraft_directory))[1]:
                        print('*' + instance)
                        continue
            print(' ' + instance)
    else:
        print('No available instances found.')

@cli.command()
@click.argument("instance")
def activate_instance(instance):
    # if the instance with such name exists
    if os.path.exists(instances_directory + instance):
        if instance != '.DS_Store':
            # if path of minecraft exist
            if os.path.exists(minecraft_directory):
                # if minecraft directory is a link, then
                if os.path.islink(minecraft_directory):
                    os.unlink(minecraft_directory)
            else:
                try:
                    os.stat(minecraft_directory)
                except OSError:
                    try:
                        os.remove(minecraft_directory)
                    except FileNotFoundError:
                        pass
            try:
                os.symlink(instances_directory + instance, minecraft_directory)
                print(f'The instance "{instance}" was activated successfully.')
            except FileExistsError:
                print(f'Seems like you have an existing Minecraft folder "{minecraft_directory}". It needs to be deleted or moved first.')
        else:
            print('Are you on drugs?')
    else:
        print(f'The instance "{instance}" doesn\'t exist.')

@cli.command()
def deactivate_instance():
    if os.path.exists(minecraft_directory) and os.path.islink(minecraft_directory):
        instance = os.path.split(os.readlink(minecraft_directory))[1]
        os.unlink(minecraft_directory)
        print(f'The instance "{instance}" was successfully deactivated.')
    else:
        print('No active instances.')

def create_instance_universal(instance):
    if instance == '.DS_Store':
        print('Go find a job.')
        exit(1)
    if os.path.exists(instances_directory + instance):
        print(f'The instance "{instance}" already exists')
        exit(1)

    # Create main instance folder
    os.mkdir(instances_directory + instance)
    # Create subfolders
    os.mkdir(instances_directory + instance + '/mods')
    os.mkdir(instances_directory + instance + '/resourcepacks')
    os.mkdir(instances_directory + instance + '/saves')

    # Not necessary, just for indication purposes
    Path(instances_directory + instance + '/' + instance + '.mp3').touch()


def delete_instance_universal(instance):
    if not os.path.exists(instances_directory + instance):
        print(f'The instance "{instance}" doesn\'t exist.')
        exit(1)
    if instance == '.DS_Store':
        print("What's wrong with you?")
        exit(1)

    global was_active
    was_active = False
    if os.path.exists(minecraft_directory):
        if os.path.islink(minecraft_directory):
            if instance == os.path.split(os.readlink(minecraft_directory))[1]:
                os.unlink(minecraft_directory)
                was_active = True

    shutil.rmtree(instances_directory + instance)

@cli.command()
@click.argument("instance")
def create_instance(instance):
    create_instance_universal(instance)
    print(f'The instance "{instance}" was created successfully.')

@cli.command()
@click.argument("instance")
def delete_instance(instance):
    delete_instance_universal(instance)
    print(f'The instance "{instance}" was deleted successfully.')

@cli.command()
@click.argument("instance")
@click.argument("new_instance_name")
def rename_instance(instance, new_instance_name):
    if os.path.exists(instances_directory + instance):
        if not os.path.exists(instances_directory + new_instance_name):
            was_active = False
            if os.path.exists(minecraft_directory):
                if os.path.islink(minecraft_directory):
                    if instance == os.path.split(os.readlink(minecraft_directory))[1]:
                        os.unlink(minecraft_directory)
                        was_active = True

            os.rename(instances_directory + instance, instances_directory + new_instance_name)

            if was_active:
                os.symlink(instances_directory + new_instance_name, minecraft_directory)

            print(f'Instance "{instance}" was successfully renamed to "{new_instance_name}".')
        else:
            print(f'The instance "{new_instance_name}" already exists')
    else:
        print(f'The instance "{instance}" doesn\'t exist')

@cli.command()
@click.argument("instance")
def reset_instance(instance):
    delete_instance_universal(instance)
    create_instance_universal(instance)

    if was_active:
        os.symlink(instances_directory + instance, minecraft_directory)
    print(f'The instance "{instance}" was reset successfully.')

@cli.command()
@click.argument("instance")
@click.argument("duplicate")
def duplicate_instance(instance, duplicate):
    if os.path.exists(instances_directory + instance):
        if not os.path.exists(instances_directory + duplicate):
            shutil.copytree(instances_directory + instance, instances_directory + duplicate)
            print(f'The duplicate of "{instance}" named "{duplicate}" was successfully created.')
        else:
            print(f'The instance "{duplicate}" already exists')
    else:
        print(f'The instance "{instance}" doesn\'t exist')

if __name__ == '__main__':
    cli()
