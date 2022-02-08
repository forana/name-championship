import sys
from contextlib import closing
from sqlite3 import Cursor

import names.io as io
from names.data import load_names
from names.db import DB, Log, Name


class Challenge:
    def __init__(self, gender: str):
        self.db = DB(gender)
        self.gender = gender
        self.check_tiers()

    def check_tiers(self):
        """
        Load data if the tiers are empty. Exit program if there as been a winner.
        """
        with closing(self.db.cursor()) as cur:
            tiers = Name.unrejected_tier_counts(cur)
            if len(tiers) == 0:
                self.populate_names(cur)
            else:
                for tier, count in tiers:
                    print(f"{io.bold(count)} left for round {tier + 1}")

    def populate_names(self, cur: Cursor):
        count = Name.insert(cur, load_names(self.gender))
        print(io.green(f" -> populated {count} names"))

    def run(self):
        while True:
            with closing(self.db.cursor()) as cur:
                lowest_tier, count = Name.unrejected_tier_counts(cur)[0]
                if count == 1:
                    print("Looks like we have a winner!")
                    print("")
                    print(io.bold(io.blue(Name.winning_name(cur))))
                    print("")
                    sys.exit(0)
                print(io.bold(f"Round {lowest_tier + 1} - {count} left"))
                choices = Name.pair_for_tier(cur, lowest_tier)
                if len(choices) == 1:
                    print(f"Odd count this round - '{choices[0].name}' automatically advances.")
                    choices[0].advance()
                else:
                    print(f"  1) {io.blue(choices[0].name)}")
                    print(f"  2) {io.green(choices[1].name)}")
                    print(f"  3) {io.red('Neither')} (reject both)")
                    answer = io.prompt("Which is better? (1/2/3) ", ["1", "2", "3"])
                    if answer in {"1", "2"}:
                        winner = choices[0] if answer == "1" else choices[1]
                        loser = choices[1] if answer == "1" else choices[0]
                        winner.advance()
                        loser.reject()
                        Log.log(cur, lowest_tier, winner.name, loser.name)
                    if answer == "3":
                        choices[0].reject()
                        choices[1].reject()
                        Log.log(cur, lowest_tier, None, choices[0].name)
                        Log.log(cur, lowest_tier, None, choices[1].name)
