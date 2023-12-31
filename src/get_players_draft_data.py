import argparse
from os.path import exists
from os import getcwd, chdir
from datetime import date
from typing import Tuple
import json
import espn_api
from src.espn_api_custom import League
# from espn_api_custom import League
import sqlite3
import traceback
from src import schemas
# import schemas

position_table_map = {
    'F': 'forwards_stats',
    'D': 'defencemen_stats',
    'G': 'goalies_stats',
}

def get_player_position(player) -> Tuple[str, str]:
    """
    Get the player's position letter and type.

    Args:
        player: The player object.

    Returns:
        Tuple[str, str]: A tuple containing the position letter and type.
    """
    if (player.position not in ['Goalie', 'Defense']):
        return 'F', 'Skater', position_table_map['F']
    elif player.position == 'Goalie':
        return 'G', 'Goalie', position_table_map['G']
    elif player.position == 'Defense':
        return 'D', 'Skater', position_table_map['D']

def get_args() -> argparse.Namespace:
    """
    Get command line arguments.

    Returns:
        argparse.Namespace: An object containing the command line arguments.
    """
    parser = argparse.ArgumentParser(description='Get credential values by logging into ESPN league, inspect page, '
                                                 'Application tab -> Storage -> Cookies -> "http://fantasy.espn.com". '
                                                 'Find required values in the list.')
    parser.add_argument('--league_id', type=int, help='Id of the fantasy league', required=True)
    parser.add_argument('--full_history', action='store_true', help='Flag to indicate that data needs to be requested from the beginning of time. \nDefault False\nHistory begins at 2019 as ESPN released a new API around that time, but users cannot request data for years it was not part of the league.')
    return parser.parse_args()

class DataPublisher:
    """
    Class to publish data to the database.
    """
    def __init__(self, league_id, year):
        if exists(f'espn-data/{league_id}'):
            self.league_id = league_id
            self.conn = sqlite3.connect(f'espn-data/{league_id}/league.db')
            self.auth = json.load(open(f'espn-data/{league_id}/auth.json', 'r'))
        else:
            print(f'Unable to locate data for League_id: {league_id}. \nSetup with "init-new-league.py"')
            exit(-1)

        self.year = year
        self.cursor = self.conn.cursor()
        self.league = self.get_league()
        self.draft = None
        self.fa = None
        self.forwards_stats_columns = set(sorted(self.get_table_column_names('forwards_stats')))
        self.defencemen_stats_columns = set(sorted(self.get_table_column_names('defencemen_stats')))
        self.goalies_stats_columns = set(sorted(self.get_table_column_names('goalies_stats')))

    def __del__(self):
        try:
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            pass

    def get_league(self) -> League:
        """
        Get a league object.

        Returns:
            League: The League object.
        """
        return League(league_id=self.league_id, espn_s2=self.auth['espn_s2'], swid=self.auth['swid'], year=self.year)
    
    def get_draft(self) -> list:
        """
        Get draft data.

        Returns:
            list: The draft data.
        """
        self.draft = self.league.espn_request.get_league_draft()
        return self.draft

    def get_fa(self) -> list:
        """
        Get free agents data.

        Returns:
            list: The free agents data.
        """
        self.fa = self.league.free_agents()
        return self.fa

    def get_table_column_names(self, table_name: str) -> list:
        """
        Get column names for a given table.

        Args:
            table_name (str): The name of the table.

        Returns:
            list: A list of column names.
        """
        self.cursor.execute(f'PRAGMA table_info({table_name})')
        return [column[1] for column in self.cursor.fetchall()]
    
    def publish_players_stats_data(self):
        """
        Publish players data to the database.
        """
        # add player to the players table
        # add players data to the players stats table based on position
        print(f'-' * 80)
        print(f'Publishing players data for year: {self.year} ...')
        for player in self.fa:
            try:
                stats = dict()
                transformed_stats = dict()
                src_columns = None
                dst_columns = None
                position_letter, position_type, position_stat_table_name = get_player_position(player)
                sql_command = str()
                # check player id exists in the players table and add if not
                self.cursor.execute(f"SELECT COUNT(*) FROM players WHERE id={player.playerId}")
                result = self.cursor.fetchone()
                if result[0] == 0:
                    self.cursor.execute(f'INSERT INTO players (id, name, active, position_type, position) VALUES ({player.playerId}, "{player.name}", 1,"{position_type}", "{position_letter}")')
                    self.conn.commit() 
                for key in [f'Total', 'Projected']:
                    try:
                        stats = player.stats[f'{key} {self.year}']['total']
                    except KeyError:
                        continue
                    try:
                        transformed_stats = {schemas.espn_to_sqlite_names[key]: value for key, value in stats.items()}
                    except Exception as e:
                        print('ERROR: Unable to map API stat name to the database column name.')
                        print(f'{player.playerId} - {player.name} - {key} - {self.year}')
                        print(e)
                        continue
                    transformed_stats['id'] = player.playerId
                    transformed_stats['year'] = self.year
                    transformed_stats['stats_type'] = key.lower()
                    
                    # make sure columns are the same in the table and in the data
                    src_columns = set(sorted(transformed_stats.keys()))
                    dst_columns = getattr(self, f'{position_stat_table_name}_columns')
                    if not src_columns.issubset(dst_columns):
                        missing_columns = src_columns - dst_columns
                        print(f'WARNING: Columns in the table "{position_stat_table_name}" and in the data are not the same.')
                        print(f'Columns in the table: {dst_columns}')
                        print(f'Columns in the data : {src_columns}')
                        print(f'Missing columns     : {missing_columns}')
                        print('Attempting to self-repair the database ...')
                        # add missing columns to the table
                        for column in missing_columns:
                            command = f'ALTER TABLE {position_stat_table_name} ADD COLUMN {column} REAL'
                            print(command)
                            self.cursor.execute(command)
                        self.conn.commit() 
                        setattr(self, f'{position_stat_table_name}_columns', set(sorted(self.get_table_column_names(position_stat_table_name))))
                        print(f'Columns in the table: {getattr(self, f"{position_stat_table_name}_columns")}')

                    self.sql_commit_insert_into_db(position_stat_table_name, transformed_stats)

            except Exception as e:
                print("UNHANDLED EXCEPTION while trying to publish players data.")
                print(e)
                print(traceback.format_exc())
                pass
        pass

    def publish_draft_years_data(self):
        """
        Publish draft years data for the current year.

        This method retrieves and publishes draft years data for the current year. It extracts the year and draft budget
        (draft_cap) from the league's draft settings and inserts this information into the 'draft_years' table in the database.

        """
        print(f'-' * 80)
        print(f'Publishing draft years data for year: {self.year} ...')
        draft = dict()
        draft['year'] = self.year
        draft['draft_cap'] = self.draft['settings']['draftSettings']['auctionBudget']
        self.sql_commit_insert_into_db('draft_years', draft)

    def publish_players_draft_data(self):
        """
        Publish players' draft data for the current year.

        This method retrieves and publishes data about players drafted in the current year. It iterates through the draft picks
        and collects information such as player ID, draft year, draft pick number, whether the player is a keeper, and the
        draft price. This data is then inserted into the 'players_draft' table in the database.

        """
        print(f'-' * 80)
        print(f'Publishing players draft data for year: {self.year} ...')
        if not self.draft['draftDetail']['drafted']:
            print(f'No draft data available for year {self.year}.')
            return
        for pick in self.draft['draftDetail']['picks']:
            data = dict()
            if pick['playerId'] == -1:
                continue
            data['id'] = pick['playerId']
            data['year'] = self.year
            data['draft_pick'] = pick['overallPickNumber']
            data['draft_keeper'] = pick['keeper']
            data['draft_price'] = pick['bidAmount']
            self.sql_commit_insert_into_db('players_draft', data)


    def sql_commit_insert_into_db(self, table_name: str, data: dict):
        """
        Execute an SQL INSERT command to insert data into a specified table in the database.

        Args:
            table_name (str): The name of the table where data will be inserted.
            data (dict): A dictionary containing column names as keys and their corresponding values.

        Raises:
            sqlite3.IntegrityError: If an integrity constraint violation occurs during the insertion.
                This can happen if there are duplicate entries that violate a UNIQUE constraint.

        """
        try:
            sql_command = generate_insert_sql(table_name, data)
            self.cursor.execute(sql_command, tuple(data.values()))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                print(f'WARNING: Duplicate data detected while INSERT into {table_name}. Skipping.')
                print(f'{data}')
                return
            print(f'ERROR: Unable to execute SQL command: {sql_command}')
            print(e)
            print(traceback.format_exc())
            raise


