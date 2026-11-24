import random
import time
import os
from inventory import update_karakter, menu_inventory
from ui import jeda, cetak_header, cetak_menu, WHITE, MAGENTA, BOLD, RED, sukses, info, serang, gagal


def levelup_karakter(aktif):
    while aktif['exp'] >= aktif['level'] * 50:
        aktif['exp'] = aktif['exp'] - aktif['level'] * 50
        aktif['level'] += 1
        aktif['attack'] += 2
        aktif["max_hp"] += 5
        sukses(f"LEVEL UP! {aktif['nama']} sekarang level {aktif['level']}")

def battle(aktif, monster, floor):
    # print(f"\n=== Battle ===\n{aktif['nama']} vs {monster['name']}")
    cetak_header(f"BATTLE {aktif['nama']} vs {monster['name']}")
    turn = random.randint(0, 1)      # 1 = pemain duluan, 0 = monster duluan

    while aktif["hp"] > 0 and monster["hp"] > 0:
        if turn == 1:
            info("Anda menyerang, Silahkan pilih aksi!")
            cetak_menu([
                ("1", "Serang"),
                ("2", "Lari"),
            ], warna=WHITE)
            action = input("> ")

            if action == "1":
                monster["hp"] -= aktif["attack"]
                serang(f"{aktif['nama']} menyerang {monster['name']}! "
                      f"Sisa HP monster: {max(0, monster['hp'])}")
            elif action == "2":
                if random.random() < 0.5:
                    print("Berhasil lari!")
                    return "kabur"
                print("Gagal lari!")
            else:
                print("Pilihan tidak valid.")
                continue             
        else:
            info("Lawan telah menyerangmu!")
            aktif["hp"] -= monster["attack"]
            serang(f"{monster['name']} menyerangmu! "
                  f"Sisa HP kamu: {max(0, aktif['hp'])}")

        time.sleep(1)
        turn = 1 - turn

    if monster["hp"] <= 0:
        print(f"{MAGENTA}{BOLD}Lantai {floor} telah dikalahkan, anda mendapatkan {monster['gold']} gold dan {monster['exp']}")
        aktif['gold'] += monster['gold']
        aktif['exp'] += monster['exp']
        if floor == aktif["highest_floor"]:
            aktif["highest_floor"] += 1
        levelup_karakter(aktif)
        jeda()
        update_karakter(aktif)
        return "menang"
    elif aktif['hp'] <= 0:
        duit_ilang = aktif['gold'] // 5
        gagal(f"Kamu telah dikalahkan! Gold berkurang {duit_ilang}")
        aktif['gold'] -= duit_ilang
        aktif['hp'] = aktif['max_hp']
        jeda()
        update_karakter(aktif)
        return "kalah"