from battle import *
from storage import FILE_MONSTER, muat_data
from ui import (cetak_menu, cetak_header, cetak_status, minta_angka)

MAKS_FLOOR = 5


def validasi_floor(aktif, floor):
    if floor > aktif["highest_floor"]:
        print(f"{RED}Kalahkan lantai sebelumnya terlebih dahulu!")
        jeda()
        return False

    return True


def menu_dungeon(aktif):
    list_monster = muat_data(FILE_MONSTER)
    maks_floor = min(aktif["highest_floor"] + 1, MAKS_FLOOR)

    cetak_header("Dungeon")
    cetak_status(aktif)
    # cetak_menu([("1", "Skeleton"),
    #                     ("2", "Goblin"),
    #                     ("3", "Shadow"),
    #                     ("0", "Kembali ke menu utama")])
    daftar_pilihan = [
        (str(enemy['id']), enemy['name'])
        for enemy in list_monster
    ]
    daftar_pilihan.append(("0", "Kembali ke menu utama"))

    cetak_menu(daftar_pilihan)

    try:
        pilihan = int(input("> "))
    except ValueError:
        print("Input harus berupa angka!")
        return
    
    if pilihan == 0:
        return
    
    if not validasi_floor(aktif, pilihan):
        return
    
    for data in list_monster:
        if pilihan <= maks_floor:
            if pilihan == data['id']:
                battle(aktif, data, pilihan)
        else:
            print("Pilih lantai yang tersedia/yang sudah dibuka")
        
            
