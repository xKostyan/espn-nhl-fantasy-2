from src import get_players_draft_data as get_players_draft_data
from src import init_league as init_league
import os

def option_one():
    """
    Placeholder function for option one.
    """
    print()
    
    print('Initializing new league ...')
    league_id = init_league.main()
    print('Populating league database ...')
    get_players_draft_data.main(league_id, True)
    print("\nDone.")
    exit(0)

def option_two():
    """
    Placeholder function for option two.
    """
    print()
    leagues = get_existing_leagues()
    if len(leagues) == 0:
        print("No existing leagues found.")
        return
    
    print("Select a league:")
    for i, league in enumerate(leagues):
        print(f"{i+1}. {league}")
    choice = input("\n:")
    league_interactions_menu(leagues[int(choice)-1])
    # get_players_draft_data.main(leagues[int(choice)-1], False)
    # print("\nDone.")
    exit(0)

def league_interactions_menu(league_id):
    # 1. update selected league data
    # 2. refresh leagues authentication
    # 3. players prices adjustment
    # 4. quit
    print("\nSelect an option:")
    print("1. Update selected league data")
    print("2. Refresh leagues authentication")
    print("3. Players prices adjustment")
    print("4. Quit")
    choice = input("\n:")
    match choice:
        case '1':
            get_players_draft_data.main(league_id, False)
        case '2':
            auth = dir()
            auth = init_league.get_league_auth(league_id)
            init_league.save_league_auth(auth)
            league_interactions_menu(league_id)
        case '3':
            print("Not implemented yet.")
        case '4':
            print("Goodbye!")
            exit(0)
        case _:
            print("Invalid choice. Try again.")
            league_interactions_menu(league_id)


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


def main():
    while True:
        print("\nSelect an option:")
        print("1. Init a new league")
        print("2. Interact with existing league")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            option_one()
        elif choice == '2':
            option_two()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()