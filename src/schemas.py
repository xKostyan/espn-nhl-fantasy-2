# this maps API value to sqlite table column name
# as well this chema is used to create 'scoring' table as this lists all statistics tracked for players
espn_to_sqlite_names = {
    "G": "G",
    "A": "A",
    "PIM": "PIM",
    "PPG": "PPG",
    "19": "PPA",
    "SHG": "SHG",
    "SHA": "SHA",
    "GWG": "GWG",
    "HAT": "HAT",
    "SOG": "SOG",
    "HIT": "HIT",
    "BLK": "BLK",
    "DEF": "DEF",
    "FOW": "FOW",
    "FOL": "FOL",
    "25": "_25",
    "TTOI ?": "TTOI",
    "ATOI": "ATOI",
    "30": "GP",
    "GP": "GP",
    "35": "_35",
    "36": "_36",
    "37": "_37",
    "+/-": "P_M",
    "16": "PTS",
    "PPP": "PPP",
    "SHP": "SHP",
    "GS": "GS",
    "W": "W",
    "L": "L",
    "GA": "GA",
    "SV": "SV",
    "SO": "SO",
    "OTL": "OTL",
    "MIN ?": "MIN",
    "GAA": "GAA",
    "SV%": "SVP"
}

# contains descriptions for the stats column names
sqlite_column_descriptions = {
    "id": "player id",
    "name": "player name",
    "active": "flag to indicate if player is active",
    "position_type": "player position type (Skater or Goalie)",
    "position": "player position (Forward, Defencemen, Goalie)",
    "year": "year",
    "draft_pick": "draft pick #",
    "draft_keeper": "flag to indicate if player was kept from previous year as a keeper",
    "draft_price": "draft price",
    "draft_cap_percentage": "draft price as a percentage of the total draft cap for that year",
    "G": "goals",
    "A": "assist",
    "P_M": "plus/minus",
    "PTS": "points",
    "PIM": "penalty minutes",
    "PPG": "power play goals",
    "PPA": "power play assists",
    "SHG": "short handed goals",
    "SHA": "short handed assists",
    "GWG": "game winning goals",
    "FOW": "face-off wins",
    "FOL": "face-off losses",
    "_25": "???",
    "TTOI": "time on ice",
    "ATOI": "average time on ice",
    "HAT": "hat tricks",
    "SOG": "shots_on_goal",
    "HIT": "hits",
    "BLK": "blocks",
    "DEF": "defensemen points",
    "GP": "games played",
    "_35": "???",
    "_36": "???",
    "_37": "???",
    "PPP": "power play points",
    "SHP": "short handed points",
    "GS": "games started",
    "W": "wins",
    "L": "losses",
    "GA": "goals against",
    "SV": "saves",
    "SO": "shutouts",
    "OTL": "overtime losses",
    "MIN": "minutes played",
    "GAA": "goals against average",
    "SVP": "save percentage"
}

# defines player table schema for the sqlite database
sqlite_players_table = {
    "id": "INTEGER PRIMARY KEY",
    "name": "TEXT",
    "active": "INTEGER",
    "position_type": "TEXT",
    "position": "TEXT"
}

# defines draft table schema for the sqlite database
sqlite_players_draft = {
    "id": "INTEGER",
    "year": "INTEGER",
    "draft_pick": "INTEGER",
    "draft_keeper": "INTEGER",
    "draft_price": "INTEGER",
    "draft_cap_percentage": "REAL",
    "UNIQUE": "(id, year)",
    "PRIMARY KEY": "(id, year)",
    "FOREIGN KEY (id)": "REFERENCES players(id)",
    "FOREIGN KEY (year)": "REFERENCES draft_years(year)"
}

sqlite_draft_years = {
    "year": "INTEGER PRIMARY KEY",
    "draft_cap": "INTEGER"
}

# defines skaters scoring table schema for the sqlite database
sqlite_forwards_stats_table = {
    "id": "INTEGER",
    "year": "INTEGER",
    "stats_type": "TEXT",
    "G": "REAL",
    "A": "REAL",
    "P_M": "REAL",
    "PTS": "REAL",
    "PIM": "REAL",
    "PPG": "REAL",
    "PPA": "REAL",
    "SHG": "REAL",
    "SHA": "REAL",
    "GWG": "REAL",
    "FOW": "REAL",
    "FOL": "REAL",
    "TTOI": "REAL",
    "ATOI": "REAL",
    "HAT": "REAL",
    "SOG": "REAL",
    "GP": "REAL",
    "HIT": "REAL",
    "BLK": "REAL",
    "PRIMARY KEY": "(id, year, stats_type)",
    "FOREIGN KEY (id)": "REFERENCES players(id)"
}

# defines defencemen scoring table schema for the sqlite database
sqlite_defencemen_stats_table = {
    "id": "INTEGER",
    "year": "INTEGER",
    "stats_type": "TEXT",
    "G": "REAL",
    "A": "REAL",
    "P_M": "REAL",
    "PTS": "REAL",
    "PIM": "REAL",
    "PPG": "REAL",
    "PPA": "REAL",
    "SHG": "REAL",
    "SHA": "REAL",
    "GWG": "REAL",
    "FOW": "REAL",
    "FOL": "REAL",
    "TTOI": "REAL",
    "ATOI": "REAL",
    "HAT": "REAL",
    "SOG": "REAL",
    "GP": "REAL",
    "HIT": "REAL",
    "BLK": "REAL",
    "DEF": "REAL",
    "PRIMARY KEY": "(id, year, stats_type)",
    "FOREIGN KEY (id)": "REFERENCES players(id)"
}

# defines goalie scoring table schema for the sqlite database
sqlite_goalies_stats_table = {
    "id": "INTEGER",
    "year": "INTEGER",
    "stats_type": "TEXT",
    "GS": "REAL",
    "W": "REAL",
    "L": "REAL",
    "GA": "REAL",
    "SV": "REAL",
    "SO": "REAL",
    "OTL": "REAL",
    "MIN": "REAL",
    "GAA": "REAL",
    "SVP": "REAL",
    "PRIMARY KEY": "(id, year, stats_type)",
    "FOREIGN KEY (id)": "REFERENCES players(id)"
}

# defines years tracking table schema for the sqlite database
sqlite_years_tracking_table = {
    "year": "INTEGER",
    "data_type": "TEXT"
}
