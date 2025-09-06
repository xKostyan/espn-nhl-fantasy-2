import os
import sqlite3


def get_existing_leagues() -> list:
    """
    Get a list of existing leagues.
    """
    folder_list = []
    data_folder = 'espn-data'
    try:
        # List all items in the specified directory
        items = os.listdir(data_folder)
        
        for item in items:
            item_path = os.path.join(data_folder, item)
            
            # Check if the item is a directory
            if os.path.isdir(item_path):
                folder_list.append(item)

    except OSError as e:
        print(f"Error: {e}")

    return folder_list

def get_existing_years(league_id) -> list:
    """
    Get a list of existing years for a given league.
    """
    # Connect to the database
    conn = sqlite3.connect(f'espn-data/{league_id}/league.db')
    
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # Execute a query to get the existing years
    cursor.execute("SELECT DISTINCT year, stats_type FROM years_tracking")
    
    # Fetch all the rows returned by the query and conver to list of lists
    rows = [list(row) for row in cursor.fetchall()]
        
    # Close the cursor and the connection
    cursor.close()
    conn.close()
    
    return rows

def get_skaters_main_table_data(league_id, year, stats_type) -> dict:
    pass


if __name__ == "__main__":
    get_existing_years('41610')