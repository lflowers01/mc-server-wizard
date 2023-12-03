from urllib.parse import urlparse
from colorama import Fore
import inquirer


def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def text(q: str, default: str = None):
    questions = [inquirer.Text("text", message=q + Fore.YELLOW, default=default)]
    return inquirer.prompt(questions)["text"]


def choice(q: str, options: [str], default: str = None, return_index: bool = False):
    questions = [inquirer.List("choice", message=q, choices=options, default=default)]
    if return_index:
        return options.index(inquirer.prompt(questions)["choice"])
    else:
        return inquirer.prompt(questions)["choice"]


def checkbox(q: str, options: [str], default: str = None):
    questions = [inquirer.Checkbox("choice", message=q, choices=options, default=default)]
    return inquirer.prompt(questions)["choice"]
