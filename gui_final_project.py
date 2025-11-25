from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import sqlite3

class DB:
    def __init__(self, path):
        self.path = path
        self.create_table()
    
    def create_table(self):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                species TEXT NOT NULL,
                nickname TEXT NOT NULL,
                type TEXT NOT NULL,
                pokeball TEXT NOT NULL,
                location TEXT NOT NULL,
                region TEXT NOT NULL,
                level INTEGER NOT NULL,
                hp INTEGER NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, parameters=()):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()
        conn.close()
    
    def fetch_all(self, query, parameters=()):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        rows = cursor.fetchall()
        conn.close()
        return rows

path = "final_project_db.db"
db = DB(path)

# Create window
root = Tk()
root.title("Pokémon Database")
root.geometry("900x600")

# Title
title_label = Label(root, text="Pokémon Database Manager", font=("Helvetica", 16))
title_label.pack(pady=10)

# Main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Left frame - Form
left_frame = LabelFrame(main_frame, text="Pokémon Data", padx=10, pady=10)
left_frame.pack(side=LEFT, fill=Y, padx=5)

# Right frame - List
right_frame = LabelFrame(main_frame, text="All Pokémon", padx=10, pady=10)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)

# Form variables
species_var = StringVar()
nickname_var = StringVar()
type_var = StringVar()
pokeball_var = StringVar()
location_var = StringVar()
region_var = StringVar()
level_var = IntVar()
hp_var = IntVar()

# Form fields
# Row 0
Label(left_frame, text="Species Name:").grid(row=0, column=0, sticky='w', pady=5)
Entry(left_frame, textvariable=species_var, width=20).grid(row=0, column=1, pady=5)

# Row 1
Label(left_frame, text="Nickname:").grid(row=1, column=0, sticky='w', pady=5)
Entry(left_frame, textvariable=nickname_var, width=20).grid(row=1, column=1, pady=5)

# Row 2 - Type (OptionMenu)
Label(left_frame, text="Type:").grid(row=2, column=0, sticky='w', pady=5)
types = ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 
         'Poison', 'Ground', 'Flying', 'Bug', 'Rock', 'Ghost', 'Dragon', 
         'Dark', 'Steel', 'Fairy']
type_menu = OptionMenu(left_frame, type_var, *types)
type_menu.grid(row=2, column=1, pady=5)
type_var.set('Normal')

# Row 3 - Pokéball (OptionMenu)
Label(left_frame, text="Pokéball Type:").grid(row=3, column=0, sticky='w', pady=5)
pokeballs = ['Poké Ball', 'Great Ball', 'Ultra Ball', 'Master Ball', 'Quick Ball']
pokeball_menu = OptionMenu(left_frame, pokeball_var, *pokeballs)
pokeball_menu.grid(row=3, column=1, pady=5)
pokeball_var.set('Poké Ball')

# Row 4 - Location (OptionMenu)
Label(left_frame, text="Capture Location:").grid(row=4, column=0, sticky='w', pady=5)
locations = ['Route 1', 'Forest', 'Cave', 'City', 'Mountain', 'Beach']
location_menu = OptionMenu(left_frame, location_var, *locations)
location_menu.grid(row=4, column=1, pady=5)
location_var.set('Route 1')

# Row 5 - Region (OptionMenu)
Label(left_frame, text="Region:").grid(row=5, column=0, sticky='w', pady=5)
regions = ['Kanto', 'Johto', 'Hoenn', 'Sinnoh', 'Unova']
region_menu = OptionMenu(left_frame, region_var, *regions)
region_menu.grid(row=5, column=1, pady=5)
region_var.set('Kanto')

# Row 6 - Level
Label(left_frame, text="Level:").grid(row=6, column=0, sticky='w', pady=5)
Entry(left_frame, textvariable=level_var, width=20).grid(row=6, column=1, pady=5)

# Row 7 - HP
Label(left_frame, text="HP:").grid(row=7, column=0, sticky='w', pady=5)
Entry(left_frame, textvariable=hp_var, width=20).grid(row=7, column=1, pady=5)

# Buttons
button_frame = Frame(left_frame)
button_frame.grid(row=8, column=0, columnspan=2, pady=20)

Button(button_frame, text="Add Pokémon", width=15).pack(pady=5)
Button(button_frame, text="Update Pokémon", width=15).pack(pady=5)
Button(button_frame, text="Delete Pokémon", width=15).pack(pady=5)
Button(button_frame, text="Clear Form", width=15).pack(pady=5)

# Treeview to show data
tree = ttk.Treeview(right_frame, columns=('ID', 'Species', 'Nickname', 'Type', 'Pokéball', 'Location', 'Region', 'Level', 'HP'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Species', text='Species')
tree.heading('Nickname', text='Nickname')
tree.heading('Type', text='Type')
tree.heading('Pokéball', text='Pokéball')
tree.heading('Location', text='Location')
tree.heading('Region', text='Region')
tree.heading('Level', text='Level')
tree.heading('HP', text='HP')

tree.column('ID', width=40)
tree.column('Species', width=100)
tree.column('Nickname', width=100)
tree.column('Type', width=80)
tree.column('Pokéball', width=80)
tree.column('Location', width=80)
tree.column('Region', width=70)
tree.column('Level', width=50)
tree.column('HP', width=50)

# Scrollbar
scrollbar = ttk.Scrollbar(right_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
tree.pack(fill=BOTH, expand=True)

# Start program
root.mainloop()
