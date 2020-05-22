# minecraft_instance_manager
This program makes possible to have multiple instances of Minecraft with their own set of mods, resourcepacks, etc.

*Special thanks to my friend, Tomás Henrique Strotsjak Barata, who has helped me in testing this software.*


## Launch

You need Python3 (https://www.python.org/downloads/) in order to run this program.
If you have installed Python3, you can run the program by executing this command in console:

`python minecraft_instance_manager.py`

***NB! On Windows this program requires administrative priveleges because on Windows only administrator can create symlinks.
The easiest way of executing this program on Windows is to double click on `minecraft_instance_manager.py` and then User Account Control (UAC) will appear.***


## How does this program work

The selected instance folder is used as a Minecraft (`.minecraft`) folder.

```
Windows:    %appdata%\.minecraft
Linux:      ~/.minecraft
MacOS:      ~/Library/Application Support/minecraft
```

`.minecraft` folder is a symlink that is targeted at the selected instance folder.


## How to manage Minecraft instances

Instance folder can be managed just like a normal Minecraft ('.minecraft') folder.
Minecraft instances are stored here:

```
Windows:    %appdata%\.minecraft_instance_manager\instances
Linux:      ~/.minecraft_instance_manager/instances
MacOS:      ~/Library/Application Support/minecraft_instance_manager/instances
```
*If you're a Mac user, you can open the folder through Spotlight:*
*1. Press 'Command'+'Space' or open the Spotlight popup through the magnifying glass icon in the right of the Menu Bar.*
*2. Type ~/Library/Application Support/minecraft and hit 'Enter'.*

After creating the instance folder already has such folders as `mods`, `resourcepacks`, `saves`.
Install everything you need there.

By modifying `.minecraft` you modify the working Minecraft instance. The working instance can be choosed using **minecraft_instance_manager**. Instance folders can be created and deleted using **minecraft_instance_manager** or manually as well. My utility just makes it easier (I hope).

## Backups
If **minecraft_instance_manager** sees that `.minecraft` is not a symlink but a normal folder, it will offer you to make a backup. Backups created by the program are stored here:

```
Windows:    %appdata%\.minecraft_instance_manager\backups
Linux:      ~/.minecraft_instance_manager/backups
MacOS:      ~/Library/Application Support/minecraft_instance_manager/backups
```


___
*P.S. **minecraft_instance_manager** adds `instance_name.mp3` in the root of the created instance folder, which is only needed for indication of the working instance if you go directly to `.minecraft` for example. It is safe to be removed if you don't want it there.*
