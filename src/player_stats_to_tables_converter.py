import sqlite3


# class that would be used to generate data and out put it to a Power BI friendly format
# class need to be able to connect to league.db and pull data from the tables
# class need to have league_id, year as inputs to connect to a specific league db and year is used to format output data
# at the end need to have 3 spread sheets: forwards, defensemen, goalies

class PlayersStatsTableDataGenerator:
    def __init__(self, league_id, year):
        self.current_year = year
        self.conn = sqlite3.connect(f'espn-data/{league_id}/league.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.years_to_use = []

        self.get_table_headers()
        self.get_scoring()
        self.get_tracked_years()
        self.get_players()
        self.get_full_data()

        self.close_connection()

    def get_tracked_years(self):
        """
        Retrieves distinct years from the 'years_tracking' table and stores them in the 'years_to_use' attribute.
        - Executes a SQL query to fetch distinct years.
        - Extracts the years from the query results.
        - If more than 5 years are retrieved, only the last 5 years are kept.
        Returns:
            None
        """

        # Execute the query to get distinct years
        self.cursor.execute("SELECT DISTINCT year FROM years_tracking")
        
        # Fetch all results
        years = self.cursor.fetchall()
                
        # Extract years from the fetched results and return as a list
        self.years_to_use = [year[0] for year in years]
        # If there are more than 5 years, keep only the last 5
        if len(self.years_to_use) > 5:
            self.years_to_use = self.years_to_use[-5:]

    def get_players(self):
        """
        Retrieves player information from the database.
        Executes a SQL query to fetch the id, name, and position of all players
        from the players table and stores the results in the `self.players` attribute.
        Returns:
            None
        """

        # Execute the query to get id, name, and position from players table
        self.cursor.execute("SELECT id, name, position FROM players")
        
        # Fetch all results
        self.players = self.cursor.fetchall()

    def get_full_data(self):
        """
        Retrieves the full statistical data for each player in the `self.players` list.
        For each player, the method constructs a dictionary containing the player's ID, name, 
        position, and a nested dictionary of statistics for each year specified in `self.years_to_use`.
        The statistics include both projected and actual stats, which are fetched from the database.
        Raises:
            ValueError: If the player's position is not 'F', 'D', or 'G'.
        Returns:
            list: A list of dictionaries, each containing the full statistical data for a player.
        """

        self.full_stats = []
        for player in self.players:
            player_id = player[0]
            name = player[1]
            position = player[2]

            player_full_data = {
                'id': player_id,
                'name': name,
                'position': position,
                'stats': {}
            }

            for year in self.years_to_use:
                player_full_data['stats'][year] = {
                    'projected': None,
                    'actual': None
                }
                # Determine the table name based on the player's position
                table_name = None
                match position:
                    case 'F':
                        table_name = 'forwards_stats'
                    case 'D':
                        table_name = 'defencemen_stats'
                    case 'G':
                        table_name = 'goalies_stats'
                    case _:
                        raise ValueError("Invalid position")

                # Execute the query to get the player's stats for the year
                # and stats type (projected or total)

                self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = ? AND year = ? and stats_type = ?", (player_id, year, 'projected'))
                projected_row = self.cursor.fetchone()
                if(projected_row):
                    stats = dict(projected_row)
                    player_full_data['stats'][year]['projected'] = self.get_calculated_points(stats, position)
                
                self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = ? AND year = ? and stats_type = ?", (player_id, year, 'total'))
                actual_row = self.cursor.fetchone()
                if(actual_row):
                    stats = dict(actual_row)
                    player_full_data['stats'][year]['actual'] = self.get_calculated_points(stats, position)
            
            self.full_stats.append(player_full_data)
                
    def get_table_headers(self):
        """
        Retrieves the column names from the specified table.
        Args:
            table_name (str): The name of the table from which to retrieve column names.
        Returns:
            list: A list of column names.
        """
        # Execute the query to get column names from the specified table
        self.tables_headers = {}
        for table_name in [ 'draft_years', 'forwards_stats', 'defencemen_stats', 'goalies_stats']:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
        
            # Fetch all results
            columns_info = self.cursor.fetchall()
            
            # Extract column names from the fetched results
            column_names = [column[1] for column in columns_info]
            self.tables_headers[table_name] = column_names

    def get_scoring(self):
        """
        Retrieves the first row from the 'scoring' table and returns it as a dictionary.
        Returns:
            dict: A dictionary where the key is the column name and the value is the cell value.
        """
        self.cursor.execute("SELECT * FROM scoring LIMIT 1")
        row = self.cursor.fetchone()
        if row:
            self.scoring = dict(row)
        else:
            raise ValueError("No scoring data found")
        
    def get_calculated_points(self, player_stats, position):
        """
        Calculate fantasy points for a player based on their statistics and position.
        Args:
            player_stats (dict): A dictionary containing the player's statistics.
            position (str): The position of the player ('F' for Forward, 'D' for Defenseman, 'G' for Goalie).
        Returns:
            dict: A dictionary containing the original player statistics with added fantasy points ('FP') 
              and average fantasy points per game/started game ('FP_AVG').
        Raises:
            ValueError: If the provided position is not 'F', 'D', or 'G'.
        """

        tmp_dict = dict(player_stats)
        match position:
            case 'F':
                scoring_keys = ["G", "A", "PIM", "PPG", "PPA", "SHG", "SHA", "GWG", "HAT", "SOG", "HIT", "BLK"]
                denominator = 'GP'
            case 'D':
                scoring_keys = ["G", "A", "PIM", "PPG", "PPA", "SHG", "SHA", "GWG", "HAT", "SOG", "HIT", "BLK", "DEF"] 
                denominator = 'GP'
            case 'G':
                scoring_keys = ["W", "L", "GA", "SV", "SO", "OTL"]
                denominator = 'GS'
            case _:
                raise ValueError("Invalid position")

        fp = 0
        for key in scoring_keys:
            if tmp_dict[key]:
                fp += tmp_dict[key] * self.scoring[key]
        tmp_dict['FP'] = fp
        if tmp_dict[denominator]:
            fp_avg = fp / tmp_dict[denominator]
        else:
            fp_avg = None
        tmp_dict['FP_AVG'] = fp_avg
        return tmp_dict

    def close_connection(self):
        # Close the connection
        self.conn.close()

    def __del__(self):
        # Close the connection when the object is deleted
        self.close_connection()


