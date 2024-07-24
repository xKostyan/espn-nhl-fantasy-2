import os


def get_existing_leagues():
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