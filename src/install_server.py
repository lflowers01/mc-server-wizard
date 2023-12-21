import subprocess
from datetime import datetime
import os
import zipfile
import platform
from time import sleep
import sys
import win32com.client
from colorama import Fore, Style
from downloads import download_file
import fetch_versions as fetch_ver
from utils import choice, text

main_dir = os.path.dirname(sys.executable)


def install_server():
    cls()
    print(Fore.YELLOW + Style.BRIGHT + "Minecraft Server Installer Wizard ~" + Style.RESET_ALL)
    print("This installer will guide you through the process of installing a Minecraft server.")

    next_step("Version Selection", 1, 5, False)
    version = None

    while version is None:
        version = text("Enter the version of the server you want to install (1.XX.XX)")
        if len(version.split(".")) != 3 or not fetch_ver.check_valid_version(version):
            print(Fore.RED + f"Invalid version! {Fore.WHITE}(1.XX.XX)" + Style.RESET_ALL)
            version = None
    inter_version = fetch_ver.get_intermidiate_version(version)
    legacy = False
    if inter_version < 13:
        legacy = True
        print(Fore.RED + Style.BRIGHT + f"WARNING: Version {version} may not work with this tool! Proceed with cation!" + Style.RESET_ALL)
    if inter_version < 18:
        target_java = 8
    else:
        target_java = 17
    jar_select = None
    print(Fore.GREEN + f"Version: {Fore.WHITE}{version}{Fore.GREEN} selected" + Style.RESET_ALL)
    next_step("JAR Dowload", 2, 5)
    while jar_select is None:
        if legacy:
            print(Fore.RED + Style.BRIGHT + "WARNING: Manual install is recomended with older versions." + Style.RESET_ALL)
        if (choice(
                "Do you want to install your JAR manualy or automatically?",
            ["Automatic", "Manual"],
                "Automatic",
        ) == "Automatic"):
            jar_select = choice("Select server JAR to install:", fetch_ver.supported_types, "Paper")
            print(Fore.CYAN + f"Downloading {jar_select}..." + Style.RESET_ALL)
            try:
                link = fetch_ver.fetch_link(version, jar_select)
                download_file(link, f"{main_dir}/server.jar")
            except FileNotFoundError as e:
                print(Fore.RED + f"No {jar_select} JAR found for version {version}!{Style.RESET_ALL}")
                print(Fore.YELLOW + "Try downloading the server JAR yourself; some legacy JARs may be too old!" + Style.RESET_ALL + "\n" + e)
                jar_select = None

        else:
            jar_select = "Manual"
            while jar_select == "Manual":
                choice(
                    f"Download the server JAR you want to install and place it in the server directory ({main_dir})."
                    "Press enter to continue",
                    ["OK"],
                )
                for item in os.listdir(main_dir):
                    if item.endswith(".jar"):
                        jar_select = item
                        print(Fore.GREEN + f"Found {jar_select}!" + Style.RESET_ALL)
                        break
                os.rename(
                    os.path.join(main_dir, jar_select),
                    os.path.join(main_dir, "server.jar"),
                )
                jar_select = "server.jar"
    next_step("Java Setup", 3, 5)
    java_version = None
    install_java = False
    try:
        output = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
        java_version = (next((line for line in output.decode("utf-8").split("\n") if "version" in line)).split(" ")[2].replace('"', ""))
        java_version = java_version.split(".")[1]
        print(f"Java version: {java_version}")

        if int(java_version) < target_java:
            install_java = True
    except subprocess.CalledProcessError:
        install_java = True
    except FileNotFoundError as e:
        print(Fore.RED + f"No {jar_select} JAR found for version {version}!{Style.RESET_ALL}")
        print(Fore.YELLOW + "Try downloading the server JAR yourself; some legacy JARs may be too old!" + Style.RESET_ALL + "\n" + str(e))
        jar_select = None

    java_path = "java"
    if install_java:
        if choice("Java is not installed or is outdated! Do you want to install it now?", ["Yes", "No"], "Yes") == "Yes":
            if platform.system() == "Linux":
                try:
                    print(Fore.CYAN + "Downloading Java..." + Style.RESET_ALL)
                    subprocess.run(["sudo", "apt", "install", "-y", "openjdk-17-jdk"], check=True)
                except subprocess.CalledProcessError as e:
                    print(Fore.RED + f"ERROR: While trying to install Java 17:\n{Style.RESET_ALL}{e}")
                    print(Fore.YELLOW + f"Try installing Java {target_java} JDK yourself" + Style.RESET_ALL)
                    return
            if platform.system() == "Windows":
                # install_extension = ".zip"
                portable = "portable"

                architecture = platform.architecture()[0]
                link = fetch_ver.get_java_link(target_java, architecture)
                print(link)
                headers = {'accept': '*/*'}
                z = download_file(link, f"{main_dir}/java.zip", headers=headers)
                if portable == "portable":
                    print(Fore.CYAN + "Extracting Java..." + Style.RESET_ALL + z)
                    print("java.zip path : " + z)
                    with zipfile.ZipFile(z, 'r') as zip_ref:
                        zip_ref.extractall(f"{main_dir}")
                    os.remove(z)

                    for item in os.listdir(main_dir):
                        if item.startswith("jdk"):
                            java_path = item
                            java_path = '"' + str(java_path) + "/bin/java.exe" + '"'
                            break
                    print(Fore.GREEN + f"Java installed! {Fore.WHITE}{java_path}" + Style.RESET_ALL)
    memory = None
    next_step("Startup Settings", 4, 5)
    while memory is None:
        memory = text("Enter the amount of memory you want to allocate to the server (in GB)")
        try:
            memory = int(memory)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "Invalid amount of memory!" + Style.RESET_ALL + e)
            memory = None
    if choice("Do you want to enable the GUI?", ["Yes", "No"], "No") == "Yes":
        gui = ""
    else:
        gui = "nogui"
    start_script = create_start_script(memory, main_dir, java_path, gui)
    if not start_script:
        return
    print(Fore.GREEN + "Server installation complete!" + Style.RESET_ALL)
    next_step("EULA and final steps", 5, 5)
    skip_eula = False
    if inter_version <= 7 and version != "1.7.10":
        skip_eula = True
        print(Fore.RED + Style.BRIGHT + f"WARNING: EULA is not required for this version! {Fore.WHITE}(skipping process)" + Style.RESET_ALL)
    if not skip_eula:
        print(Fore.CYAN + "Starting server..." + Style.RESET_ALL)
        os.chdir(main_dir)
        run_server("start.cmd")
        eula_path = os.path.join("eula.txt")
        timeout = 0
        while not os.path.isfile(eula_path):
            sleep(1)
            timeout += 1
            if timeout > 75:
                print(Fore.RED + "ERROR: Timed out - Server failed to initialize! (Do you have the right Java version installed?)" + Style.RESET_ALL)
                return
        print(Fore.GREEN + "Server started!" + Style.RESET_ALL)

        print(Fore.CYAN + "Accepting EULA..." + Style.RESET_ALL)
        with open(eula_path, "r+", encoding='utf-8') as file:
            file_data = file.read()
            file.seek(0)
            file.write(file_data.replace("eula=false", "eula=true"))
            file.truncate()
        print(Fore.GREEN + "EULA accepted!" + Style.RESET_ALL)
    if not os.path.exists("plugins") and not jar_select == "Vanilla":
        os.mkdir("plugins")

    if platform.system() == "Windows":
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, f"{main_dir}.lnk")
        print(shortcut_path, start_script)
        if choice("Do you want to create a desktop shortcut?", ["Yes", "No"], "Yes") == "Yes":
            print(Fore.CYAN + "Creating shortcut on your desktop..." + Style.RESET_ALL)
            create_shortcut(target="start.cmd", path=shortcut_path, arguments="")
            print(Fore.GREEN + "Shortcut created!" + Style.RESET_ALL)
    cls()
    print(Fore.GREEN + Style.BRIGHT + "Server installation complete!" + Style.RESET_ALL)
    if choice("Do you want to start the server now?", ["Yes", "No"], "Yes") == "Yes":
        run_server("start.cmd")
    return main_dir


