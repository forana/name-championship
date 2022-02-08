import argparse
from names.challenge import Challenge

parser = argparse.ArgumentParser("names", description="Start a tournament of names.")
parser.add_argument("gender", type=str, help="'boy' or 'girl'")
args = parser.parse_args()

Challenge(args.gender).run()
