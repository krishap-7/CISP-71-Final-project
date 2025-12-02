from tkinter import *
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import sqlite3

# -------------------- DATABASE CLASS --------------------
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

    def execute_query(self, query, params=()):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def fetch_all(self, query, params=()):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        conn.close()
        return data

db = DB("final_project_db.db")

# -------------------- TKINTER UI --------------------
root = Tk()
root.title("Pokémon Database")
root.geometry("900x600")

# Title
title_label = Label(root, text="Pokémon Database Manager", font=("Helvetica", 16))
title_label.pack(pady=10)

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Left side form
left_frame = LabelFrame(main_frame, text="Pokémon Data", padx=10, pady=10)
left_frame.pack(side=LEFT, fill=Y, padx=5)

# Right side table
right_frame = LabelFrame(main_frame, text="All Pokémon", padx=10, pady=10)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)

# -------------------- FORM VARIABLES --------------------
species_var = StringVar()
nickname_var = StringVar()
type_var = StringVar()
pokeball_var = StringVar()
location_var = StringVar()
region_var = StringVar()
level_var = IntVar()
hp_var = IntVar()

selected_id = None  # used for updating/deleting

# -------------------- FORM WIDGETS --------------------
Label(left_frame, text="Species Name:").grid(row=0, column=0, sticky='w')
Entry(left_frame, textvariable=species_var).grid(row=0, column=1)

Label(left_frame, text="Nickname:").grid(row=1, column=0, sticky='w')
Entry(left_frame, textvariable=nickname_var).grid(row=1, column=1)

Label(left_frame, text="Type:").grid(row=2, column=0, sticky='w')
types = ['Normal','Fire','Water','Electric','Grass','Ice','Fighting','Poison','Ground','Flying',
         'Bug','Rock','Ghost','Dragon','Dark','Steel','Fairy']
OptionMenu(left_frame, type_var, *types).grid(row=2, column=1)
type_var.set("Normal")

Label(left_frame, text="Pokéball Type:").grid(row=3, column=0, sticky='w')
pokeballs = ['Poké Ball','Great Ball','Ultra Ball','Master Ball','Quick Ball']
OptionMenu(left_frame, pokeball_var, *pokeballs).grid(row=3, column=1)
pokeball_var.set("Poké Ball")

Label(left_frame, text="Capture Location:").grid(row=4, column=0, sticky='w')
locations = ['Route 1','Forest','Cave','City','Mountain','Beach']
OptionMenu(left_frame, location_var, *locations).grid(row=4, column=1)
location_var.set("Route 1")

Label(left_frame, text="Region:").grid(row=5, column=0, sticky='w')
regions = ['Kanto','Johto','Hoenn','Sinnoh','Unova']
OptionMenu(left_frame, region_var, *regions).grid(row=5, column=1)
region_var.set("Kanto")

Label(left_frame, text="Level:").grid(row=6, column=0, sticky='w')
Entry(left_frame, textvariable=level_var).grid(row=6, column=1)

Label(left_frame, text="HP:").grid(row=7, column=0, sticky='w')
Entry(left_frame, textvariable=hp_var).grid(row=7, column=1)

# -------------------- BUTTON FUNCTIONS --------------------
def load_data():
    for row in tree.get_children():
        tree.delete(row)

    rows = db.fetch_all("SELECT * FROM pokemon")
    for r in rows:
        tree.insert("", END, values=r)

def add_pokemon():
    if species_var.get() == "" or nickname_var.get() == "":
        mb.showerror("Error", "Species and Nickname cannot be blank.")
        return
    
    db.execute_query("""
        INSERT INTO pokemon (species,nickname,type,pokeball,location,region,level,hp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        species_var.get(),
        nickname_var.get(),
        type_var.get(),
        pokeball_var.get(),
        location_var.get(),
        region_var.get(),
        level_var.get(),
        hp_var.get(),
    ))

    clear_form()
    load_data()

def delete_pokemon():
    global selected_id
    if selected_id is None:
        mb.showwarning("Select Pokémon", "Choose a Pokémon from the list first.")
        return
    
    db.execute_query("DELETE FROM pokemon WHERE id=?", (selected_id,))
    clear_form()
    load_data()

def update_pokemon():
    global selected_id
    if selected_id is None:
        mb.showwarning("Select Pokémon", "Choose a Pokémon from the list first.")
        return

    db.execute_query("""
        UPDATE pokemon SET
            species=?, nickname=?, type=?, pokeball=?, location=?, region=?, level=?, hp=?
        WHERE id=?
    """, (
        species_var.get(),
        nickname_var.get(),
        type_var.get(),
        pokeball_var.get(),
        location_var.get(),
        region_var.get(),
        level_var.get(),
        hp_var.get(),
        selected_id,
    ))

    clear_form()
    load_data()

def clear_form():
    global selected_id
    selected_id = None
    species_var.set("")
    nickname_var.set("")
    type_var.set("Normal")
    pokeball_var.set("Poké Ball")
    location_var.set("Route 1")
    region_var.set("Kanto")
    level_var.set(0)
    hp_var.set(0)

def on_row_select(event):
    global selected_id
    item = tree.focus()
    if not item:
        return
    data = tree.item(item)['values']

    selected_id = data[0]
    species_var.set(data[1])
    nickname_var.set(data[2])
    type_var.set(data[3])
    pokeball_var.set(data[4])
    location_var.set(data[5])
    region_var.set(data[6])
    level_var.set(data[7])
    hp_var.set(data[8])

# -------------------- BUTTONS --------------------
button_frame = Frame(left_frame)
button_frame.grid(row=8, column=0, columnspan=2, pady=20)

Button(button_frame, text="Add Pokémon", width=15, command=add_pokemon).pack(pady=5)
Button(button_frame, text="Update Pokémon", width=15, command=update_pokemon).pack(pady=5)
Button(button_frame, text="Delete Pokémon", width=15, command=delete_pokemon).pack(pady=5)
Button(button_frame, text="Clear Form", width=15, command=clear_form).pack(pady=5)

# -------------------- TREEVIEW --------------------
tree = ttk.Treeview(right_frame,
    columns=('ID','Species','Nickname','Type','Pokéball','Location','Region','Level','HP'),
    show='headings'
)

for col in ('ID','Species','Nickname','Type','Pokéball','Location','Region','Level','HP'):
    tree.heading(col, text=col)

tree.pack(fill=BOTH, expand=True)
tree.bind("<<TreeviewSelect>>", on_row_select)

load_data()

root.mainloop()