def generate_insert_sql(table_name: str, data_dict: dict) -> str:
    """
    Generate the SQL INSERT statement for inserting data into a table.

    Args:
        table_name (str): The name of the table.
        data_dict (dict): A dictionary containing column names as keys and their corresponding values.

    Returns:
        str: The SQL INSERT statement.
    """
    columns = ', '.join(data_dict.keys())
    placeholders = ', '.join(['?'] * len(data_dict))
    insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    return insert_sql

def get_years(full_history: bool) -> list:
    """
    Generate a list of years to get data about players for.
    It starts at 2019 due to the fact that the current API does not support earlier years.

    Args:
        full_history (bool): Flag indicating whether to retrieve data for the full history or not.

    Returns:
        list: A list of years to retrieve data for.
    """
    if full_history:
        init_year = 2019
    else:
        init_year = date.today().year
    current_year = date.today().year
    current_month = date.today().month

    # next year's season is generated by ESPN somewhere in August
    # predictions for the next season are generated by ESPN somewhere at the end of August - early September.
    # hence the range offset, otherwise if run during Jan - July
    # it would try to request data for the year that does not exist
    offset = 2
    if current_month in range(1, 7):
        offset = 1

    ret = list(range(init_year, current_year+offset))
    return ret

def set_cd_to_root():
    """
    Set the current working directory to the root of the project.
    """
    cwd = getcwd()
    if cwd.endswith('src'):
        chdir('..')

def main(league_id, full_history):
    set_cd_to_root()
    years = get_years(full_history)
    print(f'Getting data for the following years: {years}')
    for year in years:
        print(f'=' * 120)
        print(f'Updating data for year: {year}')
        try:
            publisher = DataPublisher(league_id, year)
            publisher.get_fa()
            publisher.publish_players_stats_data()
            publisher.get_draft()
            publisher.publish_draft_years_data()
            publisher.publish_players_draft_data()
            
            pass
        except espn_api.requests.espn_requests.ESPNInvalidLeague as ex:
            print(f'Error, unable to find league data for the year: {year}. Either league id is invalid, or data for this year is not available yet. \n')
            print(ex)
            continue
        except espn_api.requests.espn_requests.ESPNAccessDenied as ex:
            print(f'Error, authentication failed. Either the user does not have access to the specified year {year},\nor auth.json file needs to be updated with correct values. \n')
            print(ex)
            continue
        except Exception as ex:
            print(ex)
            print(traceback.format_exc())
            exit(-1)
        finally:
            try:
                del publisher
            except UnboundLocalError:
                pass

if __name__ == '__main__':
    args = get_args()
    main(args.league_id, args.full_history)