def next_step(title: str = None, step: int = None, total_steps: int = None, clear: bool = True):
    sleep(1)
    print(f"{Fore.YELLOW + Style.BRIGHT}Press enter to continue...{Style.RESET_ALL}")
    input()
    if clear:
        cls()
    print(f"{Fore.BLACK + Fore.WHITE}({step}/{total_steps}) " + Fore.MAGENTA + Style.BRIGHT + title + Style.RESET_ALL)


def run_server(start_script: str = "start.cmd"):
    print("Starting server...")
    os.system(start_script)


def create_start_script(memory: int = 1, target_dir: str = None, java_path: str = "java", gui: str = "--nogui"):
    jar_flags = f"{java_path} -Xms{memory}G -Xmx{memory}G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar server.jar {gui}"
    if platform.system() == "Windows":
        with open(f"{target_dir}/start.cmd", "w", encoding='utf-8') as file:
            prefix = ".cmd"
            file.write("@echo off\n")
            file.write(jar_flags)
            file.write("\npause")
    elif platform.system() == "Linux":
        with open(f"{target_dir}/start.sh", "w", encoding='utf-8') as file:
            prefix = ".sh"
            file.write(jar_flags)
    else:
        print(Fore.RED + "ERROR: Your OS is not supported!" + platform.system() + Style.RESET_ALL)
        return False
    return os.path.dirname(os.path.realpath(__file__)) + f"/{target_dir}/start{prefix}"


def cls():
    if platform.system() == "Windows":  # For Windows
        os.system("cls")
    else:  # For Mac and Linux
        os.system("clear")


def create_shortcut(path: str, target: str, arguments: str = ""):
    wd = os.path.abspath(os.path.dirname(target))
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = os.path.abspath(target)
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = wd
    shortcut.save()


def make_archive(output_filename, source_dir):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Skip directories that contain "jdk" or "backup"
            if "jdk" in root or "backup" in root:
                continue
            for file in files:
                # Skip .exe files
                if file.endswith('.exe'):
                    continue
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, source_dir)
                print(f'Adding {relative_path} to archive...')
                zipf.write(full_path, relative_path)


def create_backup():
    source_dir = os.getcwd()

    # Define the backup directory
    backup_dir = f"{source_dir}/backups"

    # Define the name and full path for the zip file
    zip_name = f"backups-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.zip"
    zip_path = os.path.join(backup_dir, zip_name)

    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    print(Fore.CYAN + "Creating backup..." + Style.RESET_ALL)
    make_archive(zip_path, source_dir)
    print(Fore.GREEN + "Backup created!" + Style.RESET_ALL)
    return
