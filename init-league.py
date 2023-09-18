from src import schemas
import sqlite3
import ast
from os import makedirs


def init_db(league_id):
    # TODO check if league exists, if not create it
    # TODO create a db with the league data, store it in the folder espn-data/league_id/league.db
    try:
        makedirs(f'espn-data/{league_id}')
    except FileExistsError:
        pass
    conn = sqlite3.connect(f'espn-data/{league_id}/league.sqlite')
    cursor = conn.cursor()

    scoring_table = {value: "REAL" for value in schemas.espn_to_sqlite_names.values()}
    cursor.execute(get_create_table_command('scoring', scoring_table))
    cursor.execute(get_create_table_command('players', schemas.sqlite_players_table))
    cursor.execute(get_create_table_command('player_draft', schemas.sqlite_players_draft))
    cursor.execute(get_create_table_command('skater_stats', schemas.sqlite_forwards_stats_table))
    cursor.execute(get_create_table_command('defencemen_stats', schemas.sqlite_defencemen_stats_table))
    cursor.execute(get_create_table_command('goalie_stats', schemas.sqlite_goalies_stats_table))
    conn.commit()


def get_create_table_command(table_name, table_schema):
    args = ', '.join([f'{key} {value}' for key, value in table_schema.items()])
    command = f'CREATE TABLE IF NOT EXISTS {table_name} ({args});'
    print(command)
    return command


def input_detect(_prompt):
    val = None
    try:
        val = ast.literal_eval(input(_prompt))
    except SyntaxError:
        val = 0
    except ValueError:
        print('Invalid input. Must be a number, try again.')
        val = ast.literal_eval(input(_prompt))
    finally:
        return val    


def get_inputs():
    league = dict()
    league['league_id'] = int(input('League id: '))
    league['league_name'] = input('League name: ')
    league['scoring'] = dict()
    print('Enter league scoring for each category.')
    print('If a category is not used, enter 0 or leave it empty.')
    print('Make sure to align it with league setting on ESPN as some stat values are '
          '"products of other stats" and dont have own scoring value.')
    # TODO uncomment this
    # for key, value in schemas.espn_to_sqlite_names.items():
    #     league['scoring'][value] = input_detect(f'{value:<5} {schemas.sqlite_column_descriptions[value]:<30}: ')

    return league


def main():
    data = get_inputs()
    init_db(data['league_id'])


if __name__ == '__main__':
    main()
