# database.py

import sqlite3

class TournamentDatabase:
    def __init__(self, db_name="tournament_results.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, stack INTEGER)")
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY, player_id INTEGER, decision TEXT, profit INTEGER, FOREIGN KEY (player_id) REFERENCES players(id))")

    def save_player(self, player):
        with self.conn:
            cur = self.conn.execute("INSERT INTO players (name, stack) VALUES (?, ?)", (player.name, player.stack))
            player_id = cur.lastrowid
            return player_id

    def save_game(self, player_id, decision, profit):
        with self.conn:
            self.conn.execute("INSERT INTO games (player_id, decision, profit) VALUES (?, ?, ?)", (player_id, decision, profit))

    def fetch_player_stats(self, player_name):
        with self.conn:
            player_stats = self.conn.execute("SELECT * FROM players WHERE name=?", (player_name,)).fetchall()
        return player_stats if player_stats else None

# Пример использования базы данных:
if __name__ == "__main__":
    db = TournamentDatabase()
    player_id = db.save_player(PokerPlayer("Player 1", 5000))
    db.save_game(player_id, "call", 300)
    print(db.fetch_player_stats("Player 1"))
