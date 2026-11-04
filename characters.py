
import json
from rich.console import Console
from rich.table import Table

rich = Console()
table = Table(title="View Characters \n ",  show_edge=False )



class Characters:

    @staticmethod
    def load_character():
        with open("data/characters.json", "r") as f:
            character = json.load(f)
        return character
    
    @staticmethod
    def simpan_data(data): # Jika ada data yang ingin disimpan
        with open("data/characters.json", "w") as f:
            json.dump(data, f, indent=4)
        

    @staticmethod
    def create_character(data): # Buat data karakter
            name = input("Input Name : ")
            if name == "":
                rich.print("Name cannot be empty", style="bold red")
                return
            create_chara = {
                "name": name,
                "role": "Fighter",
                "level": 1,
                "gold": 100,
                "hp": 100,
                "inventory": []
            }
            data.append(create_chara)
            Characters.simpan_data(data)
            print("Character has been created!")

    @staticmethod
    def show_character():
        characters = Characters.load_character()
        table.add_column("Name", justify="right", style="cyan", no_wrap=True)
        table.add_column("Role", style="magenta")
        table.add_column("Level", justify="right", style="green")
        for i in characters:
            table.add_row(i['name'], i['role'], str(i['level']))
        rich.print(table)
            # rich.print(
            #     f"[red bold]>[/red bold] "
            #     f"[magenta]{i['name']} - {i['role']} - Level "
            #     f"{i['level']}[/magenta]",
            #     style="blue"
            # )
            
    # @staticmethod
    # def choose_character():
        
