import csv
import os.path
from typing import List

FILENAME = os.path.join(os.path.dirname(__file__), "babynames-clean.csv")


def load_names(gender: str) -> List[str]:
    with open(FILENAME, "r") as f:
        reader = csv.reader(f)
        return [r[0] for r in reader if r[1] == gender]
