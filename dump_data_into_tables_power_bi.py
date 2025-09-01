import sqlite3
import csv
from src import player_stats_to_tables_converter as player_stats_to_tables_converter
import os
import shutil

class DataPBIExporter:
    def __init__(self, league_id, year):
        self.league_id = league_id
        self.year = year
        self.league_home_dir = f'espn-data/{league_id}'
        self.conn = sqlite3.connect(f'espn-data/{league_id}/league.db')
        self.cursor = self.conn.cursor()
        self.csv_out_dir = self.clean_csv_dumps_dir()
        # get data from the database
        data_obj = player_stats_to_tables_converter.PlayersStatsTableDataGenerator(league_id, year)
        self.data_years = data_obj.years_to_use
        self.formatted_players_data = data_obj.full_stats
        
        self.players_column_names = ['id', 'name', 'position', 'selected']
        self.forwards_stats_column_names = data_obj.tables_headers['forwards_stats']
        self.forwards_stats_column_names.append('FP')
        self.forwards_stats_column_names.append('FP_AVG')
        
        self.defencemen_stats_column_names = data_obj.tables_headers['defencemen_stats']
        self.defencemen_stats_column_names.append('FP')
        self.defencemen_stats_column_names.append('FP_AVG')
        
        self.goalies_stats_column_names = data_obj.tables_headers['goalies_stats']
        self.goalies_stats_column_names.append('FP')
        self.goalies_stats_column_names.append('FP_AVG')

        self.skater_summary_column_names = ['id', 'name', 'year', 'proj_vs_act_FP', 'proj_vs_act_FP_AVG', 'proj_vs_act_ATOI', 'proj_vs_act_STP', 'proj_vs_act_GP', 'proj_vs_act_PROD']
        self.goalie_summary_column_names = ['id', 'name', 'year', 'proj_vs_act_FP', 'proj_vs_act_FP_AVG', 'proj_vs_act_GS', 'proj_vs_act_W', 'proj_vs_act_GAA', 'proj_vs_act_SVP']
        

    def clean_csv_dumps_dir(self):
        """
        Creates a directory for CSV output files.
        This method removes the existing 'dumps' directory within the league's home directory
        and then creates a new 'dumps' directory. It returns the path to the newly created
        'dumps' directory.
        Returns:
            str: The path to the newly created 'dumps' directory.
        """

        dumps = f'{self.league_home_dir}/dumps'
        try:
            shutil.rmtree(dumps)
        except FileNotFoundError:
            pass
        os.makedirs(dumps)
        return dumps
    
    def dump_stats_data(self):
        """
        Dumps player statistics data into CSV files for use in Power BI.
        This method processes formatted player data, categorizes it by player position 
        (forwards, defencemen, goalies), and writes both summary and full statistics 
        to CSV files.
        Summary data includes:
        - Player ID
        - Player name
        - Year
        - Projected vs Actual Fantasy Points (FP)
        - Projected vs Actual Average Fantasy Points (FP_AVG)
        - Projected vs Actual Average Time on Ice (ATOI) for skaters or Games Started (GS) for goalies
        Full statistics data includes:
        - Projected and actual statistics for each player and year
        The method writes the following CSV files:
        - f_summary.csv: Summary data for forwards
        - d_summary.csv: Summary data for defencemen
        - g_summary.csv: Summary data for goalies
        - forwards_stats.csv: Full statistics for forwards
        - defencemen_stats.csv: Full statistics for defencemen
        - goalies_stats.csv: Full statistics for goalies
        Raises:
            ValueError: If a player's position is invalid.
        """
        players = list()
        forwards_summary = list()
        defencemen_summary = list()
        goalies_summary = list()
        forwards_full_stats = list()
        defencemen_full_stats = list()
        goalies_full_stats = list()
        # self.skater_summary_column_names = ['id', 'name', 'year', 'proj_vs_act_FP', 'proj_vs_act_FP_AVG', 'proj_vs_act_ATOI', proj_vs_act_STP, proj_vs_act_GP, proj_vs_act_PROD]
        # self.goalie_summary_column_names = ['id', 'name', 'year', 'proj_vs_act_FP', 'proj_vs_act_FP_AVG', 'proj_vs_act_GS', proj_vs_act_W, proj_vs_act_GAA, proj_vs_act_SV%]
        for player in self.formatted_players_data:
            active_flag = self.is_player_active(player)
            if active_flag:
                player_row = list([player[self.players_column_names[0]], player[self.players_column_names[1]], player[self.players_column_names[2]], ''])
                players.append(player_row)
            else:
                continue

            for year in player['stats']:
                # Create a rows for the player
                full_stats_projected_row = self.get_players_stats_row(player, year, 'projected')
                full_stats_actual_row = self.get_players_stats_row(player, year, 'actual')
                summary_row = list()
                summary_row.append(player['id'])
                summary_row.append(player['name'])
                summary_row.append(year)
                
                try:
                    projected_fp = round(player['stats'][year]['projected']['FP'], 2)
                except TypeError:
                    projected_fp = ''

                try:
                    actual_fp = round(player['stats'][year]['actual']['FP'], 2)
                except TypeError:
                    actual_fp = ''
                
                # add projected and actual FP to the row
                summary_row.append(f'{projected_fp} | {actual_fp}')

                try:
                    projected_fp_avg = round(player['stats'][year]['projected']['FP_AVG'], 2)
                except TypeError:
                    projected_fp_avg = ''
                
                try:
                    actual_fp_avg = round(player['stats'][year]['actual']['FP_AVG'], 2)
                except TypeError:
                    actual_fp_avg = ''
                
                # add projected and actual FP_AVG to the row
                summary_row.append(f'{projected_fp_avg} | {actual_fp_avg}')

                if (player['position'] != 'G'):
                    try:
                        projected_atoi = round(player['stats'][year]['projected']['ATOI']/60, 2)
                    except TypeError:
                        projected_atoi = ''

                    try:
                        actual_atoi = round(player['stats'][year]['actual']['ATOI']/60, 2)
                    except TypeError:
                        actual_atoi = ''
                    summary_row.append(f'{projected_atoi} | {actual_atoi}')

                    try:
                        projected_stp = int(player['stats'][year]['projected']['STP'])
                    except TypeError:
                        projected_stp = ''
                    try:
                        actual_stp = int(player['stats'][year]['actual']['STP'])
                    except TypeError:
                        actual_stp = ''
                    summary_row.append(f'{projected_stp} | {actual_stp}')

                    try:
                        projected_gp = int(player['stats'][year]['projected']['GP'])
                    except TypeError:
                        projected_gp = ''
                    try:
                        actual_gp = int(player['stats'][year]['actual']['GP'])
                    except TypeError:
                        actual_gp = ''
                    summary_row.append(f'{projected_gp} | {actual_gp}')

                    try:
                        projected_prod = round(player['stats'][year]['projected']['TTOI'] / 60 / player['stats'][year]['projected']['PTS'], 2)
                    except (TypeError, ZeroDivisionError):
                        projected_prod = ''
                    try:
                        actual_prod = round(player['stats'][year]['actual']['TTOI'] / 60 / player['stats'][year]['actual']['PTS'], 2)
                    except (TypeError, ZeroDivisionError):
                        actual_prod = ''
                    summary_row.append(f'{projected_prod} | {actual_prod}')

                else:
                    try:
                        projected_gs = int(player['stats'][year]['projected']['GS'])
                    except TypeError:
                        projected_gs = ''

                    try:
                        actual_gs = int(player['stats'][year]['actual']['GS'])
                    except TypeError:
                        actual_gs = ''                  
                    summary_row.append(f'{projected_gs} | {actual_gs}')
                    # TODO add combo goalies for 'W %% (W/GS*100), 'GAA (GoalsAgainstAverage)', 'SV% (SavePercentage)'

                    try:
                        projected_w = round(player['stats'][year]['projected']['W'] / player['stats'][year]['projected']['GS'] * 100, 2)
                    except (TypeError, ZeroDivisionError):
                        projected_w = ''
                    try:
                        actual_w = round(player['stats'][year]['actual']['W'] / player['stats'][year]['actual']['GS'] * 100, 2)
                    except (TypeError, ZeroDivisionError):
                        actual_w = ''
                    summary_row.append(f'{projected_w} | {actual_w}')

                    try:
                        projected_gaa = round(player['stats'][year]['projected']['GAA'], 2)
                    except TypeError:
                        projected_gaa = ''
                    try:
                        actual_gaa = round(player['stats'][year]['actual']['GAA'], 2)
                    except TypeError:
                        actual_gaa = ''
                    summary_row.append(f'{projected_gaa} | {actual_gaa}')

                    try:
                        projected_svp = round(player['stats'][year]['projected']['SVP'], 2)
                    except TypeError:
                        projected_svp = ''
                    try:
                        actual_svp = round(player['stats'][year]['actual']['SVP'], 2)
                    except TypeError:
                        actual_svp = ''
                    summary_row.append(f'{projected_svp} | {actual_svp}')

                match player['position']:
                    case 'F':
                        forwards_full_stats.append(full_stats_projected_row)
                        forwards_full_stats.append(full_stats_actual_row)
                        forwards_summary.append(summary_row)
                    case 'D':
                        defencemen_full_stats.append(full_stats_projected_row)
                        defencemen_full_stats.append(full_stats_actual_row)
                        defencemen_summary.append(summary_row)
                    case 'G':
                        goalies_full_stats.append(full_stats_projected_row)
                        goalies_full_stats.append(full_stats_actual_row)
                        goalies_summary.append(summary_row)
                    case _:
                        raise ValueError("Invalid position")
        
        # dump data into csv files
        self.csv_writer(f'{self.csv_out_dir}/players.csv', self.players_column_names, players)

        self.csv_writer(f'{self.csv_out_dir}/f_summary.csv', self.skater_summary_column_names, forwards_summary)
        self.csv_writer(f'{self.csv_out_dir}/d_summary.csv', self.skater_summary_column_names, defencemen_summary)
        self.csv_writer(f'{self.csv_out_dir}/g_summary.csv', self.goalie_summary_column_names, goalies_summary)

        self.csv_writer(f'{self.csv_out_dir}/f_stats.csv', self.forwards_stats_column_names, forwards_full_stats)
        self.csv_writer(f'{self.csv_out_dir}/d_stats.csv', self.defencemen_stats_column_names, defencemen_full_stats)
        self.csv_writer(f'{self.csv_out_dir}/g_stats.csv', self.goalies_stats_column_names, goalies_full_stats)

    def export_table_to_csv(self, table_name):
        """
        Exports the contents of a specified database table to a CSV file.
        Args:
            table_name (str): The name of the table to export.
        Raises:
            Exception: If there is an error executing the SQL query or writing to the CSV file.
        The CSV file will be saved in the directory specified by `self.csv_out_dir` with the
        filename format '{table_name}.csv'. The first row of the CSV file will contain the
        column names, followed by the table data.
        """

        csv_dump_file = f'{self.csv_out_dir}/{table_name}.csv'

        # Query to select all data from the table
        query = f"SELECT * FROM {table_name}"
        
        # Execute the query
        self.cursor.execute(query)
        
        # Get the column names from the cursor description
        column_names = [description[0] for description in self.cursor.description]
        
        # Fetch all rows from the table
        rows = self.cursor.fetchall()

        # Write data to CSV
        with open(csv_dump_file, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)
            writer.writerows(rows)
        

    def is_player_active(self, player):
        """
        For player to be considered active:
            + need to have TTOI in last OR second last sesaons > 0 
            or need to have FP projected for current season
        Args:
            player (dict): A dictionary containing player information, including 'status'.
        Returns:
            bool: True if the player is active, False otherwise.
        """
        flag = False
        try:
            if player['stats'][self.data_years[-1]]['projected']['FP'] > 0:
                flag = True
        except TypeError:
            pass
        
        try:
            if player['stats'][self.data_years[-2]]['actual']['FP'] > 0:
                flag = True
        except TypeError:
            pass

        try:
            if player['stats'][self.data_years[-2]]['projected']['FP'] > 0:
                flag = True
        except TypeError:
            pass
        return flag

    def get_players_stats_row(self, player, year, stats_type):
        """
        Generates a row of player statistics for a given year and stats type.
        Args:
            player (dict): A dictionary containing player information, including 'id', 'position', and 'stats'.
            year (int): The year for which the statistics are being retrieved.
            stats_type (str): The type of statistics to retrieve (e.g., 'regular', 'playoff').
        Returns:
            list: A list containing the player's id, year, stats type, and the corresponding statistics.
              If the statistics for the given year and type are not available, empty strings are appended
              for each missing statistic.
        Raises:
            ValueError: If the player's position is invalid.
        """

        ret_row = list()
        keys = list()
        filtered_keys = list()

        match player['position']:
            case 'F':
                keys = self.forwards_stats_column_names
            case 'D':
                keys = self.defencemen_stats_column_names
            case 'G':
                keys = self.goalies_stats_column_names
            case _:
                raise ValueError("Invalid position")
        
        
        ret_row.append(player['id'])
        ret_row.append(year)
        ret_row.append(stats_type)
        
        filtered_keys = [item for item in keys if item not in ['id', 'year', 'stats_type']]

        if player['stats'][year][stats_type]:
            stats = player['stats'][year][stats_type]
            for key in filtered_keys:
                try:
                    ret_row.append(round(stats[key], 2))
                except TypeError:
                    ret_row.append('')
        else:
            for key in filtered_keys:
                ret_row.append('')
        
        return ret_row
    
    def csv_writer(self, csv_file_path, column_names, data):
        """
        Writes data to a CSV file.
        Args:
            csv_file (str): The path to the CSV file.
            data (list): A list of lists containing the data to write to the CSV file.
        Returns:
            None
        """
        with open(csv_file_path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)
            writer.writerows(data)

    def close_connection(self):
        # Close the connection
        self.conn.close()

    def __del__(self):
        # Close the connection when the object is deleted
        self.close_connection()



def main(league_id, year):
    # dump data into tables for Power BI
    # target is t output following tables
    # following tables as csv files: players, forwards_stats, defencemen_stats, goalies_stats
    # combined data for multiline sparkle charts: f_summary, d_summary, g_summary

    exporter_obj = DataPBIExporter(league_id, year)
    exporter_obj.dump_stats_data()
 

if __name__ == '__main__':
    league_id = 41610
    year = 2026
    main(league_id, year)  