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
    with open("character_data.txt", "w") as file:
        # Use the custom encoder for serialization
        character_data = json.dumps(character, cls=WeaponEncoder)
        file.write(character_data)

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
            Weapon(item['name'], item['damage_range']) if 'damage_range' in item else item
            for item in character_data['inventory']
        ]

        # Convert 'current_weapon' dictionary to Weapon object
        if 'current_weapon' in character_data and character_data['current_weapon'] is not None:
            character_data['current_weapon'] = Weapon(character_data['current_weapon']['name'],
                                                      character_data['current_weapon']['damage_range'])

        character = character_data
        return character
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
    character['level'] += 1
    character['exp'] = 0
    character['bonus_points'] += 1
    character['health'] += random.randint(5, 10)
    character['strength'] += random.randint(1, 3)
    character['intelligence'] += random.randint(1, 3)
    character['dexterity'] += random.randint(1, 3)

def allocate_bonus_points(character):
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
        character['bonus_points'] -= 1
        print(f"You allocated a bonus point to {attribute}.")
    else:
        print("Invalid choice. Bonus point not allocated.")

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
    if character['current_weapon']:
        print(f"{character['current_weapon'].name} ({character['current_weapon'].damage_range[0]} - {character['current_weapon'].damage_range[1]} damage)")
    else:
        print("None")

    print("Inventory:")
    for item in character['inventory']:
        if isinstance(item, Weapon):
            print(f"- {item.name} ({item.damage_range[0]} - {item.damage_range[1]} damage)")
        else:
            print(f"- {item}")

    print("-------------------------")


def run_away(character):
    success_rate = character['dexterity'] * 2  # Higher dexterity increases the chance of success
    return random.randint(1, 100) <= success_rate

def encounter_boss(character):
    print("You encounter a fearsome boss!")
    choice = input("Do you want to (F)ight or (R)un? ").lower()

    if choice == 'f':
        boss_strength = 20  # You can customize the boss strength
        battle(character, boss_strength)
    elif choice == 'r':
        if run_away(character):
            print("You successfully ran away!")
        else:
            print("You couldn't escape! Prepare for battle.")
            boss_strength = 20  # You can customize the boss strength
            battle(character, boss_strength)
    else:
        print("Invalid choice. The boss eyes you menacingly.")

    print("The evil force's influence intensifies, manifesting into a fearsome creature known as the Shadow Serpent.")
    print("It lurks in the shadows, terrorizing the village. It's up to you to confront this menace and protect your home.")

    enemy_strength = random.randint(15, 25)

    print("\nMiniboss Encounter:")
    print(f"You encounter the Shadow Serpent with strength {enemy_strength}!")

    choice = input("Do you want to (F)ight or (R)un? ").lower()

    if choice == 'f':
        battle(character, enemy_strength)

        # Check if the player won the battle before printing the conclusion
        if character['exp'] >= 0:
            print("\n----- Conclusion -----")
            print(f"Congratulations, {character['name']}! You have defeated the Shadow Serpent and become the village's new hero.")
            print("The village is saved, and your courage is celebrated by all.")
        else:
            print("\n----- Conclusion -----")
            print(f"Despite the challenges, {character['name']} couldn't defeat the Shadow Serpent.")
            print("The village struggles under the influence of the evil force.")

        print("\nThank you for playing the Text-based RPG. Goodbye!")

    elif choice == 'r':
        if run_away(character):
            print("You successfully retreat, but the Shadow Serpent's presence lingers over the village.")
        else:
            print("You couldn't escape! Prepare for battle.")
            battle(character, enemy_strength)
    else:
        print("Invalid choice. The Shadow Serpent hisses in anticipation.")


def explore_area(character):
    if random.choice([True, False]):
        # Simulate a scenario or battle where the player gains XP
        enemy_strength = random.randint(5, 15)
        print(f"\nYou encounter an enemy with strength {enemy_strength}!")

        # Give the player the option to fight or run
        choice = input("Do you want to (F)ight or (R)un? ").lower()

        if choice == 'f':
            battle(character, enemy_strength)
        elif choice == 'r':
            if run_away(character):
                print("You successfully ran away!")
            else:
                print("You couldn't escape! Prepare for battle.")
                battle(character, enemy_strength)
    else:
        encounter_boss(character)

def generate_loot():
    loot_types = ["Gold", "Health Potion", "Sword", "Axe", "Bow"]
    return random.choice(loot_types)

def add_to_inventory(character, loot):
    if loot == "Gold":
        character['inventory'].append(loot)
        print(f"You found {loot}!")
    elif loot == "Health Potion":
        character['inventory'].append({"name": loot})
        print(f"You found a {loot}! It has been added to your inventory.")
    elif loot in ["Sword", "Axe", "Bow"]:
        weapon = {"name": loot, "damage_range": [5, 15]}  # You can customize damage ranges
        character['inventory'].append(weapon)
        print(f"You found a {loot}! It has been added to your inventory.")
    else:
        print("Unknown item.")

def battle(character, enemy_strength):
    # Simulate a battle
    if character['strength'] >= enemy_strength:
        print("You defeated the enemy!")
        character['exp'] += random.randint(10, 20)

        # Check if the player leveled up
        if character['exp'] >= 50:
            level_up(character)
            allocate_bonus_points(character)

        # Generate loot after defeating an enemy
        loot = generate_loot()
        add_to_inventory(character, loot)
    else:
        print("You were defeated. Game Over.")

def main():
    # Check if a character exists or create a new one
    character = load_character()
    if character is None:
        print("No character found. Let's create a new one.")
        character = create_character()
        save_character(character)
    else:
        print(f"Welcome back, {character['name']}!")

    # Game loop
    while character['level'] <= 5:  # Set a limit for the sake of example
        print_character_info(character)

        # Give the player the option to explore or exit
        choice = input("Do you want to (E)xplore, (I)nv, or (Q)uit? ").lower()

        if choice == 'e':
            explore_area(character)
        elif choice == 'i':
            # Display inventory and allow the player to equip weapons
            print("Inventory:")
            for item in character['inventory']:
                if isinstance(item, Weapon):
                    print(f"- {item.name} ({item.damage_range[0]} - {item.damage_range[1]} damage)")
                else:
                    print(f"- {item}")
            
            equip_choice = input("Type the name of the weapon you want to equip (or type 'Q' to go back): ").capitalize()

            if equip_choice == 'Q':
                continue

            found_weapon = None
            for item in character['inventory']:
                if isinstance(item, Weapon) and item.name.lower() == equip_choice.lower():
                    found_weapon = item
                    break
                elif isinstance(item, dict) and 'name' in item and item['name'].lower() == equip_choice.lower():
                    found_weapon = Weapon(item['name'], item['damage_range'])
                    break

            if found_weapon:
                character['current_weapon'] = found_weapon
                print(f"You have equipped {found_weapon.name}.")
            else:
                print("Invalid choice. No such weapon in your inventory.")
        elif choice == 'q':
            print("Exiting the game. Goodbye!")
            break

        # Save character data after each scenario
        save_character(character)

if __name__ == "__main__":
    main()
