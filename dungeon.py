import random
import time
from rich.progress import track

class Monster:
    def __init__(self, name, hp, damage, type_, floor):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.type = type_
        self.floor = floor
        
    def munculin(self):
        return f"{self.name}, {self.hp}, {self.damage}, {self.type}, {self.floor}"
        


# def floor_1(monster_target):
#     print(f"Prepare to fight {monster_target.name}")
#     battle(monster_target)

def battle(enemy):
    p = 100
    turn = random.randint(1,2)
    for i in track(range(5), description="Loading..."):
        time.sleep(0.8)  # Simulate work being done
    while p>0 and enemy.hp>0:

        if turn == 1:
            print("Your Turn")
            input("Attack : ")
            enemy.hp -= 5
            turn = 2
            print(f"You damage 5")
            print(f"Enemy HP : {enemy.type}")
            time.sleep(1)
            
        if turn == 2:
            print("Enemy Turn")
            time.sleep(2)
            p -= enemy.damage
            turn = 1
            print(f"Enemy damage {enemy.damage}")
            print(f"Your HP {p}")
            time.sleep(1)
    if p>0:
        print("You win!")
    else:
        print("You lose")
        

DemonKnight = Monster(
    name="Demon Knight",
    hp= 200,
    damage=20,
    type_="Assassin",
    floor=5
)
# DemonKnight.munculin()
battle(DemonKnight)