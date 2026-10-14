import random
world=[]
SIZE=10
for row in range(SIZE):
    world.append(["."] * SIZE)

creature_x=random.randint(0, SIZE-1)
creature_y=random.randint(0, SIZE-1)



food_x=random.randint(0, SIZE-1)
food_y=random.randint(0, SIZE-1)

world[food_y][food_x]="F"
world[creature_y][creature_x]="C"

for row in world:
    print(" ".join(row))
print()

for step in range(10):
    dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
    new_x=creature_x + dx
    new_y=creature_y + dy
    if 0 <= new_x < SIZE and 0 <= new_y < SIZE:
        world[creature_y][creature_x]="."
        creature_x=new_x
        creature_y=new_y
        world[creature_y][creature_x]="C"
    for row in world:
        print(" ".join(row))
    print()
    if new_x == food_x and new_y == food_y:
        print("The creature has found the food!")
        break