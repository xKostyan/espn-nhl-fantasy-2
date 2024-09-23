from src import player_stats_to_tables_converter as player_stats_to_tables_converter

def main():
    obj = player_stats_to_tables_converter.PlayersStatsTablesGenerator(league_id=41610, year=2025)
    
    # Fetch unique years
    obj.get_table_headers()
    obj.get_scoring()
    obj.get_tracked_years()
    obj.get_players()
    obj.get_full_data()
    pass
    
    

if __name__ == '__main__':
    main()  