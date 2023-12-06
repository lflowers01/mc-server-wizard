import os
import requests
from tqdm import tqdm
from colorama import Fore, Style


def download_file(url, filename, headers=None):
    response = requests.get(url, stream=True, timeout=15, headers=headers)

    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024

    progress_bar = tqdm(
        total=total_size_in_bytes,
        unit="iB",
        unit_scale=True,
        desc=os.path.basename(filename),
        ascii=True,
        ncols=75,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}",
    )

    with open(filename, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print(Fore.RED + f"ERROR, something went wrong downloading {url}" + Style.RESET_ALL)
        return False
    else:
        return os.path.abspath(filename)


jars = {
    "1.16": {
        "Vanilla": "https://piston-data.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar",
        "Spigot": "https://cdn.getbukkit.org/spigot/spigot-1.16.5.jar",
        "CraftBukkit": "https://cdn.getbukkit.org/craftbukkit/craftbukkit-1.16.5.jar",
        "Paper": "https://papermc.io/api/v2/paper/1.16.5/latest/download",
        "Purpur": "https://api.purpurmc.org/v2/purpur/1.16.5/latest/download",
    },
    "1.17": {
        "Vanilla": "https://piston-data.mojang.com/v1/objects/a16d67e5807f57fc4e550299cf20226194497dc2/server.jar",
        "Spigot": "https://download.getbukkit.org/spigot/spigot-1.17.1.jar",
        "CraftBukkit": "https://download.getbukkit.org/craftbukkit/craftbukkit-1.17.1.jar",
        "Paper": "https://papermc.io/api/v2/paper/1.17.1/latest/download",
        "Pufferfish": "https://ci.pufferfish.host/job/Pufferfish-1.17/22/artifact/build/libs/Pufferfish-1.17.1-R0.1-SNAPSHOT.jar",
        "Purpur": "https://api.purpurmc.org/v2/purpur/1.19.4/latest/download",
    },
    "1.18": {
        "Vanilla": "https://piston-data.mojang.com/v1/objects/c8f83c5655308435b3dcf03c06d9fe8740a77469/server.jar",
        "Spigot": "https://download.getbukkit.org/spigot/spigot-1.18.2.jar",
        "CraftBukkit": "https://download.getbukkit.org/craftbukkit/craftbukkit-1.18.2.jar",
        "Paper": "https://papermc.io/api/v2/paper/1.18.2/latest/download",
        "Pufferfish": "https://ci.pufferfish.host/job/Pufferfish-1.18/72/artifact/build/libs/pufferfish-paperclip-1.18.2-R0.1-SNAPSHOT-reobf.jar",
        "Purpur": "https://api.purpurmc.org/v2/purpur/1.18.2/latest/download",
    },
    "1.19": {
        "Vanilla": "https://piston-data.mojang.com/v1/objects/8f3112a1049751cc472ec13e397eade5336ca7ae/server.jar",
        "Spigot": "https://download.getbukkit.org/spigot/spigot-1.19.4.jar",
        "CraftBukkit": "https://download.getbukkit.org/craftbukkit/craftbukkit-1.19.4.jar",
        "Paper": "https://papermc.io/api/v2/paper/1.19.4/latest/download",
        "Pufferfish": "https://ci.pufferfish.host/job/Pufferfish-1.19/73/artifact/build/libs/pufferfish-paperclip-1.19.4-R0.1-SNAPSHOT-reobf.jar",
        "Purpur": "https://api.purpurmc.org/v2/purpur/1.19.4/latest/download",
    },
    "1.20": {
        "Vanilla": "https://piston-data.mojang.com/v1/objects/5b868151bd02b41319f54c8d4061b8cae84e665c/server.jar",
        "Spigot": "https://download.getbukkit.org/spigot/spigot-1.20.2.jar",
        "CraftBukkit": "https://download.getbukkit.org/craftbukkit/craftbukkit-1.20.2.jar",
        "Paper": "https://papermc.io/ci/job/Paper-1.20/lastBuild/artifact/paperclip.jar",
        "Pufferfish": "https://ci.pufferfish.host/job/Pufferfish-1.20/33/artifact/build/libs/pufferfish-paperclip-1.20.2-R0.1-SNAPSHOT-reobf.jar",
        "Purpur": "https://api.purpurmc.org/v2/purpur/1.20.2/latest/download",
    },
}

plugins = {
    "EssentialsX": "",
    "LuckPerms": "",
    "Vault": "https://dev.bukkit.org/projects/vault/files/latest",
    "WorldEdit": "https://dev.bukkit.org/projects/worldedit/files/latest",
    "WorldGuard": "https://dev.bukkit.org/projects/worldguard/files/latest",
    "ClearLag": "https://dev.bukkit.org/projects/clearlagg/files/latest",
    "ProtocolLib": "",
    "ViaVersion": "",
    "ViaBackwards": "",
    "ViaRewind": "",
    "Chunky": "",
    "FastAsyncWorldEdit": "",
    "spark": "",
    "CoreProtect": "",
    "dynmap": "",
    "multiverse-core": "",
    "vault-chat-format": "",
    "citizens": "",
    "mcMMO": "",
    "PlaceholderAPI": "",
    "Shopkeepers": "",
}
