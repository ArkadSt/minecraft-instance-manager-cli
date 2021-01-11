# minecraft-instance-manager-cli
This is the cli version of **minecraft-instance-manager**. **minecraft-instance-manager** makes possible to have multiple instances of Minecraft with their own set of mods, resourcepacks, etc.

### List of contributors
Tomás Henrique Strotsjak Barata - helped me in testing this program on it's early stage of development.  
ra1nlox - ported everything to click library, which resulted in cleaner code and nice command line interface

## Dependencies
minecraft-instance-manager-cli needs **click** package in order to work.  
It can be easily installed by performing `pip install click`

## Launch
You need Python3 (https://www.python.org/downloads/) in order to run this program.
If you have installed Python3, you can run the program by executing this command in console. That will display the help page:

```
Linux, MacOS: python3 minecraft-im.py
Windows:      python minecraft-im.py
```

***NB! On Windows this program requires administrative priveleges because on Windows only administrators can create symlinks. It is recommended to run this program from admin console.***

Program is intended to be run with commands, listed on the help page. Most of the commands require 1 or 2 arguments, depending on the task.

## How does this program work

The selected instance folder is used as a Minecraft folder.
Minecraft folder is stored here:

```
Windows:    %appdata%\.minecraft
Linux:      ~/.minecraft
MacOS:      ~/Library/Application Support/minecraft
```

Minecraft folder is a symlink that is targeted at the selected instance folder.

## How to manage Minecraft instances
Instance folder can be managed just like a normal Minecraft folder.
Minecraft instances are stored here:

```
Windows:    %appdata%\.minecraft-instance-manager\instances
Linux:      ~/.minecraft-instance-manager/instances
MacOS:      ~/Library/Application Support/minecraft-instance-manager/instances
```
*On MacOS you can access `~/Library/Application Support/` using Spotlight. Just type `~/Library/Application Support/` into the prompt*

After creating, the instance folder already has such folders as `mods`, `resourcepacks`, `saves`.
Install everything you need there.

By modifying the Minecraft folder you modify the working Minecraft instance. The working instance can be choosed using **minecraft-instance-manager**. Instance folders can be created and deleted using **minecraft-instance-manager** or manually as well. My utility just makes it easier (I hope).

___
*P.S. **minecraft-instance-manager** adds `instance_name.mp3` in the root of the created instance folder, which is only needed for indication of the working instance if you go directly to Minecraft folder for example. It is safe to be removed if you don't want it there.*
