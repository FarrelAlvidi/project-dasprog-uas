import json
import os
from ui import (cetak_header, cetak_status, cetak_tabel_item, cetak_menu, bersihkan_layar,
                jeda, tanya, sukses, gagal, info, minta_angka)
from storage import muat_data, FILE_ITEM


# ITEM_BAWAAN = [
#     {"id": "potion_kecil", "nama": "Potion Kecil", "tipe": "potion", "harga": 30, "efek": 30},
#     {"id": "potion_besar", "nama": "Potion Besar", "tipe": "potion", "harga": 70, "efek": 80},
#     {"id": "pedang_kayu", "nama": "Pedang Kayu", "tipe": "weapon", "harga": 50, "efek": 2},
#     {"id": "pedang_besi", "nama": "Pedang Besi", "tipe": "weapon", "harga": 150, "efek": 5},
#     {"id": "pedang_baja", "nama": "Pedang Baja", "tipe": "weapon", "harga": 400, "efek": 9},
#     {"id": "pedang_naga", "nama": "Pedang Naga", "tipe": "weapon", "harga": 1000, "efek": 15},
# ]

def update_karakter(karakter):
    with open("data/characters.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, char in enumerate(data):
        if char["nama"] == karakter["nama"]:
            data[i] = karakter
            break

    with open("data/characters.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def muat_items():
    hasil = {}
    for item in muat_data(FILE_ITEM):
        hasil[item["id"]] = item
    return hasil


def senjata_aktif(karakter, item_dict):
    return item_dict.get(karakter.get("equipped", ""), {})


def daftar_tas(karakter, data_items):
    tas = []

    for item_id, jumlah in karakter["inventory"].items():
        if jumlah > 0 and item_id in data_items:
            item = data_items[item_id].copy()
            tas.append(item)

    return tas


def tambah_item(karakter, id_item, jumlah=1):
    inv = karakter.setdefault("inventory", {})

    inv[id_item] = inv.get(id_item, 0) + jumlah

    update_karakter(karakter)

    print(f"Berhasil menambahkan {id_item} sebanyak {jumlah}!")
    


def kurangi_item(karakter, id_item, jumlah=1):
    inv = karakter.setdefault("inventory", {})
    inv[id_item] -= jumlah
    if inv[id_item] <= 0: # Cek kalau item nya = 0, del item tersebut
        del inv[id_item] 
        if karakter.get("equipped", "") == id_item:
            karakter["attack"] -= muat_items()[id_item]["efek"]
            karakter["equipped"] = ""

def pakai_potion(karakter, item):
    hp = karakter.get("hp", 100)
    max_hp = karakter.get("max_hp", 100)
    if hp >= max_hp:
        gagal("HP sudah penuh, potion tidak dipakai.")
        return False
    karakter["hp"] = min(max_hp, hp + item["efek"])
    kurangi_item(karakter, item["id"])
    update_karakter(karakter)
    sukses(f"Memakai {item['nama']}! HP pulih {hp} ➔ {karakter['hp']}")
    return True


def pasang_senjata(karakter, item):
    if karakter.get("equipped", "") == item["id"]:
        gagal(f"{item['nama']} sudah kamu pakai.")
        return False
    if karakter.get("equipped", ""):
        lepas_senjata(karakter) # Jika udah ada senjata yang dipakai, harus dilepas dlu
    karakter["equipped"] = item["id"]
    karakter["attack"] += item['efek']
    update_karakter(karakter)
    
    sukses(f"Berhasil memasang {item['nama']} (Bonus ATK +{item['efek']})!")
    return True


def lepas_senjata(karakter):
    id_senjata = karakter.get("equipped", "")
    if karakter.get("equipped", "") == "":
        gagal("Kamu belum memakai senjata.")
        return False
    efek = muat_items()[id_senjata]["efek"]
    karakter["equipped"] = ""
    karakter["attack"] -= efek
    update_karakter(karakter)
    sukses("Senjata berhasil dilepas.")
    return True


def bonus_senjata(karakter):
    """Bonus ATK dari senjata yang dipakai. Hasilnya 0 kalau tidak pakai senjata."""
    return senjata_aktif(karakter, muat_items()).get("efek", 0)


def pakai_potion_battle(karakter):
    """
    Aksi "Item" di battle. Hasil True kalau potion berhasil dipakai (giliran terpakai),
    False kalau dibatalkan atau gagal.
    """
    potion = []
    for item in daftar_tas(karakter, muat_items()):
        if item["tipe"] == "potion":
            potion.append(item)
    if len(potion) == 0:
        gagal("Kamu tidak punya potion!")
        return False
    cetak_tabel_item("POTION DI TAS", potion, inventory=karakter["inventory"])
    nomor = minta_angka("Pilih nomor potion (0 = batal) ➤ ", 0, len(potion))
    if nomor == 0:
        return False
    return pakai_potion(karakter, potion[nomor - 1])


def pakai_dari_tas(karakter, tas):
    nomor = minta_angka("Pilih nomor item yang ingin dipakai (0 = batal) ➤ ", 0, len(tas))
    if nomor == 0:
        return False
    item = tas[nomor - 1]
    print()
    if item["tipe"] == "potion":
        pakai_potion(karakter, item)
    else:
        pasang_senjata(karakter, item)
    return True

        

def menu_inventory(karakter):
    isi_inventory = muat_items()
    while True:
        bersihkan_layar()
        cetak_header("Inventory")
        senjata = senjata_aktif(karakter, isi_inventory)
        cetak_status(karakter)

        tas = daftar_tas(karakter, isi_inventory)
        if len(tas) == 0:
            print()
            info("Tas kamu masih kosong. Belanja dulu di Shop ya!")
        else:
            cetak_tabel_item("ISI TAS", tas, inventory=karakter["inventory"],
                 id_dipakai=karakter.get("equipped", ""))
            print(" ★ = senjata yang sedang dipakai")

        cetak_menu([("1", "Pakai potion / pasang senjata"),
                    ("2", "Lepas senjata"),
                    ("0", "Kembali ke menu utama")])
        pilihan = tanya("Pilih opsi ➤ ")

        if pilihan == "1":
            if len(tas) == 0:
                gagal("Tas kosong, belum ada item yang bisa dipakai.")
                jeda()
            elif pakai_dari_tas(karakter, tas):
                jeda()
        elif pilihan == "2":
            lepas_senjata(karakter)
            jeda()
        elif pilihan == "0":
            break
        else:
            gagal("Pilihan tidak valid.")
            jeda()
