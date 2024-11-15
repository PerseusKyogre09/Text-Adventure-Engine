import json
import random


class Weapon:
    def __init__(self, name, damage_range):
        self.name = name
        self.damage_range = damage_range

    def to_json(self):
        return {
            "name": self.name,
            "damage_range": self.damage_range,
        }

    @staticmethod
    def from_dict(data):
        if isinstance(data, dict) and "name" in data and "damage_range" in data:
            return Weapon(data["name"], data["damage_range"])
        return None


class WeaponEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Weapon):
            return obj.to_json()
        return super().default(obj)


def create_character():
    print("Welcome to the Text-based RPG!")
    name = input("Enter your character's name: ")

    character = {
        "name": name,
        "health": 100,
        "strength": 10,
        "intelligence": 10,
        "dexterity": 10,
        "level": 1,
        "exp": 0,
        "bonus_points": 0,
        "current_weapon": None,
        "inventory": [],
    }
    return character


def save_character(character):
    with open("character_data.json", "w") as file:
        character_data = {
            **character,
            "current_weapon": character["current_weapon"].to_json() if character["current_weapon"] else None,
            "inventory": [
                item.to_json() if isinstance(item, Weapon) else item
                for item in character["inventory"]
            ],
        }
        json.dump(character_data, file, indent=4, cls=WeaponEncoder)


def load_character():
    try:
        with open("character_data.json", "r") as file:
            character_data = json.load(file)

        character_data["current_weapon"] = (
            Weapon.from_dict(character_data["current_weapon"])
            if character_data["current_weapon"]
            else None
        )

        character_data["inventory"] = [
            Weapon.from_dict(item) if Weapon.from_dict(item) else item
            for item in character_data["inventory"]
        ]

        return character_data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def level_up(character):
    print(f"Congratulations, {character['name']}! You leveled up!")
    character["level"] += 1
    character["exp"] = 0
    character["bonus_points"] += 1
    character["health"] += random.randint(5, 10)
    character["strength"] += random.randint(1, 3)
    character["intelligence"] += random.randint(1, 3)
    character["dexterity"] += random.randint(1, 3)


def allocate_bonus_points(character):
    while character["bonus_points"] > 0:
        print(f"You have {character['bonus_points']} bonus points to allocate.")
        print("1. Health")
        print("2. Strength")
        print("3. Intelligence")
        print("4. Dexterity")

        choice = input("Choose an attribute to allocate a bonus point (1-4): ")
        if choice.isdigit() and 1 <= int(choice) <= 4:
            attribute = ""
            if choice == "1":
                attribute = "health"
            elif choice == "2":
                attribute = "strength"
            elif choice == "3":
                attribute = "intelligence"
            elif choice == "4":
                attribute = "dexterity"

            character[attribute] += 1
            character["bonus_points"] -= 1
            print(f"You allocated a bonus point to {attribute}.")
        else:
            print("Invalid choice. Try again.")


def print_character_info(character):
    print("\n----- Character Info -----")
    print(f"Name: {character['name']}")
    print(f"Level: {character['level']}")
    print(f"Health: {character['health']}")
    print(f"Strength: {character['strength']}")
    print(f"Intelligence: {character['intelligence']}")
    print(f"Dexterity: {character['dexterity']}")
    print(f"Experience: {character['exp']}")
    print(f"Bonus Points: {character['bonus_points']}")

    print("Current Weapon:", end=" ")
    if character["current_weapon"]:
        print(
            f"{character['current_weapon'].name} ({character['current_weapon'].damage_range[0]} - {character['current_weapon'].damage_range[1]} damage)"
        )
    else:
        print("None")

    print("Inventory:")
    for item in character["inventory"]:
        if isinstance(item, Weapon):
            print(f"- {item.name} ({item.damage_range[0]} - {item.damage_range[1]} damage)")
        else:
            print(f"- {item}")

    print("-------------------------")


def run_away(character):
    success_rate = character["dexterity"] * 2
    return random.randint(1, 100) <= success_rate


def battle(character, enemy_strength):
    print(f"\nAn enemy with strength {enemy_strength} appears!")
    if character["strength"] >= enemy_strength:
        print("You defeated the enemy!")
        character["exp"] += random.randint(10, 20)
        if character["exp"] >= 50:
            level_up(character)
            allocate_bonus_points(character)

        loot = generate_loot()
        add_to_inventory(character, loot)
    else:
        print("You were defeated. Game Over.")


def generate_loot():
    loot_types = ["Gold", "Health Potion", "Sword", "Axe", "Bow"]
    loot_name = random.choice(loot_types)
    if loot_name in ["Sword", "Axe", "Bow"]:
        return Weapon(loot_name, [5, 15])
    return loot_name


def add_to_inventory(character, loot):
    character["inventory"].append(loot)
    if isinstance(loot, Weapon):
        print(f"You found a {loot.name}! It has been added to your inventory.")
    else:
        print(f"You found {loot}!")


def explore_area(character):
    if random.choice([True, False]):
        enemy_strength = random.randint(5, 15)
        battle(character, enemy_strength)
    else:
        print("The area seems peaceful. You found nothing.")


def main():
    character = load_character()
    if character is None:
        print("No character found. Let's create a new one.")
        character = create_character()
        save_character(character)
    else:
        print(f"Welcome back, {character['name']}!")

    while True:
        print_character_info(character)
        choice = input("Do you want to (E)xplore, (I)nventory, or (Q)uit? ").lower()

        if choice == "e":
            explore_area(character)
        elif choice == "i":
            print("Inventory:")
            for item in character["inventory"]:
                if isinstance(item, Weapon):
                    print(f"- {item.name} ({item.damage_range[0]} - {item.damage_range[1]} damage)")
                else:
                    print(f"- {item}")
            equip_choice = input("Type the name of the weapon to equip or 'Q' to quit: ").capitalize()
            if equip_choice == "Q":
                continue
            for item in character["inventory"]:
                if isinstance(item, Weapon) and item.name == equip_choice:
                    character["current_weapon"] = item
                    print(f"You equipped {item.name}.")
                    break
            else:
                print("Weapon not found in inventory.")
        elif choice == "q":
            print("Saving progress and exiting the game. Goodbye!")
            save_character(character)
            break


if __name__ == "__main__":
    main()
