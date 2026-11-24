import os

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
WHITE = "\033[97m"
GRAY = "\033[90m"

WARNA_ITEM = {
    "potion_kecil": GREEN,
    "potion_besar": CYAN,
    "pedang_kayu": YELLOW,
    "pedang_besi": WHITE,
    "pedang_baja": BLUE,
    "pedang_naga": RED,
}
WARNA_TIPE = {"potion": GREEN, "weapon": MAGENTA}
LABEL_TIPE = {"potion": "Potion", "weapon": "Senjata"}

if os.name == "nt":
    os.system("")


def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")


def jeda():
    input(f"\n {GRAY}Tekan Enter untuk melanjutkan...{RESET}")


def tanya(pesan):
    print(f" {CYAN}{BOLD}{pesan}{RESET}", end="")
    return input().strip()


def minta_angka(pesan, kecil, besar):
    while True:
        try:
            angka = int(tanya(pesan))
            if kecil <= angka <= besar:
                return angka
            gagal(f"Angka harus antara {kecil} sampai {besar}.")
        except ValueError:
            gagal("Masukkan angka yang valid!")


def sukses(teks):
    print(f" {GREEN}{BOLD}✔ {teks}{RESET}")


def gagal(teks):
    print(f" {RED}{BOLD}✘ {teks}{RESET}")
    
def serang(teks):
    print(f" {GRAY}{BOLD}» {teks}{RESET}")


def info(teks):
    print(f" {YELLOW}• {teks}{RESET}")

def cetak_header(teks, warna=CYAN):
    lebar = 56
    judul = " ".join(teks.upper())  
    if len(judul) > lebar - 6:  
        judul = teks.upper()
    judul = f"◆ {judul} ◆"
    print(f"\n{warna}{BOLD}╔" + "═" * lebar + f"╗{RESET}")
    print(f"{warna}{BOLD}║{RESET}{BOLD}{judul.center(lebar)}{RESET}{warna}{BOLD}║{RESET}")
    print(f"{warna}{BOLD}╚" + "═" * lebar + f"╝{RESET}")


def cetak_menu(daftar_pilihan, warna=CYAN):
    print(f"\n {warna}{BOLD}MENU{RESET} {GRAY}" + "─" * 49 + RESET)
    for kode, teks in daftar_pilihan:
        print(f"  {warna}{BOLD}[{kode}]{RESET} {teks}")
    print()


def hp_bar(sekarang, maks, panjang=10):
    if maks <= 0:
        maks = 1
    rasio = max(0.0, min(1.0, sekarang / maks))
    isi = int(rasio * panjang)
    bar = "█" * isi + "░" * (panjang - isi)
    if rasio > 0.5:
        warna = GREEN
    elif rasio > 0.25:
        warna = YELLOW
    else:
        warna = RED
    return f"{warna}[{bar}]{RESET} {sekarang}/{maks}"

def exp_bar(exp, butuh, panjang=10):
    isi = int(min(1.0, exp / butuh) * panjang)
    return f"{BLUE}[{'█' * isi}{'░' * (panjang - isi)}]{RESET} {exp}/{butuh}"


def cetak_status(karakter, bonus_atk=0, warna=CYAN):
    atk = karakter.get("attack", 0)
    # nama_senjata = karakter.get('equipped', '')
    butuh = karakter.get('level') * 50
    sisi = f"{warna}│{RESET}"
    print(f"\n{warna}┌─ {BOLD}STATUS{RESET}{warna} " + "─" * 46 + RESET)
    print(f"{sisi}  {BOLD}{karakter.get('nama', 'Pemain')}{RESET}  {GRAY}Lv {karakter.get('level', 1)}{RESET}")
    print(f"{sisi} HP       {hp_bar(karakter.get('hp'), karakter.get('max_hp', 0))}")
    print(f"{sisi} EXP      {exp_bar(karakter.get('exp', 0), butuh)}")
    print(f"{sisi} Gold     {YELLOW}{BOLD}◉ {karakter.get('gold', 0)} G{RESET}")    
    print(f"{sisi} Senjata  {MAGENTA}{BOLD}{karakter.get('equipped', 'None')}{RESET}")
    print(f"{sisi} ATK      {RED}{BOLD}{atk + bonus_atk}{RESET} {GRAY}({atk} dasar + {bonus_atk} senjata){RESET}")
    print(f"{warna}└" + "─" * 55 + RESET)

def teks_efek(item):
    if item["tipe"] == "potion":
        return f"Pulihkan {item['efek']} HP"
    return f"+{item['efek']} ATK"


def sel(teks, lebar, kode=RESET, rata="kiri"):
    """Satu sel tabel: teks dipadatkan sebesar lebar kolom, lalu diberi warna."""
    if rata == "kanan":
        teks = str(teks).rjust(lebar)
    else:
        teks = str(teks).ljust(lebar)
    return f" {kode}{teks}{RESET} "


def buat_garis(lebar_kolom, kiri, tengah, kanan):
    garis = kiri
    for i in range(len(lebar_kolom)):
        garis += "─" * (lebar_kolom[i] + 2)
        if i < len(lebar_kolom) - 1:
            garis += tengah
    return garis + kanan


def cetak_tabel_item(judul, daftar_item, harga_jual=False, inventory=None,
                     judul_jumlah="Jumlah", id_dipakai=""):
    lebar = [2, 16, 8, 14, 10]  
    if inventory is not None:
        lebar.append(6)  # kolom jumlah
    judul_harga = "Harga Jual" if harga_jual else "Harga"
    sisi = f"{CYAN}│{RESET}"

    print(f"\n {YELLOW}{BOLD}◆ {judul}{RESET}")
    print(f"{CYAN}{buat_garis(lebar, '┌', '┬', '┐')}{RESET}")

    baris = sisi + sel("No", 2, BOLD, "kanan")
    baris += sisi + sel("Nama Item", 16, BOLD)
    baris += sisi + sel("Tipe", 8, BOLD)
    baris += sisi + sel("Efek", 14, BOLD)
    baris += sisi + sel(judul_harga, 10, BOLD, "kanan")
    if inventory is not None:
        baris += sisi + sel(judul_jumlah, 6, BOLD, "kanan")
    print(baris + sisi)
    print(f"{CYAN}{buat_garis(lebar, '├', '┼', '┤')}{RESET}")

    for no, item in enumerate(daftar_item, 1):
        warna = WARNA_ITEM.get(item["id"], WARNA_TIPE.get(item["tipe"], RESET))
        nama = "  " + item["nama"]
        if item["id"] == id_dipakai:
            nama = "★ " + item["nama"]
        harga = item["harga"] // 2 if harga_jual else item["harga"]

        baris = sisi + sel(no, 2, GRAY, "kanan")
        baris += sisi + sel(nama, 16, warna + BOLD)
        baris += sisi + sel(LABEL_TIPE.get(item["tipe"], item["tipe"]), 8, WARNA_TIPE.get(item["tipe"], RESET))
        baris += sisi + sel(teks_efek(item), 14, WHITE)
        baris += sisi + sel(f"{harga} G", 10, YELLOW, "kanan")
        if inventory is not None:
            jumlah = inventory.get(item["id"], 0)
            warna_jumlah = CYAN if jumlah > 0 else GRAY
            baris += sisi + sel(jumlah, 6, warna_jumlah, "kanan")
        print(baris + sisi)

    print(f"{CYAN}{buat_garis(lebar, '└', '┴', '┘')}{RESET}")

# print(sel("Halo", 20))
print(buat_garis([2, 3, 5, 2], '└', '┴', '┘'))