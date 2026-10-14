import random
world=[]
SIZE=10
for row in range(SIZE):
    world.append(["."] * SIZE)

creature_x=random.randint(0, SIZE-1)
creature_y=random.randint(0, SIZE-1)

MAX_ENERGY=10
creature_energy=MAX_ENERGY

turns_survived=0
walls_hit=0
food_eaten=0

FOOD_COUNT = 5
foods = []

while len(foods) < FOOD_COUNT:
    food_x = random.randint(0, SIZE - 1)
    food_y = random.randint(0, SIZE - 1)

    if (food_x, food_y) != (creature_x, creature_y) and (food_x, food_y) not in foods:
        foods.append((food_x, food_y))
        world[food_y][food_x] = "F"


world[creature_y][creature_x]="C"

print(f"Creature's energy: {creature_energy}")
for row in world:
    print(" ".join(row))
print()
print("-------------------------------------------------")


while creature_energy > 0:
    turns_survived += 1
    dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
    new_x=creature_x + dx
    new_y=creature_y + dy

    if 0 <= new_x < SIZE and 0 <= new_y < SIZE:
        world[creature_y][creature_x]="."
        creature_x=new_x
        creature_y=new_y
        creature_energy -= 1
        world[creature_y][creature_x]="C"
        
        if (creature_x, creature_y) in foods:
            print("The creature has found the food!")
            food_eaten += 1
            creature_energy = min(creature_energy + 5, MAX_ENERGY)

            foods.remove((creature_x, creature_y))

            while True:
                food_x = random.randint(0, SIZE - 1)
                food_y = random.randint(0, SIZE - 1)

                if (
                    (food_x, food_y) != (creature_x, creature_y)
                    and (food_x, food_y) not in foods
                ):
                    foods.append((food_x, food_y))
                    world[food_y][food_x] = "F"
                    break

            print(f"Creature's energy: {creature_energy}")


    else:
        print("The creature hit the wall and lost energy.")
        print()
        creature_energy -= 1
        walls_hit += 1

    print(f"Creature's energy: {creature_energy}")

    for row in world:
        print(" ".join(row))
    print("-------------------------------------------------")
    print()
print("The creature has run out of energy!")
print("the creature has died. GAME OVER")
print(f"Turns survived: {turns_survived}")
print(f"Walls hit: {walls_hit}")
print(f"Food eaten: {food_eaten}")
