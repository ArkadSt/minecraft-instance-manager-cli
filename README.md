# minecraft_instance_manager
This program makes possible to have multiple instances of Minecraft with their own set of mods, resourcepacks, etc.

*Special thanks to my friend, Tomás Henrique Strotsjak Barata, who has helped me in testing this software.*\
*Updated by rain*
## Launch

You need Python3 (https://www.python.org/downloads/) in order to run this program.
If you have installed Python3, you can run the program by executing this command in console:

```
Linux, MacOS: python3 minecraft_instance_manager.py
Windows:      python minecraft_instance_manager.py
```

***Only for Windows***\
Also, you can download release from github, place ".exe" file in folder on your C: disk to use it from cmd everywhere!

***NB! On Windows this program requires administrative priveleges because on Windows only administrator can create symlinks.
The easiest way of executing this program on Windows is to open `minecraft_instance_manager.py` in the cmd and then User Account Control (UAC) will appear.***

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
Windows:    %appdata%\.minecraft_instance_manager\instances
Linux:      ~/.minecraft_instance_manager/instances
MacOS:      ~/Library/Application Support/minecraft_instance_manager/instances
```
*On MacOS you can access `~/Library/Application Support/` using Spotlight. Just type `~/Library/Application Support/` into the prompt*

After creating, the instance folder already has such folders as `mods`, `resourcepacks`, `saves`.
Install everything you need there.

By modifying the Minecraft folder you modify the working Minecraft instance. The working instance can be choosed using **minecraft_instance_manager**. Instance folders can be created and deleted using **minecraft_instance_manager** or manually as well. My utility just makes it easier (I hope).

___
*P.S. **minecraft_instance_manager** adds `instance_name.mp3` in the root of the created instance folder, which is only needed for indication of the working instance if you go directly to Minecraft folder for example. It is safe to be removed if you don't want it there.*
