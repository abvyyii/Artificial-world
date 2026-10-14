import random
SIZE=10
MAX_ENERGY=10
FOOD_COUNT = 5
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
FOOD_ENERGY = 5

class Creature:
    def __init__(self, x , y):
        self.x=x
        self.y=y
        self.energy=MAX_ENERGY
        self.last_position=None
        self.turns_survived=0
        self.walls_hit=0
        self.food_eaten=0

    def is_alive(self):
        return self.energy > 0

    def choose_move(self):
        while True:
            dx, dy = random.choice(DIRECTIONS)
            new_x , new_y = self.x + dx, self.y + dy

            if self.last_position is None or (new_x, new_y) != self.last_position:
                return new_x, new_y

    def move(self, new_x, new_y):
        self.last_position = (self.x, self.y)
        self.x, self.y = new_x, new_y
        self.energy -= 1

    def hit_wall(self):
        self.walls_hit += 1
        self.energy -= 1

    def eat_food(self):
        self.food_eaten += 1
        self.energy = min(self.energy + FOOD_ENERGY, MAX_ENERGY)


def create_world():
    world=[]
    for _ in range(SIZE):
        world.append(["."] * SIZE)
    return world   

def spawn_foods(world, creature):
    creature.last_position = None   # respawn also resets this creature's memory

    foods = []
    while len(foods) < FOOD_COUNT:
        food_x = random.randint(0, SIZE - 1)
        food_y = random.randint(0, SIZE - 1)

        if (food_x, food_y) != (creature.x, creature.y) and (food_x, food_y) not in foods:
            foods.append((food_x, food_y))
            world[food_y][food_x] = "F"
    return foods

def in_bounds(x, y):
    return 0 <= x < SIZE and 0 <= y < SIZE

def print_world(world, creature):
    print(f"Creature's energy: {creature.energy}")
    for row in world:
        print(" ".join(row))
    print("-"*50)
    print()

def main():
    world = create_world()
    print("Welcome to the Artificial World Simulation!")

    creature = Creature(random.randint(0, SIZE - 1), random.randint(0, SIZE - 1))
    foods = spawn_foods(world, creature)
    world[creature.y][creature.x] = "C"
    print_world(world, creature)

    while creature.is_alive():
        creature.turns_survived += 1
        new_x, new_y = creature.choose_move()

        if in_bounds(new_x, new_y):
            world[creature.y][creature.x] = "."
            creature.move(new_x, new_y)
            world[creature.y][creature.x] = "C"

            if (creature.x, creature.y) in foods:
                print("The creature has found the food!")
                creature.eat_food()
                foods.remove((creature.x, creature.y))

                if not foods:
                    print("All food has been eaten! Respawning food...")
                    foods = spawn_foods(world, creature)   # also resets last_position
        else:
            print("The creature hit the wall and lost energy.")
            print()
            creature.hit_wall()

        print_world(world, creature)

    print("The creature has run out of energy!")
    print("The creature has died. GAME OVER")
    print("-"*50)
    print("Final Stats::")
    print(f"Turns survived: {creature.turns_survived}")
    print(f"Walls hit: {creature.walls_hit}")
    print(f"Food eaten: {creature.food_eaten}")


if __name__ == "__main__":
    main()