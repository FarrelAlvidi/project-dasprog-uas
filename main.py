from characters import characters, tampilkarakter, buat_karakter
# from shop import shop
from dungeon import *
from battle import *
from rich.console import Console
from inventory import menu_inventory
from shop import *
from ui import (cetak_menu, cetak_header, gagal)

console = Console()


def input_angka(pesan):
    while True:
        teks = input(pesan)
        if teks.isdigit():
            return int(teks)
        gagal("Masukkan angka!")


def cari_karakter(id_karakter):
    for character in characters:
        if character["id"] == id_karakter:
            return character
    return None


def pilih_karakter():
    while True:
        tampilkarakter()
        aktif = cari_karakter(input_angka("Pilih karakter (id): "))
        if aktif is not None:
            return aktif
        print("Karakter tidak ditemukan!")


def menu_utama(aktif):
    while True:
        bersihkan_layar()
        cetak_header(f"Selamat Datang {aktif["nama"]}")
        cetak_status(aktif)
        cetak_menu([
            ("1", "Dungeon"),
            ("2", "Inventory"),
            ("3", "Shop"),
            ("4", "Exit")
        ])
        pilihan = input_angka("> ")

        if pilihan == 1:
            # print("Choose Floor")      # nanti: menu_dungeon(aktif)
            menu_dungeon(aktif)
            # battle(aktif)
        elif pilihan == 2:
              # nanti: menu_inventory(aktif)
            menu_inventory(aktif)
        elif pilihan == 3:  
            menu_shop(aktif)
            # print("Shop")  # nanti: shop(aktif)
        elif pilihan == 4:
            console.print(f"Sampai bertemu lagi {aktif['nama']}!", style="green bold")
            jeda()
            main()
            break
        else:
            gagal("Tolong pilih aksi yang tersedia!")
            jeda()
            
# def menu_inventory(aktif):
#     print(aktif["inventory"])  # nanti: menu_inventory(aktif)
#     pilihan = input_angka("Pilih item yang ingin dipakai \n> ")
    
def main():
    # print("-" * 15, "Welcome To Dungeon Game", "-" * 15)
    bersihkan_layar()
    cetak_header("Welcome To Dungeon Game", warna="\033[91m")
    cetak_menu([
        ("1", "Lihat Karakter"),
        ("2", "Buat Karakter Baru"),
        ("0", "Keluar")
    ], warna="\033[91m")
    while True:
        pilihan = input_angka("➤ ")

        if pilihan == 1:
            if characters:
                menu_utama(pilih_karakter())
            else:
                gagal("Belum ada karakter, Silahkan buat terlebih dahulu!")
        elif pilihan == 2:
            buat_karakter()
        elif pilihan == 0:
            break
        else:
            print("Tolong pilih aksi yang tersedia!")


if __name__ == "__main__":
    main()