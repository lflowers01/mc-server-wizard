''' defines commands and their actions '''
import sys
from main import Command, chelp, install_server, plugin_manager, root_dir

command_hierarchy = {
    "help": Command(name="help", description="Shows this help message", bind=chelp),
    "start": Command(
        name="start",
        description="Starts the server",
        bind=install_server.run_server,
        args=f"{root_dir}/start.cmd",
    ),
    "update plugins": Command(
        name="update plugins",
        description="Updates all plugins",
        bind=plugin_manager.update_plugin_yml,
        args=f"{root_dir}/plugins",
        alias=["update plugin", "plugin update", "plugins update"],
    ),
    "update jar": Command(
        name="update jar",
        description="Updates the server jar",
        bind=None,
        alias=["jar update"],
    ),
    "install plugin": Command(
        name="install plugin",
        description="Installs a plugin",
        bind=plugin_manager.plugin_install_process,
    ),
    "create backup": Command(
        name="create backup",
        description="Creates a backup of your server files",
        bind=None,
        alias=["backup create", "make backup", "backup make"],
    ),
    "clear": Command(
        name="clear",
        description="Clears the console",
        bind=install_server.cls,
        alias=["cls"],
    ),
    "delete plugin": Command(
        name="delete plugin",
        description="Deletes selected plugins",
        bind=None,
        alias=["plugin delete", "delete plugins", "plugins delete"],
    ),
    "disable plugin": Command(
        name="disable plugin",
        description="Disables selected plugins",
        bind=None,
        alias=["plugin disable", "disable plugins", "plugins disable"],
    ),
    "enable plugin": Command(
        name="enable plugin",
        description="Enables selected plugins",
        bind=None,
        alias=["plugin enable", "enable plugins", "plugins enable"],
    ),
    "list plugins": Command(
        name="list plugins",
        description="Lists all plugins",
        bind=None,
        alias=["plugins list", "list plugin"],
    ),
    "exit": Command(name="exit", description="Exits the program", bind=sys.exit),
}
