import platform
import requests

java_install = {
    16: {
        "portable": {
            "Windows": {
                "64bit": "https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.zip",
                "32bit": "https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x86-32_windows_hotspot_16.0.2_7.zip",
            }
        },
        "installer": {
            "Windows": {
                "64bit": "https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x64_windows_hotspot_16.0.2_7.msi",
                "32bit": "https://github.com/adoptium/temurin16-binaries/releases/download/jdk-16.0.2%2B7/OpenJDK16U-jdk_x86-32_windows_hotspot_16.0.2_7.msi",
            }
        },
    },
    17: {
        "portable": {
            "Windows": {
                "64bit": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9.1/OpenJDK17U-jdk_x64_windows_hotspot_17.0.9_9.zip",
                "32bit": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9.1/OpenJDK17U-jdk_x86-32_windows_hotspot_17.0.9_9.zip",
            }
        },
        "installer": {
            "Windows": {
                "64bit": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9.1/OpenJDK17U-jdk_x64_windows_hotspot_17.0.9_9.msi",
                "32bit": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9.1/OpenJDK17U-jdk_x86-32_windows_hotspot_17.0.9_9.msi",
            }
        },
    },
    8: {
        "portable": {
            "Windows": {
                "64bit": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9.1/OpenJDK17U-jdk_x64_windows_hotspot_17.0.9_9.zip",
                "32bit": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9.1/OpenJDK17U-jdk_x86-32_windows_hotspot_17.0.9_9.zip",
            }
        },
        "installer": {
            "Windows": {
                "64bit": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9.1/OpenJDK17U-jdk_x64_windows_hotspot_17.0.9_9.msi",
                "32bit": "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9.1/OpenJDK17U-jdk_x86-32_windows_hotspot_17.0.9_9.msi",
            }
        },
    }
}


def latest_mc_version():
    return str(requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", timeout=15).json()["latest"]["release"])


def get_intermidiate_version(version: str):
    return int(version.split(".")[1])


class Paper:

    def __init__(self, version: str):
        self.version = str(version)
        self.url = f"https://papermc.io/api/v2/projects/paper/versions/{self.version}/builds/{self.latest_build()}/downloads/paper-{self.version}-{self.latest_build()}.jar"

    def latest_build(self):
        return requests.get(f"https://papermc.io/api/v2/projects/paper/versions/{self.version}", timeout=15).json()['builds'][-1]


class Vanilla:

    def __init__(self, version: str):
        self.version = str(version)
        self.url = self.get_url()

    def get_url(self):
        version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", timeout=15).json()['versions']
        for version in version_list:
            if version['id'] == self.version:
                return requests.get(version['url'], timeout=15).json()['downloads']['server']['url']


class Spigot:

    def __init__(self, version: str):
        self.version = str(version)
        self.url = f"https://download.getbukkit.org/spigot/spigot-{self.version}.jar"


class CraftBukkit:

    def __init__(self, version: str):
        self.version = str(version)
        self.url = f"https://download.getbukkit.org/craftbukkit/craftbukkit-{self.version}.jar"


class Purpur:

    def __init__(self, version: str):
        self.version = str(version)
        self.url = f"https://api.purpurmc.org/v2/purpur/{self.version}/latest/download"


class Pufferfish:

    def __init__(self, version: str):
        self.version = str(version)
        self.intermidiate_version = int(self.version.split(".")[1])
        if self.intermidiate_version < 17:
            raise ValueError("Pufferfish is only available for 1.17.X and above.")
        self.url = self.get_file()

    def get_file(self):
        builds = requests.get(f"https://ci.pufferfish.host/job/Pufferfish-1.{self.intermidiate_version}/api/json", timeout=15).json()["builds"]
        for build in builds:
            v = requests.get(f"{build['url']}/api/json", timeout=15).json()['artifacts'][0]['displayPath']
            build_version = v.split("-")[2]
            if build_version == self.version:
                return f"https://ci.pufferfish.host/job/Pufferfish-1.{self.intermidiate_version}/{build['number']}/artifact/build/libs/{v}"


def fetch_link(version: str, server_type: str):
    if server_type.lower() == "vanilla":
        return Vanilla(version).url
    elif server_type.lower() == "spigot":
        return Spigot(version).url
    elif server_type.lower() == "craftbukkit":
        return CraftBukkit(version).url
    elif server_type.lower() == "paper":
        return Paper(version).url
    elif server_type.lower() == "purpur":
        return Purpur(version).url
    elif server_type.lower() == "pufferfish":
        return Pufferfish(version).url
    else:
        raise ValueError(f"Invalid server type: {server_type}")


def check_valid_version(version: str):
    version_list = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json", timeout=15).json()['versions']
    for v in version_list:
        if v['id'] == version:
            return True
    return False


def get_java_link(version: int, architecture: str):
    return java_install[version]["portable"][platform.system()][architecture]


supported_types = ["Vanilla", "Craftbukkit", "Spigot", "Paper", "Pufferfish", "Purpur"]
