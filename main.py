
import random

SIZE = 10
MAX_ENERGY = 10
FOOD_COUNT = 5
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
FOOD_ENERGY = 5


class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = MAX_ENERGY
        self.last_position = None
        self.turns_survived = 0
        self.walls_hit = 0
        self.food_eaten = 0
        self.creatures_absorbed = 0

    def is_alive(self):
        return self.energy > 0

    def choose_move(self):
        while True:
            dx, dy = random.choice(DIRECTIONS)
            new_x, new_y = self.x + dx, self.y + dy

            if (
                self.last_position is None
                or (new_x, new_y) != self.last_position
            ):
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
        self.energy = min(
            self.energy + FOOD_ENERGY,
            MAX_ENERGY
        )

    def absorb(self, other):
        self.food_eaten += other.food_eaten
        self.turns_survived += other.turns_survived
        self.walls_hit += other.walls_hit
        self.creatures_absorbed += other.creatures_absorbed + 1
        self.energy = min(self.energy + other.energy, MAX_ENERGY)


def create_world():
    world = []

    for _ in range(SIZE):
        world.append(["."] * SIZE)

    return world


def spawn_foods(creatures):
    for creature in creatures:
        if creature.is_alive():
            creature.last_position = None

    occupied = {
        (c.x, c.y)
        for c in creatures
        if c.is_alive()
    }

    foods = []

    while len(foods) < FOOD_COUNT:
        food_x = random.randint(0, SIZE - 1)
        food_y = random.randint(0, SIZE - 1)

        if (
            (food_x, food_y) not in occupied
            and (food_x, food_y) not in foods
        ):
            foods.append((food_x, food_y))

    return foods


def in_bounds(x, y):
    return 0 <= x < SIZE and 0 <= y < SIZE


def build_grid(creatures, foods):
    grid = create_world()

    for food_x, food_y in foods:
        grid[food_y][food_x] = "F"

    for creature in creatures:
        if creature.is_alive():
            grid[creature.y][creature.x] = "C"

    return grid


def print_world(creatures, foods):
    for i, creature in enumerate(creatures):
        status = "Alive" if creature.is_alive() else "Dead"

        print(
            f"Creature {i + 1} | {status} | "
            f"Energy: {creature.energy} | "
            f"Food eaten: {creature.food_eaten} |"
            f"Creatures absorbed: {creature.creatures_absorbed}"
        )

    for row in build_grid(creatures, foods):
        print(" ".join(row))

    print("-" * 50)
    print()


def creature_at(x, y, creatures, moving_creature):
    for other in creatures:
        if (
            other is not moving_creature
            and other.is_alive()
            and (other.x, other.y) == (x, y)
        ):
            return other

    return None


def take_turn(creature, creatures, foods):
    creature.turns_survived += 1

    new_x, new_y = creature.choose_move()

    if not in_bounds(new_x, new_y):
        print("The creature hit the wall and lost energy.")
        creature.hit_wall()
        return foods

    other = creature_at(
        new_x, new_y, creatures, creature
    )

    if other is not None:
        if creature.food_eaten > other.food_eaten:
            print("The moving creature wins the encounter!")

            creature.absorb(other)
            creatures.remove(other)
            creature.move(new_x, new_y)

        elif other.food_eaten > creature.food_eaten:
            print("The moving creature loses the encounter!")

            other.absorb(creature)
            creatures.remove(creature)
            return foods

        else:
            print("Encounter tied! Neither creature replaces the other.")
            return foods

    else:
        creature.move(new_x, new_y)

    if (creature.x, creature.y) in foods:
        print("The creature has found the food!")

        creature.eat_food()
        foods.remove((creature.x, creature.y))

        if not foods:
            print("All food has been eaten! Respawning food...")
            foods = spawn_foods(creatures)

    return foods


def main():
    print("Welcome to the Artificial World Simulation!")

    while True:
        try:
            creature_count = int(
                input("Enter the number of creatures (1-5): ")
            )

            if 1 <= creature_count <= 5:
                break

            print("Please enter a number between 1 and 5.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")

    creatures = []

    while len(creatures) < creature_count:
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)

        if all(
            (c.x, c.y) != (x, y)
            for c in creatures
        ):
            creatures.append(Creature(x, y))

    foods = spawn_foods(creatures)

    print_world(creatures, foods)

    while any(c.is_alive() for c in creatures):
        for creature in creatures.copy():
            if creature in creatures and creature.is_alive():
                foods = take_turn(
                    creature, creatures, foods
                )

        print_world(creatures, foods)

    print("All creatures have died. GAME OVER")
    print("-" * 50)
    print("Final Stats:")

    for i, creature in enumerate(creatures):
        print(f"Creature {i + 1}")
        print(f"Turns survived: {creature.turns_survived}")
        print(f"Walls hit: {creature.walls_hit}")
        print(f"Food eaten: {creature.food_eaten}")
        print(f"Final energy: {creature.energy}")
        print(f"Creatures absorbed: {creature.creatures_absorbed}")
        print()



if __name__ == "__main__":
    main()
