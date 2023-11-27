'''
Manages installation of server install script, server JAR and inital setup
'''
import sys
import os
from colorama import Fore, Style
import plugin_manager
from command_hierarchy import command_hierarchy
import install_server
from utils import choice


def chelp():
    print(Fore.WHITE + Style.BRIGHT + "Commands:" + Style.RESET_ALL)
    for c in command_hierarchy.items():
        name = str(command_hierarchy[c].name)
        description = str(command_hierarchy[c].description)
        print(
            Fore.GREEN + name,
            Fore.WHITE + "-",
            Fore.YELLOW + description,
        )


class Command:

    def __init__(self,
                 name: str,
                 bind,
                 description: str,
                 args=None,
                 alias: list = None):
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
            if (choice(
                    f"Do you want to create the server in this directory? ({os.getcwd()})",
                ["Yes", "No"],
            ) == "Yes"):
                install_server.install_server()
            else:
                print(
                    "Please put this program in the directory you want to create the server in"
                )
                sys.exit()

    root_dir = os.getcwd()
    plugin_manager.set_root(root_dir)
    command_list = {}
    for command in command_hierarchy.values():
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
