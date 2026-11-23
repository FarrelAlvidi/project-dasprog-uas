import json
from rich.console import Console
from ui import BOLD, RESET, GRAY
from ui import cetak_menu, gagal
from inventory import update_karakter

console = Console()
file_path = "data/characters.json"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        characters = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    characters = []

roles = {
    "Warrior": {"hp": 120, "attack": 10},
    "Mage": {"hp": 80, "attack": 14},
    "Rogue": {"hp": 100, "attack": 12},
}


def buat_karakter():
    nama = input("Masukkan Nama Karakter: ").strip().title()

    if nama == "":
        print("Nama karakter tidak boleh kosong!")
        return

    role = input("Masukkan Role Karakter (Warrior, Mage, Rogue): ").strip().title()

    if role not in roles:
        print("Role karakter tidak valid!")
        return

    s = roles[role]

    data_karakter = {
        "id": len(characters) + 1,  
        "nama": nama,
        "role": role,
        "level": 1,
        "exp": 0,
        "gold": 100,
        "highest_floor": 1,
        "inventory": {"potion_kecil":1},
        "equipped": "",
        "max_hp": s['hp'],
        "hp": s["hp"],
        "attack": s["attack"]
    }

    characters.append(data_karakter)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(characters, f, indent=4)

    print("Karakter berhasil dibuat!")


def tampilkarakter():
    # console.print("Daftar Karakter:", style="bold blue")
    console.print(f"[bold blue]MENU KARAKTER[/bold blue] [bright_black]{'─' * 49}[/bright_black]")
    

    for k in characters:
        console.print(f"{k['id']}. {k['nama']} - {k['role']} - Level: {k['level']} - Highest Floor: {k['highest_floor']}")
        


# buat_karakter()
# tampilkarakter()