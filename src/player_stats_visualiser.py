import tkinter as tk
from tkinter import ttk
import data_processor

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NHL Players Stats Visualiser")
        self.root.geometry("800x600")

        self.league_id = None
        self.year = []

        self.select_league_id()

    def select_league_id(self):
        def save_next():
            self.league_id = self.tk_selected_id.get()
            del self.tk_selected_id
            self.select_year()

        self.leagues = data_processor.get_existing_leagues()
        self.clear_window()
        self.tk_selected_id = tk.StringVar()

        label = tk.Label(self.root, text="Select League Id")
        label.pack(pady=10)

        # Create dropdown menu
        dropdown = tk.OptionMenu(self.root, self.tk_selected_id, *self.leagues)
        dropdown.pack(pady=10)

        # Next button to go to the next screen
        next_button = tk.Button(self.root, text="Next", command=save_next)
        next_button.pack(pady=20)

    def select_year(self):
        def save_next():
            self.year = self.year_map[self.tk_selected_year.get()]
            del self.tk_selected_year
            del self.year_map
            self.players_main_menu()
        self.years = data_processor.get_existing_years(self.league_id)
        self.year_map = {str(year): year for year in self.years}

        self.clear_window()
        label1 = tk.Label(self.root, text=f"League ID: {self.league_id}")
        label1.pack(pady=5)
        label2 = tk.Label(self.root, text=f"Select data source:")
        label2.pack(pady=5)

        # Create dropdown menu
        self.tk_selected_year = tk.StringVar()
        dropdown = tk.OptionMenu(self.root, self.tk_selected_year, *self.year_map.keys())
        dropdown.pack(pady=10)
        next_button = tk.Button(self.root, text="Next", command=save_next)
        next_button.pack(pady=20)

    def players_main_menu(self):
        self.clear_window()
        label1 = tk.Label(self.root, text=f"Stats visualiser for League ID {self.league_id}\n{self.year[0]} {self.year[1]}")
        label1.pack(pady=10)

        # generate table data for skaters
        # generate table data for goalies
        # generate buttons for F, D, G

    # def create_screen4(self):
    #     self.clear_window()
    #     label = tk.Label(self.root, text="Screen4 placeholder")
    #     label.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
