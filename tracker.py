import sqlite3
from dataclasses import dataclass

#foods database 
def insert_food(conn, name, protein, carb, fat, unit):
    with conn:
        conn.execute("INSERT INTO Foods(name, protein, carb, fat, unit) VALUES (:name, :protein, :carb, :fat, :unit)",
                    {"name": name, "protein": protein, "carb": carb, "fat": fat, "unit": unit})

def get_conn(relation, path=":memory:"):
    conn = sqlite3.connect(path)
    conn.executescript(relation)
    return conn

FOODS_SCHEMA = """  
CREATE TABLE IF NOT EXISTS Foods(
name    TEXT NOT NULL UNIQUE,
protein    REAL NOT NULL,
carb    REAL NOT NULL,
fat    REAL NOT NULL,
unit    REAL,
PRIMARY KEY    (name));
"""

FOODS = [
    ("olive oil", 0.0, 0.0, 100.0, None),
    ("rice uncooked", 7.1, 78.0, 0.7, None),
    ("rice cooked", 2.4, 26.0, 0.2, None),
    ("chicken breast uncooked", 22.5, 0.0, 2.6, None),
    ("chicken breast cooked", 31.0, 0.0, 3.6, None),
    ("potatoes boiled", 2.0, 20.0, 0.1, None),
    ("potatoes baked", 2.5, 25.0, 0.15, None),
    ("potatoes raw", 2.0, 17.0, 0.1, None),
    ("pasta uncooked", 13.0, 75.0, 1.5, None),
    ("pasta cooked", 5.8, 31.0, 0.9, None),
    ("tomatoes", 0.9, 3.9, 0.2, 120.0),
    ("butter", 0.85, 0.1, 81.0, None),
    ("butter clarified", 0.0, 0.0, 100.0, None),
    ("quark protein", 12.0, 4.0, 0.2, 226.0),
    ("yoghurt", 6.0, 4.0, 7.0, None),
    ("skyr", 11.0, 4.0, 0.2, None),
    ("egg white", 11.0, 0.7, 0.2, 33.0),
    ("egg yolk", 16.0, 3.6, 27.0, 17.0),
    ("egg", 12.6, 1.1, 9.5, 50.0),
    ("aubergine roasted", 1.0, 8.0, 0.2, None),
    ("pepper roasted", 1.0, 6.0, 0.3, None),
    ("bread white", 8.5, 49.0, 3.2, 30.0),
    ("bread whole", 10.0, 43.0, 3.5, 30.0),
    ("bread rye", 8.5, 48.0, 3.3, 30.0),
    ("bread sourdough", 8.0, 50.0, 1.5, 40.0),
    ("cheese feta", 14.0, 4.0, 21.0, None),
    ("olives", 0.8, 6.0, 15.0, 4.0),
    ("honey", 0.3, 82.0, 0.0, None),
    ("banana", 1.1, 23.0, 0.3, 118.0),
    ("milk whole", 3.3, 4.7, 3.6, None),
    ("milk reduced", 3.4, 4.8, 1.8, None),
    ("milk skimmed", 3.4, 5.0, 0.1, None),
    ("cucumbers", 0.7, 3.6, 0.1, 200.0),
    ("onions", 1.1, 9.3, 0.1, 110.0),
    ("kebab adana", 17.0, 2.0, 22.0, 150.0),
    ("lahmacun", 11.0, 33.0, 7.0, 180.0),
    ("kofte", 18.0, 4.0, 15.0, 40.0),
    ("mayo light", 0.5, 8.0, 25.0, None),
    ("cheese tulum", 22.0, 1.5, 28.0, None),
    ("baklava", 6.0, 48.0, 25.0, 60.0),
    ("popcorn", 12.0, 74.0, 4.5, None),
    ("corn cob", 3.3, 21.0, 1.3, 90.0),
    ("chicken thigh cooked", 26.0, 0.0, 10.0, None),
    ("beef lean cooked", 30.0, 0.0, 10.0, None),
    ("beef mince raw", 20.0, 0.0, 15.0, None),
    ("lentil soup", 2.5, 9.0, 2.0, 250.0),
    ("lentils cooked", 9.0, 20.0, 0.4, None),
    ("chickpeas cooked", 8.9, 27.0, 2.6, None),
    ("bulgur cooked", 3.1, 19.0, 0.2, None),
    ("lavash", 8.0, 53.0, 1.5, 60.0),
    ("simit", 9.0, 55.0, 4.5, 100.0),
    ("balsamic vinegar", 0.5, 17.0, 0.0, None),
    ("ketchup", 1.2, 26.0, 0.2, None),
    ("tuna canned", 25.0, 0.0, 1.0, 80.0),
    ("apple", 0.3, 14.0, 0.2, 180.0),
    ("orange", 0.9, 12.0, 0.1, 130.0),
    ("whey", 75.0, 6.0, 4.5, 32.0),
    ("doner chicken", 25.0, 0.0, 12.0, None),
    ("doner beef", 22.0, 0.0, 20.0, None),
]

conn = get_conn(FOODS_SCHEMA)

for f in FOODS:
    insert_food(conn, *f)

#entries database

ENTRIES_SCHEMA = """ 
CREATE TABLE IF NOT EXISTS entries(
date    TEXT NOT NULL UNIQUE,
kcal    INTEGER NOT NULL,
protein INTEGER NOT NULL,
carb    INTEGER NOT NULL,
fat     INTEGER NOT NULL,
PRIMARY KEY    (date));
"""


#calculation funcs
def meal_calc(conn, meal_list):
    rows = []
    total = [0.0, 0.0, 0.0, 0.0]

    for item in meal_list:
        name, measure = item[0], item[1]
        unit = item[2] if len(item) > 2 else "g"

        entity = conn.execute(
            "SELECT protein, carb, fat, unit FROM Foods WHERE name = :name",
            {"name": name}
        ).fetchone()

        if entity is None:
            raise ValueError(f"food not found: {name}")

        if unit == "unit":
            if entity[3] is None:
                raise ValueError(f"{name} adetle olculemez")
            grams = measure * entity[3]
        else:
            grams = measure

        k = grams / 100
        protein = entity[0]*k
        carb = entity[1]*k
        fat = entity[2]*k
        kcal = protein*4 + carb*4 + fat*9

        rows.append((name, kcal, protein, carb, fat))
        for i, v in enumerate((kcal, protein, carb, fat)):
            total[i] += v

    return rows, tuple(total)