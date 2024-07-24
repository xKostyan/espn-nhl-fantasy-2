import tkinter as tk
from tkinter import ttk
import data_processor

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NHL Players Stats Visualiser")
        self.root.geometry("800x600")
        self.leagues = data_processor.get_existing_leagues()
        self.years = []
        self.league_id = None
        self.year = None

        self.select_league_id()

    def select_league_id(self):
        def save_next():
            self.league_id = self.tk_selected_id.get()
            del self.tk_selected_id
            self.create_screen2()

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
        self.clear_window()
        label = tk.Label(self.root, text=f"Selected league id: {self.league_id}")
        label.pack(pady=10)
        # next_button = tk.Button(self.root, text="Next", command=self.create_screen3)
        # next_button.pack(pady=20)

    # def create_screen3(self):
    #     self.clear_window()
    #     label = tk.Label(self.root, text="Screen3 placeholder")
    #     label.pack(pady=10)
    #     next_button = tk.Button(self.root, text="Next", command=self.create_screen4)
    #     next_button.pack(pady=20)

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
