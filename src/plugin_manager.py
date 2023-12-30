import os
from difflib import SequenceMatcher
import yaml
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style
from downloads import download_file
from utils import *


def set_root(root):
    global plugin_path, yml_path
    plugin_path = os.path.abspath(f"{root}/plugins")
    if not os.path.exists(f"{root}/plugin_data"):
        os.mkdir(f"{root}/plugin_data")

    yml_path = os.path.abspath(f"{root}/plugin_data")


ptypes = ["spigot", "bukkit"]


def get_download_url(plugin):
    if plugin.type[0] == "s":
        return f"https://api.spiget.org/v2/resources/{plugin.id}/download"
    elif plugin.type[0] == "b":
        return f"https://dev.bukkit.org/projects/{plugin.slug}/files/latest"
    else:
        raise ValueError("Invalid type")


def get_version_id(type, id, slug):
    if type[0] == "s":
        return requests.get(f"https://api.spiget.org/v2/resources/{id}").json()["version"]
    elif type[0] == "b":
        r = requests.get(f"https://dev.bukkit.org/projects/{slug}/files")
        soup = BeautifulSoup(r.content, "html.parser")
        version_id = soup.find("tbody").find("a")["href"]
        if version_id is not None:
            return version_id.split("/")[-2]
        else:
            return None


class Plugin:

    def __init__(self, plugin):
        self.id = plugin.id
        self.type = plugin.type
        self.slug = plugin.slug
        self.name = plugin.name
        self.version_id = get_version_id(type=self.type, id=self.id, slug=self.slug)
        self.save_to_yml()

    def save_to_yml(self):
        to_dict = {
            "name": self.name,
            "version-id": self.version_id,
            "slug": self.slug,
        }
        with open(f"{yml_path}/{self.name}~{self.type[0]}~{self.id}.yml", "w") as yml:
            yaml.dump(to_dict, yml)

    def get_plugin_yml(self, jar_path):
        # update_plugin_yml(jar_path)
        yname = os.path.basename(jar_path).split(".")[0]
        if os.path.exists(f"{yml_path}/{yname}.yml"):
            with open(f"{yml_path}/{yname}.yml", "r") as yml:
                return yaml.safe_load(yml)
        else:
            open(f"{yml_path}/{yname}.yml", "w").close()


def sort_results(r: list, query: str):
    for result in r:
        similarity = SequenceMatcher(None, query.lower(), result.name.lower()).ratio()
        result.search_volume = similarity
    return sorted(r, key=lambda x: x.search_volume, reverse=True)


def update_plugin_yml(path):
    c = 0
    for file in os.listdir(path):
        if file.endswith(".jar"):
            filename = os.path.basename(file)

            filename = filename.split("~")
            name = filename[0]
            type = filename[1]
            id = filename[2].split(".")[0]
            yml_file = f"{yml_path}/{name}~{type[0]}~{id}.yml"

            if not os.path.exists(yml_file):
                os.mkdir(yml_file)
            with open(yml_file, "r") as file:
                data = yaml.safe_load(file)
            data["name"] = name
            data["type"] = type
            data["id"] = id
            with open(yml_file, "w") as file:
                yaml.dump(data, file)
            if data["version-id"] != get_version_id(type, id, data["slug"]):
                c += 1
                print(f"{Fore.CYAN}Updating {name}{Style.RESET_ALL}")
                download_plugin(
                    plugin=Plugin(SearchResult(type=type, name=name, id=id, slug=data["slug"])),
                    target=plugin_path,
                )
                data["version-id"] = get_version_id(type, id, data["slug"])
                with open(yml_file, "w") as file:
                    yaml.dump(data, file)
    if c == 0:
        print(f"{Fore.GREEN}No updates available{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}Updated {c} plugins{Style.RESET_ALL}")


def get_longest(l: list):
    longest = 0
    for i in l:
        if len(i) > longest:
            longest = len(i)
    return longest


