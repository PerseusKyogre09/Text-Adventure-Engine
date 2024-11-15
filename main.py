import json
import random

# Weapon Class
class Weapon:
    def __init__(self, name, damage_range, durability, critical_hit_chance=0.1, special_effects=None):
        self.name = name
        self.damage_range = damage_range
        self.durability = durability
        self.critical_hit_chance = critical_hit_chance
        self.special_effects = special_effects or []

    def calculate_damage(self):
        base_damage = random.randint(*self.damage_range)
        if random.random() < self.critical_hit_chance:
            print(f"Critical hit with {self.name}!")
            return base_damage * 2
        return base_damage

    def use_weapon(self):
        self.durability -= 1
        if self.durability <= 0:
            print(f"Your {self.name} broke!")
            return False
        return True

    def to_json(self):
        return {
            "name": self.name,
            "damage_range": self.damage_range,
            "durability": self.durability,
            "critical_hit_chance": self.critical_hit_chance,
            "special_effects": self.special_effects,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["damage_range"],
            data["durability"],
            data.get("critical_hit_chance", 0.1),
            data.get("special_effects", []),
        )

    def calculate_damage(self):
        damage = random.randint(*self.damage_range)
        if random.random() < self.critical_chance:
            damage *= 2 # Double damage for critical hit
            print(f"Critical hit with {self.name}! Damage is doubled.")
        return damage

    def use_weapon(self):
        """Decreases durability when the weapon is used."""
        if self.durability > 0:
            self.durability -= 1
            if self.durability == 0:
                print(f"{self.name} broke!")
            return True
        else:
            print(f"{self.name} is broken and cannot be used.")
            return False

# Weapon Table       
unique_weapons = [
    Weapon("Iron Sword", [8, 12], durability=15, critical_hit_chance=0.15),
    Weapon("Battle Axe", [10, 20], durability=10, critical_hit_chance=0.1, special_effects=["Armor Pierce"]),
    Weapon("Enchanted Bow", [6, 14], durability=20, critical_hit_chance=0.25, special_effects=["Poison"]),
    Weapon("Legendary Blade", [15, 25], durability=25, critical_hit_chance=0.3, special_effects=["Burn"]),
    Weapon("Dagger of Shadows", [4, 10], durability=30, critical_hit_chance=0.4, special_effects=["Bleed"]),
]

class WeaponEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Weapon):
            return obj.to_json()
        return super().default(obj)

# Character Functions
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
        json.dump(character_data, file, indent=4)


def load_character():
    try:
        with open("character_data.txt", "r") as file:
            character_data = json.load(file)
        
        # Handle the case where 'current_weapon' is not present (old character data)
        character_data.setdefault('current_weapon', None)

        # Handle the case where 'inventory' is not present (old character data)
        character_data.setdefault('inventory', [])

        # If 'inventory' contains dictionaries, assume they are Weapon objects and convert them
        character_data['inventory'] = [
            Weapon.from_dict(item) if isinstance(item, dict) and 'damage_range' in item else item
            for item in character_data['inventory']
        ]

        # Convert 'current_weapon' dictionary to Weapon object
        if 'current_weapon' in character_data and isinstance(character_data['current_weapon'], dict):
            character_data['current_weapon'] = Weapon.from_dict(character_data['current_weapon'])

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

def run_away(character):
    success_rate = character["dexterity"] * 2
    return random.randint(1, 100) <= success_rate

