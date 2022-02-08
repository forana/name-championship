from contextlib import closing
from sqlite3 import Cursor, connect
from typing import List, Optional, Tuple


class DB:
    def __init__(self, gender: str):
        self.conn = connect(f"names-{gender}.sqlite")
        self._create_tables()

    def _create_tables(self) -> None:
        with closing(self.cursor()) as cur:
            Name.create_table(cur)
            Log.create_table(cur)

    def cursor(self) -> Cursor:
        cur = self.conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        return cur


class Name:
    def __init__(self, cur: Cursor, name: str, tier: int, rejected: bool):
        self.cur = cur
        self.name = name
        self.tier = tier
        self.rejected = rejected

    @classmethod
    def create_table(cls, cur: Cursor) -> None:
        cur.execute("create table if not exists names (name text primary key, tier integer not null, rejected integer not null)")
        cur.execute("create index if not exists idx_name_tier on names (tier)")
        cur.execute("create index if not exists idx_name_unrejected_tier on names (tier) where not rejected")

    @classmethod
    def insert(cls, cur: Cursor, names: List[str]) -> int:
        cur.execute("begin")
        rowcount = cur.executemany("insert into names (name, tier, rejected) values (?, 0, false)", [(n,) for n in names]).rowcount
        cur.execute("commit")
        return rowcount

    @classmethod
    def unrejected_tier_counts(cls, cur: Cursor) -> Tuple[int, int]:
        return cur.execute('select tier, count(name) as "count" from names where not rejected group by tier order by tier asc').fetchall()

    @classmethod
    def pair_for_tier(cls, cur: Cursor, tier: int) -> List["Name"]:
        """
        Might return less than 2 rows - needs to be checked.
        """
        rows = cur.execute("select name from names where tier = ? and not rejected order by random() limit 2", (tier,)).fetchall()
        return [Name(cur, r[0], tier, False) for r in rows]

    @classmethod
    def winning_name(cls, cur: Cursor) -> str:
        return cur.execute("select name from names where not rejected limit 1").fetchone()[0]

    def _update(self, reject: bool) -> None:
        self.cur.execute("begin")
        self.cur.execute("update names set tier = ?, rejected = ? where name = ?", (self.tier, reject, self.name))
        self.cur.execute("commit")

    def reject(self):
        self._update(True)

    def advance(self):
        self._update(False)


class Log:
    def __init__(self, tier: int, winner: str, loser: str):
        self.tier = tier
        self.winner = winner
        self.loser = loser

    @classmethod
    def create_table(cls, cur: Cursor) -> None:
        cur.execute("create table if not exists logs (tier integer not null, winner text null, loser text not null, ts integer not null)")

    @classmethod
    def log(cls, cur: Cursor, tier: int, winner: Optional[str], loser: str):
        cur.execute("begin")
        cur.execute("insert into logs (tier, winner, loser, ts) values (?, ?, ?, time('now'))", (tier, winner, loser))
        cur.execute("commit")
