import plugin_manager
import os
from colorama import Fore, Style
import install_server
from utils import *
import sys


os.chdir(os.path.abspath(os.path.dirname(sys.executable)))
print(os.path.abspath(os.path.dirname(sys.executable)))
if not os.path.exists("plugins"):
    files = os.listdir()
    if len(files) > 1:
        print(f"{Fore.RED}Directory must be empty!{Style.RESET_ALL}")
        input("Press enter to exit...")
        sys.exit()
    else:
        if (
            choice(
                f"Do you want to create the server in this directory? ({os.getcwd()})",
                ["Yes", "No"],
            )
            == "Yes"
        ):
            install_server.install_server()
        else:
            print(
                "Please put this program in the directory you want to create the server in"
            )
            sys.exit()

global root_dir
root_dir = os.getcwd()
plugin_manager.set_root(root_dir)


def help():
    print(Fore.WHITE + Style.BRIGHT + "Commands:" + Style.RESET_ALL)
    for command in command_hierarchy:
        name = str(command_hierarchy[command].name)
        description = str(command_hierarchy[command].description)
        print(
            Fore.GREEN + name,
            Fore.WHITE + "-",
            Fore.YELLOW + description,
        )


class Command:
    def __init__(self, name: str, bind, description: str, args=None, alias: list = []):
        self.name = name
        self.action = bind
        self.description = description
        self.args = args
        self.alias = alias

    def execute(self, ref=None):
        if ref:
            self.action(ref)
        else:
            if self.args == None:
                self.action()
            else:
                self.action(self.args)


if __name__ == "__main__":
    command_hierarchy = {
        "help": Command(name="help", description="Shows this help message", bind=help),
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

    command_list = {}
    for command in command_hierarchy.values():
        command_list[command.name] = command
        for alias in command.alias:
            command_list[alias] = command

    while True:
        user_input = input(Fore.GREEN + ">>> " + Style.RESET_ALL)
        ref = None
        if "plugin" in user_input and len(user_input.split(" ")) > 2:
            ref = user_input.split(" ")[-1]
            user_input = user_input.replace(ref, "")
            print(f"user input modified to {user_input}, ref set to {ref}")
        user_input = user_input.lower().rstrip()
        if user_input in command_list:
            if command_list[user_input].action != None:
                command_list[user_input].execute(ref)
            else:
                print(Fore.RED + "Command not set" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Command not found" + Style.RESET_ALL)
