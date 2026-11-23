from inventory import muat_items, senjata_aktif, daftar_tas, tambah_item, kurangi_item
from ui import (cetak_header, cetak_status, cetak_tabel_item, cetak_menu, bersihkan_layar,
                jeda, tanya, sukses, gagal, info, minta_angka, YELLOW, BOLD, RESET)
from inventory import (update_karakter, lepas_senjata)


def beli_item(k, item, jumlah=1):
    total = item["harga"] * jumlah
    if item["tipe"] == "weapon" and item["id"] in k.get("inventory", {}):
        gagal("Kamu sudah punya senjata ini.")
        return False
    if k.get("gold", 0) < total:
        gagal(
            f"Gold tidak cukup! Butuh {total} G, kamu punya {k.get('gold', 0)} G.")
        return False
    k["gold"] -= total
    tambah_item(k, item["id"], jumlah)
    sukses(f"Berhasil membeli {jumlah}x {item['nama']} seharga {total} Gold!")
    return True


def jual_item(k, item_id, item_dict, jumlah=1):
    inv = k.setdefault("inventory", {})
    if inv.get(item_id, 0) < jumlah:
        gagal("Kamu tidak punya item itu dalam jumlah tersebut.")
        return False
    data = item_dict.get(item_id, {})
    pendapatan = (data.get("harga", 10) // 2) * \
        jumlah  # jual dengan setengah harga
    sedang_dipakai = k.get("equipped", "") == item_id
    kurangi_item(k, item_id, jumlah)
    update_karakter(k)
    k["gold"] = k.get("gold", 0) + pendapatan
    sukses(
        f"Berhasil menjual {jumlah}x {data.get('nama', item_id)} seharga {pendapatan} Gold.")
    if sedang_dipakai and k.get("equipped", "") == "":
        info("Senjata yang kamu pakai ikut terlepas.")
    return True


def beli_dari_toko(karakter, items_data):
    nomor = minta_angka(
        "Pilih nomor item yang ingin dibeli (0 = batal) ➤ ", 0, len(items_data))
    if nomor == 0:
        return
    item = items_data[nomor - 1]
    jumlah = 1
    if item["tipe"] == "potion":
        jumlah = minta_angka("Mau beli berapa? (1-99) ➤ ", 1, 99)
    print()
    beli_item(karakter, item, jumlah)
    jeda()


def jual_dari_inventory(karakter, item_dict):
    tas = daftar_tas(karakter, item_dict)
    if len(tas) == 0:
        print()
        info("Tas kosong, tidak ada barang yang bisa dijual.")
        jeda()
        return
    cetak_tabel_item("ISI TAS (harga jual = 50% dari harga asli)", tas, harga_jual=True,
                     inventory=karakter["inventory"], id_dipakai=karakter.get("equipped", ""))
    print()
    nomor = minta_angka(
        "Pilih nomor item yang ingin dijual (0 = batal) ➤ ", 0, len(tas))
    if nomor == 0:
        return
    item = tas[nomor - 1]
    jumlah = 1
    punya = karakter["inventory"][item["id"]]
    if punya > 1:
        jumlah = minta_angka(f"Mau jual berapa? (1-{punya}) ➤ ", 1, punya)
    print()
    jual_item(karakter, item["id"], item_dict, jumlah)
    jeda()


def menu_shop(karakter):
    item_dict = muat_items()
    items_data = []
    for id_item, item in item_dict.items():
        items_data.append(item)

    while True:
        bersihkan_layar()
        cetak_header("Toko Item", YELLOW)
        senjata = senjata_aktif(karakter, item_dict)
        cetak_status(karakter,
                     senjata.get("efek", 0), YELLOW)
    
        cetak_tabel_item("DAFTAR BARANG DI TOKO", items_data, inventory=karakter.get("inventory", {}),
                         judul_jumlah="Punya", id_dipakai=karakter.get("equipped", ""))
        print(" ★ = senjata yang sedang dipakai")

        cetak_menu([("1", "Beli item"),
                    ("2", "Jual item dari inventory"),
                    ("0", "Kembali ke menu utama")], YELLOW)
        pilihan = tanya("Pilih opsi ➤ ")

        if pilihan == "1":
            beli_dari_toko(karakter, items_data)
        elif pilihan == "2":
            jual_dari_inventory(karakter, item_dict)
        elif pilihan == "0":
            break
        else:
            gagal("Pilihan tidak valid.")
            jeda()
