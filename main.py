from characters import Characters
import time
# from rich import print
from rich.console import Console
# from rich.layout import Layout

console = Console()
data = Characters.load_character()

print("-" * 15, "Welcome To Dungeon Game", "-" * 15)
# while True:
#     print("1. Choose Character")
#     print("2. Create Character")
#     print("3. Leave")
#     choose = int(input("> "))
#     if choose  == 1:
#         Characters.show_character()
#         choose_character = int(input("> ")) - 1

#     elif choose == 2:
#         Characters.create_character(data)
#     elif choose == 3:
#         break

while True:
    print("Silahkan Pilih ")
    print("1. Characters")
    print("2. Dungeon")
    print("3. Shop")
    print("4. Inventory")
    print("5. Leaderboard")
    print("6. Leave")
    choose = int(input("> "))
    if choose == 2:
        print("Choose Floor")
        choose_floor =  int(input("> "))
        
    if choose == 6:
        console.print("See you next time!", style="green")
        break
        
        