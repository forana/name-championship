import argparse
from names.challenge import Challenge

parser = argparse.ArgumentParser("names", description="Start a tournament of names.")
parser.add_argument("gender", type=str, help="'boy' or 'girl'")
parser.add_argument("action", type=str, choices=["run", "stats"])
args = parser.parse_args()

c = Challenge(args.gender)
if args.action == "run":
    c.run()
if args.action == "stats":
    c.stats()
