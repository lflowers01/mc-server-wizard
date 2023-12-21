import sys
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import FormattedText

from colorama import Fore, Style
import plugin_manager
import install_server
from utils import choice

global COMMAND_HIERARCHY
COMMAND_HIERARCHY = {}
command_list = {}


def quit_program():
    sys.exit()


def chelp():
    print(Fore.WHITE + Style.BRIGHT + "Commands:" + Style.RESET_ALL)
    for c in COMMAND_HIERARCHY.items():
        name = str(COMMAND_HIERARCHY[c[0]].name)
        description = str(COMMAND_HIERARCHY[c[0]].description)
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
        if self.name == "install plugin" or self.name == "delete plugin" or self.name == "disable plugin":
            if ref is None or ref == "":
                print(f"{Fore.RED}Please specify a plugin name{Style.RESET_ALL}")
                return
            self.args = ref
        if self.args is None:
            self.action()
        else:
            self.action(self.args)


def completer(text, state):
    options = [i for i in command_list if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None


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
            if choice(f"Do you want to create the server in this directory? ({os.getcwd()})", ["Yes", "No"]) == "Yes":
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
        "install plugin": Command(
            name="install plugin",
            description="Installs a plugin",
            bind=plugin_manager.plugin_install_process,
        ),
        "list plugins": Command(
            name="list plugins",
            description="Lists all plugins",
            bind=plugin_manager.list_plugins,
            alias=["plugins list", "list plugin", "plugin list"],
        ),
        "create backup": Command(
            name="create backup",
            description="Creates a backup of your server files",
            bind=install_server.create_backup,
            alias=["backup create", "make backup", "backup make", "backup"],
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
            bind=plugin_manager.delete_plugin,
            alias=["plugin delete", "delete plugins", "plugins delete"],
        ),
        "exit": Command(
            name="exit",
            description="Exits the program",
            bind=quit_program,
            alias=["quit"],
        ),
        "disable plugin": Command(
            name="disable plugin",
            description="Disables/enables a plugin",
            bind=plugin_manager.disable_plugin,
            alias=["plugin disable", "disable plugins", "plugins disable", "plugin enable", "enable plugin", "enable plugins", "plugins enable"],
        ),
    }
    for command in COMMAND_HIERARCHY.values():
        command_list[command.name] = command
        if command.alias is not None:
            for a in command.alias:
                command_list[a] = command

    completer = WordCompleter(COMMAND_HIERARCHY, ignore_case=True)

    while True:
        query = None
        user_input = prompt(FormattedText([('fg:ansiblue', '>>> ')]), completer=completer)
        if "plugin" in user_input and len(user_input.split(" ")) > 2:
            query = user_input.split(" ")[-1]
            user_input = user_input.replace(query, "")
        user_input = user_input.lower().rstrip()
        if user_input in command_list:
            if command_list[user_input].action is not None:
                if query is None:
                    command_list[user_input].execute()
                else:
                    command_list[user_input].execute(query)
            else:
                print(Fore.RED + "Command not set" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Command not found" + Style.RESET_ALL)
