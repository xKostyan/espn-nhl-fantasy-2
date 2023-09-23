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
    "TTOI ?": "TTOI",
    "ATOI": "ATOI",
    "GP": "GP",
    "5": "_5",
    "12": "_12",
    "16": "PTS",
    "25": "_25",
    "30": "GP",
    "35": "_35",
    "36": "_36",
    "37": "_37",
    "99": "_99",
    "+/-": "P_M",
    "PPP": "PPP",
    "SHP": "SHP",
    "GS": "GS",
    "W": "W",
    "L": "L",
    "SA": "SA",
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
    "TTOI": "time on ice",
    "ATOI": "average time on ice",
    "HAT": "hat tricks",
    "SOG": "shots_on_goal",
    "HIT": "hits",
    "BLK": "blocks",
    "DEF": "defensemen points",
    "GP": "games played",
    "_5": "???",
    "_12": "???",
    "_16": "points",
    "_25": "???",
    "_35": "???",
    "_36": "???",
    "_37": "???",
    "_99": "???",
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
    "UNIQUE": "(id, year)",
    "PRIMARY KEY": "(id, year)",
    "FOREIGN KEY (id)": "REFERENCES players(id)",
    "FOREIGN KEY (year)": "REFERENCES draft_years(year)"
}

sqlite_draft_years = {
    "year": "INTEGER PRIMARY KEY",
    "draft_cap": "INTEGER"
}

sqlite_forwards_stats_table = {
    "id": "INTEGER",
    "year": "INTEGER",
    "stats_type": "TEXT",
    "PRIMARY KEY": "(id, year, stats_type)",
    "FOREIGN KEY (id)": "REFERENCES players(id)",
    "FOREIGN KEY (year)": "REFERENCES draft_years(year)"
}

sqlite_defencemen_stats_table = {
    "id": "INTEGER",
    "year": "INTEGER",
    "stats_type": "TEXT",
    "PRIMARY KEY": "(id, year, stats_type)",
    "FOREIGN KEY (id)": "REFERENCES players(id)",
    "FOREIGN KEY (year)": "REFERENCES draft_years(year)"
}

sqlite_goalies_stats_table = {
    "id": "INTEGER",
    "year": "INTEGER",
    "stats_type": "TEXT",
    "PRIMARY KEY": "(id, year, stats_type)",
    "FOREIGN KEY (id)": "REFERENCES players(id)",
    "FOREIGN KEY (year)": "REFERENCES draft_years(year)"
}

# defines years tracking table schema for the sqlite database
sqlite_years_tracking_table = {
    "year": "INTEGER",
    "data_type": "TEXT"
}
