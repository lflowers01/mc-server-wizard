from __future__ import print_function, unicode_literals
import inquirer
from inquirer import *
from colorama import Fore, Style, Back
from downloads import *
from tqdm import tqdm
import subprocess
import os
import platform
from time import sleep
import stat 
from urllib.parse import urlparse
import pylnk3
import fetch_versions
import win32com.client
import plugin_manager
from utils import *
global main_dir



def main():    
    cls()
    print(Fore.YELLOW + Style.BRIGHT + "Welcome to the Minecraft Server Installer!" + Style.RESET_ALL)
    print("This installer will guide you through the process of installing a Minecraft server.")
    next_step("Directory Settings", 1, 4, False)
    version = None
    main_dir = None
    while main_dir == None:
        main_dir = text("Enter the name of the directory you want to install the server in (will create a folder with the given name)")
        if ' ' in main_dir:
            print(Fore.RED + "Directory name cannot contain spaces!" + Style.RESET_ALL)
            main_dir = None
        else:
            try:
                os.mkdir(main_dir)
            except:
                print(Fore.RED + "ERROR: Directory already exists! (or invalid name)" + Style.RESET_ALL)
                main_dir = None
    print(Fore.GREEN + f"Directory: {Fore.WHITE}{main_dir}{Fore.GREEN} created successfully" + Style.RESET_ALL)
    while version == None:
        version = text("Enter the version of the server you want to install (1.XX.XX)")
        print(version, check_valid_version(version))
        if len(version.split(".")) != 3 or not check_valid_version(version):
            print(Fore.RED + f"Invalid version! {Fore.WHITE}(1.XX.XX)" + Style.RESET_ALL)
            version = None;
    inter_version = get_intermidiate_version(version)
    legacy = False
    if inter_version < 13:
        legacy = True
        print(Fore.RED + Style.BRIGHT + f"WARNING: Version {version} may not work with this tool! Proceed with cation!" + Style.RESET_ALL)
    if inter_version < 18:
        target_java = 8
    else: 
        target_java = 17
    print(target_java)
    jar_select = None
    print(Fore.GREEN + f"Version: {Fore.WHITE}{version}{Fore.GREEN} selected" + Style.RESET_ALL)
    next_step("JAR/Java Setup", 2, 4)
    while jar_select == None:
        if legacy:
            print(Fore.RED + Style.BRIGHT + "WARNING: Manual install is recomended with older versions." + Style.RESET_ALL)
        if choice("Do you want to install your JAR manualy or automatically?", ["Automatic", "Manual"], "Automatic") == "Automatic":
            jar_select = choice("Select server JAR to install:", fetch_versions.supported_types, "Paper")
            print(Fore.CYAN + f"Downloading {jar_select}..." + Style.RESET_ALL)
            try:
                link = fetch_versions.fetch_link(version, jar_select)
                download_file(link, f"{main_dir}\server.jar")
            except:
                print(Fore.RED + f"No {jar_select} JAR found for version {version}!{Style.RESET_ALL}")
                print(Fore.YELLOW + "Try downloading the server JAR yourself; some legacy JARs may be too old!" + Style.RESET_ALL)
                jar_select = None


        else:
            jar_select = "Manual"
            while jar_select == "Manual":
                choice(f"Download the server JAR you want to install and place it in the server directory ({main_dir}). Press enter to continue", ["OK"])
                for item in os.listdir(main_dir):
                    if item.endswith('.jar'):
                        jar_select = item
                        print(Fore.GREEN + f"Found {jar_select}!" + Style.RESET_ALL)
                        break
                os.rename(os.path.join(main_dir, jar_select), os.path.join(main_dir, 'server.jar'))
                jar_select = "server.jar"
            
    

    java_version = None
    install_java = False
    try:
        output = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
        java_version = next((line for line in output.decode('utf-8').split('\n') if 'version' in line)).split(' ')[2].replace('"', '')
        java_version = java_version.split('.')[1]
        print(f"Java version: {java_version}")
        
        if int(java_version) < target_java:
            install_java = True
    except Exception:
        install_java = True
    java_path = "java"
    if install_java:
        if choice("Java is not installed or is outdated! Do you want to install it now?", ["Yes", "No"], "Yes") == "Yes":
            if platform.system() == "Linux":
                try:
                    print(Fore.CYAN + "Downloading Java..." + Style.RESET_ALL)
                    subprocess.run(['sudo', 'apt', 'install', '-y', 'openjdk-17-jdk'], check=True)
                except Exception as e:
                    print(Fore.RED + f"ERROR: While trying to install Java 17:\n{Style.RESET_ALL}{e}")
                    print(Fore.YELLOW + "Try installing Java 17 JDK yourself" + Style.RESET_ALL)
                    return
            if platform.system() == "Windows":
                if choice("Do you want to install Java to be portable?", ["Yes", "No"], "Yes") == "No":
                    portable = 'installer'
                    install_extension = '.msi'
                else:
                    portable = 'portable'
                    install_extension = '.zip'
                print(Fore.CYAN + "Downloading Java..." + Style.RESET_ALL)
                download_file(java_install[target_java][portable][platform.system()][platform.architecture()[0]], f"{main_dir}\java{install_extension}")
                if portable == 'portable':
                    print(Fore.CYAN + "Extracting Java..." + Style.RESET_ALL)
                    subprocess.run(['tar', '-xf', f"{main_dir}\java{install_extension}", '-C', main_dir])
                    os.remove(f"{main_dir}\java{install_extension}")
                    
                    for item in os.listdir(main_dir):
                        if item.startswith('jdk'):
                            java_path = item
                            java_path = '"' + str(java_path) + "/bin/java.exe" + '"'
                            break
                    print(Fore.GREEN + f"Java installed! {Fore.WHITE}{java_path}" + Style.RESET_ALL)

                else:
                    print(Fore.CYAN + "Installing Java..." + Style.RESET_ALL)
                    subprocess.run([f"{main_dir}\java{install_extension}"], check=True)
                    os.remove(f"{main_dir}\java{install_extension}")
    
    memory = None

    next_step("Server Settings", 3, 4)
    while memory == None:
        memory = text("Enter the amount of memory you want to allocate to the server (in GB)")
        try:
            memory = int(memory)
        except:
            print(Fore.RED + "Invalid amount of memory!" + Style.RESET_ALL)
            memory = None
    if choice("Do you want to enable the GUI?", ["Yes", "No"], "No") == "Yes":
        gui = ""
    else:
        gui = "nogui"
    start_script = create_start_script(memory, main_dir, java_path, gui)
    if not start_script:
        return
    print(start_script)
    print(Fore.GREEN + "Server installation complete!" + Style.RESET_ALL)
    next_step("EULA and final steps", 4, 4)
    skip_eula = False
    if inter_version <= 7 and version != "1.7.10":
        skip_eula = True
        print(Fore.RED + Style.BRIGHT + f"WARNING: EULA is not required for this version! {Fore.WHITE}(skipping process)" + Style.RESET_ALL)
    if not skip_eula:
        print(Fore.CYAN + "Starting server..." + Style.RESET_ALL)
        os.chdir(main_dir)
        run_server(start_script)
        eula_path = os.path.join('eula.txt')
        timeout = 0
        while not os.path.isfile(eula_path):
            sleep(1)  
            timeout += 1
            if timeout > 75:
                print(Fore.RED + "ERROR: Timed out - Server failed to initialize! (Do you have the right Java version installed?)" + Style.RESET_ALL)
                return
        print(Fore.GREEN + "Server started!" + Style.RESET_ALL)

        print(Fore.CYAN + "Accepting EULA..." + Style.RESET_ALL)
        with open(eula_path, 'r+') as file:
            file_data = file.read()
            file.seek(0)
            file.write(file_data.replace('eula=false', 'eula=true'))
            file.truncate()
        print(Fore.GREEN + "EULA accepted!" + Style.RESET_ALL)
        print(jar_select)
        print(list(plugins.keys()))
    if not os.path.exists("plugins") and not jar_select == "Vanilla":
        os.mkdir("plugins")
    if jar_select != "Vanilla":
        if choice("Do you want to install plugins?", ["Yes", "No"], "Yes") == "Yes":
            p_selection = checkbox(f"Select plugins to install {Fore.YELLOW}(Space to select, enter to confirm){Style.RESET_ALL}", list(plugins.keys()))
            print(Fore.CYAN + "Installing plugins..." + Style.RESET_ALL)
            for plugin in p_selection:
                print(Fore.CYAN + f"Downloading {plugin}..." + Style.RESET_ALL)
                if is_valid_url(plugins[plugin]):
                   download_file(plugins[plugin], f"plugins\{plugin}.jar")
                else:
                    print(Fore.RED + f"ERROR: Invalid URL for {plugin}! Skipping" + Style.RESET_ALL)
            print(Fore.GREEN + "Plugins installed!" + Style.RESET_ALL)
    if platform.system() == "Windows":
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        shortcut_path = os.path.join(desktop, f"{main_dir}.lnk")
        print(shortcut_path, start_script)
        if choice("Do you want to create a desktop shortcut?", ["Yes", "No"], "Yes") == "Yes":
            print(Fore.CYAN + "Creating shortcut on your desktop..." + Style.RESET_ALL)
            create_shortcut(shortcut_path, start_script, "")
            print(Fore.GREEN + "Shortcut created!" + Style.RESET_ALL)
    run_server(start_script)
    cls()