def battle(character, enemy_strength):
    """
    Handles a turn-based battle between the player and an enemy.
    """
    enemy_health = 50 + enemy_strength
    print(f"\nAn enemy with strength {enemy_strength} has appeared!")
    print(f"The enemy has {enemy_health} health points.")

    while enemy_health > 0 and character["health"] > 0:
        print("\n----- Your Turn -----")
        print("Choose your action:")
        print("1. Attack")
        print("2. Use Tool")
        print("3. Run")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            # Player attacks
            weapon = character["current_weapon"]
            if weapon:
                if weapon.use_weapon():
                    damage = weapon.calculate_damage()
                    print(f"You attack with {weapon.name}, dealing {damage} damage!")
                else:
                    damage = 0  # No damage if weapon breaks
            else:
                damage = random.randint(5, 10)  # Default damage
                print(f"You punch the enemy, dealing {damage} damage!")

            enemy_health -= damage
            print(f"The enemy now has {max(0, enemy_health)} health.")

            # If enemy is defeated
            if enemy_health <= 0:
                print("You defeated the enemy!")
                character['exp'] += random.randint(10, 20)

                if character['exp'] >= 50:
                    level_up(character)
                    allocate_bonus_points(character)

                loot = generate_loot()
                add_to_inventory(character, loot)

                # Generate loot
                loot = generate_loot()
                add_to_inventory(character, loot)
                break

        elif choice == "2":
            # Use a tool
            if any(item == "Health Potion" for item in character["inventory"]):
                character["inventory"].remove("Health Potion")
                heal_amount = random.randint(15, 30)
                character["health"] = min(character["health"] + heal_amount, 100)
                print(f"You used a Health Potion and restored {heal_amount} health.")
                print(f"Your health is now {character['health']}.")
            else:
                print("You don't have any tools to use!")
        elif choice == "3":
            # Run option
            if run_away(character):
                print("You successfully escaped!")
                return
            else:
                print("You failed to escape! The enemy blocks your way.")
        else:
            print("Invalid choice! You lose your turn.")

        # Enemy's attack
        if enemy_health > 0:
            print("\nEnemy's turn!")
            enemy_damage = random.randint(1, max(5, enemy_strength // 2))
            character['health'] -= enemy_damage
            print(f"The enemy deals {enemy_damage} damage to you. Your health is now {max(0, character['health'])}.")

            # Check if the player is defeated
            if character['health'] <= 0:
                print("You were defeated. Game Over.")
                break

    print("\nThe battle has ended.")

def generate_loot():
    loot_table = {
        "Common": ["Gold", "Health Potion", "Wooden Shield"],
        "Rare": ["Steel Helmet", unique_weapons[0], unique_weapons[1]],
        "Epic": ["Enchanted Ring", unique_weapons[2]],
        "Legendary": [unique_weapons[3], unique_weapons[4]],
    }

    loot_chance = random.random()
    if loot_chance < 0.2:  # 20% chance of not getting loot
        print("You didn't find any loot this time.")
        return None

    rarity = random.choices(
        ["Common", "Rare", "Epic", "Legendary"],
        weights=[60, 25, 10, 5],  # Probability distribution of Items
        k=1
    )[0]

    item = random.choice(loot_table[rarity])
    print(f"You found a {rarity} item: {item.name if isinstance(item, Weapon) else item}!")
    return item




def add_to_inventory(character, loot):
    if isinstance(loot, Weapon):
        character['inventory'].append(loot)
        print(f"The {loot.name} has been added to your inventory.")
    elif isinstance(loot, str):
        print(f"You found some {loot}! Added to your inventory.")
        if loot == "Gold":
            character['inventory'].append({"type": "Gold", "amount": random.randint(10, 50)})
        elif loot == "Health Potion":
            character['inventory'].append({"type": "Health Potion", "effect": "Restore 20 HP"})
        else:
            character['inventory'].append({"type": loot})
    else:
        print(f"You found a {loot}! Added to your inventory.")
        character['inventory'].append(loot)

def explore_area(character):
    if random.choice([True, False]):
        enemy_strength = random.randint(5, 15)
        battle(character, enemy_strength)
    else:
        print("The area seems peaceful. You found nothing.")

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
    if not character["inventory"]:
        print("Your inventory is empty.")
    else:
        for index, item in enumerate(character["inventory"], 1):
            if isinstance(item, Weapon):
                print(f"{index}. {item.name} ({item.damage_range[0]} - {item.damage_range[1]} damage)")
            else:
                print(f"{index}. {item}")

    print("-------------------------")

def select_item_from_inventory(character):
    print("Select an item from your inventory by number.")
    for index, item in enumerate(character["inventory"], 1):
        print(f"{index}. {item.name if isinstance(item, Weapon) else item}")

    choice = input("Enter the number of the item to equip or 'Q' to quit: ").capitalize()

    if choice == 'Q':
        return None

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(character["inventory"]):
            item = character["inventory"][choice - 1]
            if isinstance(item, Weapon):
                character["current_weapon"] = item
                print(f"You equipped {item.name}.")
            else:
                print(f"{item} is not a weapon and can't be equipped.")
        else:
            print("Invalid choice. Please select a valid number.")
    else:
        print("Invalid input. Please enter a valid number or 'Q' to quit.")

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
            select_item_from_inventory(character)
        elif choice == "q":
            print("Saving progress and exiting the game. Goodbye!")
            save_character(character)
            break

if __name__ == "__main__":
    main()
