import sys
from typing import List


def blue(s: str) -> str:
    return f"\033[94m{s}\033[0m"

def green(s: str) -> str:
    return f"\033[92m{s}\033[0m"

def red(s: str) -> str:
    return f"\033[91m{s}\033[0m"

def bold(s: str) -> str:
    return f"\033[1m{s}\033[0m"

def prompt(message: str, choices: List[str]) -> str:
    choice = None
    sys.stdout.write(message)
    sys.stdout.flush()
    while True:
        choice = sys.stdin.read(1)
        if choice in choices:
            return choice