def next_step(title:str = None, step:int = None, total_steps:int = None, clear:bool = True):
    sleep(1)
    print(f"{Fore.YELLOW + Style.BRIGHT}Press enter to continue...{Style.RESET_ALL}")
    input()
    if clear:
        cls()
    print(f"{Fore.BLACK + Fore.WHITE}({step}/{total_steps}) " + Fore.MAGENTA + Style.BRIGHT + title + Style.RESET_ALL)

def run_server(start_script:str = "start.cmd"):
    subprocess.Popen("start cmd /c " + start_script, stdin=subprocess.PIPE, shell=True)



def create_start_script(memory:int = 1, dir:str = None, java_path:str = "java", gui:str = "--nogui"):
    jar_flags = f"{java_path} -Xms{memory}G -Xmx{memory}G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar {gui}"
    if platform.system() == "Windows":
        with open(f'{dir}\start.cmd', 'w') as file:
            prefix = ".cmd"
            file.write("@echo off\n")
            file.write(jar_flags)
            file.write("\npause")
    elif platform.system() == "Linux":
        with open(f'{dir}\start.sh', 'w') as file:
            prefix = ".sh"
            file.write(jar_flags)
    else:
        print(Fore.RED + "ERROR: Your OS is not supported!" + platform.system() + Style.RESET_ALL)
        return False
    return os.path.dirname(os.path.realpath(__file__)) + f"\{dir}\start{prefix}"




def cls():
    if platform.system() == "Windows":  # For Windows
        os.system('cls')
    else:  # For Mac and Linux
        os.system('clear')

def create_shortcut(path: str, target: str, arguments: str = ""):
    wd = os.path.abspath(os.path.dirname(target))
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = os.path.abspath(target)
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = wd
    shortcut.save()

if __name__ == "__main__":
    main()