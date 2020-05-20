# minecraft_instance_manager
This program makes possible to have multiple instances of Minecraft with their own set of mods, resourcepacks, etc.

*Special thanks to my friend, Tomás Henrique Strotsjak Barata, who helped me in testing this software.*


## Launch

You need Python3 (https://www.python.org/downloads/) in order to run this program.
If you have installed Python3, you can run the program by executing this command in console:

`python minecraft_instance_manager-x.x.x.py`

***NB! On Windows this program requires administrative priveleges.
The recommended way of executing this program on Windows is
to double click on `minecraft_instance_manager-x.x.x.py`.***


## How does this program work

The selected instance folder is used as a Minecraft (`.minecraft`) folder.

```
Windows:    %appdata%\.minecraft
Linux:      ~/.minecraft
```

`.minecraft` folder is a symlink that is targeted at the selected instance folder.


## How to manage Minecraft instances

Instance folder can be managed just like a normal Minecraft ('.minecraft') folder
Minecraft instances are stored here:

```
Windows:    %appdata%\.minecraft_instance_manager\instances
Linux:      ~/.minecraft_instance_manager
```

After creating the instance folder already has such folders as `mods`, `resourcepacks`, `saves`.
Install everything you need there.

By modifying `%appdata%\.minecraft` on Windows or `~/.minecraft` on Linux you modify the default Minecraft instance.
Instance folders can be created and deleted manually as well. My utility just makes it easier (I hope).
