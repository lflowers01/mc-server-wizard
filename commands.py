import plugin_manager
import os
from colorama import Fore, Style
import main


def help():
    print(Fore.WHITE + Style.BRIGHT + "Commands:" + Style.RESET_ALL)
    for command in command_list:
        name = str(command_list[command].name)
        description = str(command_list[command].description)
        print(
            Fore.GREEN + name,
            Fore.WHITE + "-",
            Fore.YELLOW + description,
        )


class Command:
    def __init__(self, name: str, bind, description: str, args: list = None):
        self.name = name
        self.action = bind
        self.description = description
        self.args = args

    def execute(self):
        if self.args == None:
            self.action()
        else:
            self.action(self.args)


if __name__ == "__main__":
    command_list = {
        "help": Command(name="help", description="Shows this help message", bind=help),
        "start": Command(
            name="start",
            description="Starts the server",
            bind=main.run_server,
            args=["start.cmd"],
        ),
        "update plugins": Command(
            "update plugins",
            "Updates all plugins",
            plugin_manager.update_plugin_yml,
            args=["mcserver/plugin_data"],
        ),
        "update jar": Command("update jar", "Updates the server jar", None),
        "install plugin": Command(
            "install plugin",
            "Installs a plugin",
            plugin_manager.plugin_install_process,
        ),
        "create backup": Command(
            "create backup", "Creates a backup of your server files", None
        ),
        "clear": Command("clear", "Clears the console", main.cls),
    }

    while True:
        command = input(Fore.GREEN + ">>> " + Style.RESET_ALL)
        if command in command_list:
            command_list[command].execute()
        else:
            print(Fore.RED + "Command not found" + Style.RESET_ALL)
