
# YOUR PROJECT TITLE
###Video Demo:  <https://youtu.be/qC2HDNDb-4Y>
#### Description:
*CS50 Final Project*

Install a Minecraft server like magic!
Only available for Windows, stay tuned for Linux distribution.
### Installation

1. Download the `.exe` from the releases tab.
2. Run it in an empty directory.
3. Follow the instructions to install!

**If the installer throws an error or closes randomly/on open:**

 - Doubble check your directory is empy! Hidden files included!

 - Run the program as an administrator

 - Move your directory out of the root of your drive.

 - For older machines, try running in compatibility mode for your given version.

### Using the tool

Once the server is installed you can run `help` to see a list of commands;
```
help - Shows this help message
start - Starts the server
update plugins - Updates all plugins
install plugin - Installs a plugin
list plugins - Lists all plugins
create backup - Creates a backup of your server files
clear - Clears the console
delete plugin - Deletes selected plugins
exit - Exits the program
disable plugin - Disables/enables a plugin
```

### Building from Source

Dowmload the source code.
Run the `./build.ps1` file.
Arguments:
 - `-clean` : deletes all files in the `/dist` directory before building
 - `-test` : runs the `.exe` after building.

The script will then build the `.exe` in the `/dist` directory.