class SearchResult:

    def __init__(self, type: ptypes, name, id: int, search_volume=0, slug=None):
        self.type = type
        self.name = name
        self.id = id
        self.search_volume = search_volume
        self.slug = slug
        self.type_formatted = self.type.title()
        if self.type == "spigot":
            self.type_formatted = Fore.YELLOW + self.type_formatted + Style.RESET_ALL
        elif self.type == "bukkit":
            self.type_formatted = Fore.BLUE + self.type_formatted + Style.RESET_ALL


class Search:

    def __init__(self, query):
        self.query = query
        self.spigot = self.spigot_search()
        self.bukkit = self.bukkit_search()
        self.results = self.get_results()

        l = get_longest([i.name for i in self.results][0:9])
        self.formatted_results = [f"{i.name}{' ' * (l - len(i.name)) + Fore.WHITE + Style.DIM} │ {Style.RESET_ALL}{i.type_formatted}" for i in self.results][0:9]

    def spigot_search(self):
        link = f"https://api.spiget.org/v2/search/resources/{self.query}?field=name&sort=download&size=10"
        response = requests.get(link).json()
        return response

    def bukkit_search(self):
        q = self.query.replace(" ", "-").lower()
        link = f"https://servermods.forgesvc.net/servermods/projects?search={q}"
        response = requests.get(link).json()
        return response

    def get_results(self):
        results = []
        for result in self.spigot:
            results.append(SearchResult("spigot", result["name"], result["id"]))
        for result in self.bukkit:
            results.append(SearchResult(
                type="bukkit",
                name=result["name"],
                id=result["id"],
                slug=result["slug"],
            ))
        return sort_results(results, self.query)


def download_plugin(plugin: SearchResult, target):
    try:
        d = download_file(
            get_download_url(plugin),
            f"{target}/{plugin.name}~{plugin.type[0]}~{plugin.id}.jar",
        )
    except FileExistsError:
        print(f"{Fore.RED}Plugin already installed!{Style.RESET_ALL}")

    return Plugin(plugin=plugin)


def plugin_install_process(ref):
    if not ref:
        search_results = Search(text("Enter a plugin name"))
    else:
        search_results = Search(ref)
    if len(search_results.results) == 0:
        print(f"{Fore.RED}No plugins found{Style.RESET_ALL}")
        return
    else:
        selection = choice("Found plugins", search_results.formatted_results, return_index=True)
    plugin = search_results.results[selection]
    print(f"{Fore.CYAN}Installing {plugin.name}{Style.RESET_ALL}")
    download_plugin(plugin, plugin_path)
    print(f"{Fore.GREEN}Installed {plugin.name}{Style.RESET_ALL}")


def list_plugins():
    for file in os.listdir(plugin_path):
        if file.endswith(".jar"):
            print(file.split("~")[0])


def delete_plugin(q):
    q = q.lower().rstrip()
    print(q)
    for file in os.listdir(plugin_path):
        if file.split("~")[0].lower() == q:
            os.remove(f"{plugin_path}/{file}")
            print(f"{Fore.GREEN}Deleted {q}.jar{Style.RESET_ALL}")
    for file in os.listdir(yml_path):
        if file.split("~")[0].lower() == q:
            os.remove(f"{yml_path}/{file}")
            print(f"{Fore.GREEN}Deleted {q}.yml{Style.RESET_ALL}")
            return
    print(f"{Fore.RED}Plugin not found{Style.RESET_ALL}")


def disable_plugin(q):
    q = q.lower().rstrip()
    print(q)
    for file in os.listdir(os.path.abspath(plugin_path)):
        if not os.path.isdir(os.path.join(plugin_path, file)):
            if file.endswith(".disabled"):
                if file.split(".")[0].split("~")[0].lower() == q:
                    os.rename(f"{plugin_path}/{file}", f"{plugin_path}/{file.split('.')[0]}.jar")
                    print(f"{Fore.GREEN}Enabled {q}.jar{Style.RESET_ALL}")
                    return
            else:
                if file.split("~")[0].lower() == q:
                    os.rename(f"{plugin_path}/{file}", f"{plugin_path}/{file}.disabled")
                    print(f"{Fore.GREEN}Disabled {q}.jar{Style.RESET_ALL}")
