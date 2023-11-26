import os
import zipfile
import yaml
import requests
from downloads import download_file
from colorama import Fore, Style
from difflib import SequenceMatcher
from utils import *
import yaml
headers = {'X-Api-Token': '91ab28ce-f679-4356-8b06-362f94ee0348'}
root = os.path.abspath("minecraft")
plugin_path = os.path.abspath(f"{root}/plugins")
if not os.path.exists(f"{root}/plugin_data"):
    yml_path = os.mkdir(f"{root}/plugin_data")
else:
    yml_path = os.path.abspath(f"{root}/plugin_data")
ptypes = ["spigot", "bukkit"]

def get_download_url(plugin):
    if plugin.type[0] == "s":
        return f"https://api.spiget.org/v2/resources/{plugin.id}/download"
    elif plugin.type[0] == "b":
        return f"https://dev.bukkit.org/projects/{plugin.slug}/files/latest"
    else:
        raise ValueError("Invalid type")

def get_version_id(type, id):
        if type == "spigot":
            return requests.get(f"https://api.spiget.org/v2/resources/{id}").json()["version"]
        elif type == "bukkit":
            ljson = requests.get(f"https://api.curseforge.com/servermods/files?projectIds={id}").json()
            
            print(ljson, id)
            link = ljson[0]["fileUrl"].replace("\/", "/")
            return link.split("/")[-1]


class Plugin:
    def __init__(self, path, plugin):
        self.path = path
        self.id = plugin.id
        self.type = plugin.type
        self.slug = plugin.slug
        yaml = self.get_plugin_yml(path)
        self.name = yaml.get("name")
        self.version = yaml.get("version")
        self.version_id = get_version_id(type=self.type, id=self.id)
        self.api_version = yaml.get("api-version")
        self.website = yaml.get("website")
        self.download_url = get_download_url(
            SearchResult(id=self.id, type=self.type, name=self.name, slug=self.slug)
        )
        self.save_to_yml()
        
    def save_to_yml(self):
        to_dict = {
            "name": self.name,
            "version": self.version,
            "version-id": self.version_id,
            "api-version": self.api_version,
            "website": self.website,
            "slug": self.slug,
            "download-url": self.download_url,
        }
        with open(f"{yml_path}/{self.name}~{self.type[0]}~{self.id}.yml", "w") as yml:
            yaml.dump(to_dict, yml)
    def get_plugin_yml(self, jar_path):
        with zipfile.ZipFile(jar_path, "r") as jar:
            for file in jar.namelist():
                if file.endswith("plugin.yml"):
                    with jar.open(file) as yml:
                        return yaml.safe_load(yml)


def sort_results(r: list, query: str):
    for result in r:
        similarity = SequenceMatcher(None, query.lower(), result.name.lower()).ratio()
        result.search_volume = similarity
    return sorted(r, key=lambda x: x.search_volume, reverse=True)

def update_plugin_yml(path):
    for file in os.listdir(path):
        if file.endswith(".jar"):
            filename = os.path.basename(file)
            print(filename)
            try:
                filename = filename.split("~")
                name = filename[0]
                type = filename[1]
                id = filename[2].split(".")[0]
                with open(f'{name}~{type[0]}~{id}.yml', 'r') as file:
                    data = yaml.safe_load(file)
                data["name"] = name
                data["type"] = type
                data["id"] = id
                with open('my_class.yml', 'w') as file:
                    yaml.dump(data, file)
                if not data["version-id"] or data["version-id"] != get_version_id(type, id):
                    plugin = Plugin(path=f"{path}/{file}", plugin=SearchResult(type=type, name=name, id=id))
                    print(f"{Fore.GREEN}Updated plugin {name}{Style.RESET_ALL}")
                    download_plugin(plugin, plugin_path)
            except Exception as p:
                print(p)
                print(f"{Fore.RED}Could not set .yml for {filename}{Style.RESET_ALL}")
            

    

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
        self.formatted_results = [
            f"{i.name}{' ' * (l - len(i.name)) + Fore.WHITE + Style.DIM} │ {Style.RESET_ALL}{i.type_formatted}"
            for i in self.results
        ][0:9]

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
            results.append(SearchResult(type="bukkit", name=result["name"], id=result["id"], slug=result["slug"]))
        return sort_results(results, self.query)


def download_plugin(plugin: SearchResult, target):
    try:
        d = download_file(get_download_url(plugin), f"{target}/{plugin.name}~{plugin.type[0]}~{plugin.id}.jar")
    except FileExistsError:
        print(f"{Fore.RED}Plugin already installed!{Style.RESET_ALL}")

    return Plugin(path=d, plugin=plugin)



def plugin_install_process():
    search_results = Search(text("Enter a plugin name"))
    if len(search_results.results) == 0:
        print(f"{Fore.RED}No plugins found{Style.RESET_ALL}")
        return
    else:
        selection = choice(
            "Found plugins", search_results.formatted_results, return_index=True
        )
    plugin = search_results.results[selection]
    download_plugin(plugin, plugin_path)
    update_plugin_yml(plugin_path)

if __name__ == "__main__":
    plugin_install_process()
    