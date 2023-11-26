import pylnk3
from urllib.parse import urlparse
from colorama import Fore
from inquirer import *

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False




def text(q:str, default:str = None):
    questions = [
        Text(
            "text",
            message=q + Fore.YELLOW,
            default=default
        )
    ]
    return prompt(questions)["text"]


def choice(q:str, options: [str], default:str = None, return_index:bool = False):
    questions = [
        List(
            "choice",
            message=q,
            choices=options,
            default=default
        )
    ]
    if return_index:
        return options.index(prompt(questions)["choice"])
    else:
        return prompt(questions)["choice"]

def checkbox(q:str, options: [str], default:str = None):
    questions = [
        Checkbox(
            "choice",
            message=q,
            choices=options,
            default=default
        )
    ]
    return prompt(questions)["choice"]