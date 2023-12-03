'''
Manages installation of server install script, server JAR and inital setup
'''
import sys
import os
from colorama import Fore, Style
import plugin_manager
import install_server
from utils import choice

global COMMAND_HIERARCHY
COMMAND_HIERARCHY = {}


def chelp():
    print(Fore.WHITE + Style.BRIGHT + "Commands:" + Style.RESET_ALL)
    for c in COMMAND_HIERARCHY.items():
        name = str(COMMAND_HIERARCHY[c].name)
        description = str(COMMAND_HIERARCHY[c].description)
        print(
            Fore.GREEN + name,
            Fore.WHITE + "-",
            Fore.YELLOW + description,
        )


class Command:

    def __init__(self, name: str, bind, description: str, args=None, alias: list = None):
        self.name = name
        self.action = bind
        self.description = description
        self.args = args
        self.alias = alias

    def execute(self, ref=None):
        if ref:
            self.action(ref)
        else:
            if self.args is None:
                self.action()
            else:
                self.action(self.args)


print(__name__)
if __name__ == "__main__":

    os.chdir(os.path.abspath(os.path.dirname(sys.executable)))
    print(os.path.abspath(os.path.dirname(sys.executable)))
    if not os.path.exists("plugins"):
        files = os.listdir()
        if len(files) > 1:
            print(f"{Fore.RED}Directory must be empty!{Style.RESET_ALL}")
            input("Press enter to exit...")
            sys.exit()
        else:
            if (choice(f"Do you want to create the server in this directory? ({os.getcwd()})", ["Yes", "No"]) == "Yes"):
                install_server.install_server()
            else:
                print("Please put this program in the directory you want to create the server in")
                sys.exit()

    root_dir = os.getcwd()
    plugin_manager.set_root(root_dir)
    COMMAND_HIERARCHY = {
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
    }
    command_list = {}
    print(COMMAND_HIERARCHY.values())
    for command in COMMAND_HIERARCHY.values():
        command_list[command.name] = command
        for a in command.alias:
            command_list[a] = command

    while True:

        user_input = input(Fore.GREEN + ">>> " + Style.RESET_ALL)
        if "plugin" in user_input and len(user_input.split(" ")) > 2:
            query = user_input.split(" ")[-1]
            user_input = user_input.replace(query, "")
        user_input = user_input.lower().rstrip()
        if user_input in command_list:
            if command_list[user_input].action is not None:
                command_list[user_input].execute(query)
            else:
                print(Fore.RED + "Command not set" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Command not found" + Style.RESET_ALL)
