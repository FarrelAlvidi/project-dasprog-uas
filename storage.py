import json
import os

FILE_KARAKTER = "data/characters.json"
FILE_ITEM = "data/items.json"
FILE_MONSTER = "data/monsters.json"

DEFAULT_KARAKTER = {
    "inventory": {},
    "equipped_weapon": "",
    "highest_floor": 0,
}


def muat_data(nama_file):
    if not os.path.exists(nama_file):
        return []
    with open(nama_file, "r", encoding="utf-8") as f:
        return json.load(f)


def simpan_data(nama_file, data):
    os.makedirs(os.path.dirname(nama_file), exist_ok=True)
    with open(nama_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def muat_karakter():
    daftar = muat_data(FILE_KARAKTER)
    for k in daftar:
        for key, nilai in DEFAULT_KARAKTER.items():
            k.setdefault(key, nilai)
    return daftar