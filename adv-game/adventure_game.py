import random

rooms = {
    "entrance": {
        "description": "This is the entrance of the castle. You can go east to the dungeon.",
        "exits": {"east": "dungeon"},
        "items": [],
    },
    "dungeon": {
        "description": "This is the dungeon. You can go west to the entrance and south to the boss room.",
        "exits": {"west": "entrance", "south": "boss_room"},
        "items": ["potion", "sword", "shield"],
    },
    "boss_room": {
        "description": "This is the boss room. You can go north to the dungeon.",
        "exits": {"north": "dungeon"},
        "items": ["treasure"],
        "enemy": {
            "name": "Dragon",
            "health": 100,
            "attack": 20,
            "defense": 5,
            "description": "A dragon is guarding the treasure. Defeat it to get the treasure.",
        },
    },
}

player = {
    "health": 100,
    "current_room": "entrance",
    "inventory": [],
    "name": "",
    "attack": 5,
    "defense": 5,
}


def display_room(room: str):
    print("\n" + "=" * 20)
    print("Description: " + room["description"])
    print("Exits: " + ", ".join(room["exits"]))
    if room["items"]:
        print("Items: " + ", ".join(room["items"]))
    else:
        print("Items: None")
    print("=" * 20)


def move_player(direction: str):
    if direction in rooms[player["current_room"]]["exits"]:
        player["current_room"] = rooms[player["current_room"]]["exits"][direction]
        display_room(rooms[player["current_room"]])
    else:
        print("You can't go that way!")


def get_item(item: str):
    if item in rooms[player["current_room"]]["items"]:
        player["inventory"].append(item)
        rooms[player["current_room"]]["items"].remove(item)
        print("You have picked up the " + item + ".")
    else:
        print(item + " is not available in this room.")


def use_item(item: str):
    if item in player["inventory"]:
        if item == "potion":
            player["health"] += 20
            print(
                "You have used the potion. Your health is now "
                + str(player["health"])
                + "."
            )
        elif item == "sword":
            player["attack"] += 10
            player["inventory"].remove(item)
            print(
                "You have equipped the sword. Your attack is now "
                + str(player["attack"])
                + "."
            )
        elif item == "shield":
            player["defense"] += 10
            player["inventory"].remove(item)
            print(
                "You have equipped the shield. Your defense is now "
                + str(player["defense"])
                + "."
            )
        else:
            print("You can't use the " + item + ".")
    else:
        print("You can't find the " + item + ".")


def combat(enemy):
    print(f"You have encountered a {enemy['name']}!")
    print(enemy["description"])

    def display_health():
        print(
            f"Your Health: {player['health']}  |  {enemy['name']}'s Health: {enemy['health']}"
        )

    combat_actions = {
        "attack": lambda: max(
            player["attack"] + random.randint(1, 10) - enemy["defense"], 0
        ),
        "defend": lambda: setattr(player, "defense", player["defense"] + 5),
        "use": lambda item: use_item(item),
        "examine": lambda: print(
            f"{enemy['name']} - {enemy['description']}. Attack: {enemy['attack']}, Defense: {enemy['defense']}"
        ),
    }

    while player["health"] > 0 and enemy["health"] > 0:
        display_health()
        print("\nWhat do you want to do?")
        for action in combat_actions:
            print(f"- {action}")
        choice = input().lower().split()

        if choice[0] == "run":
            print(f"You have escaped from the {enemy['name']}.")
            return "escape"

        if choice[0] in combat_actions:
            if choice[0] == "attack":
                damage = combat_actions[choice[0]]()
                enemy["health"] -= damage
                print(f"You deal {damage} damage to the {enemy['name']}!")
            elif choice[0] == "defend":
                combat_actions[choice[0]]()
                print("Your defense has increased for this turn!")
            elif choice[0] == "use":
                if len(choice) > 1:
                    combat_actions[choice[0]](choice[1])
                else:
                    print("Please specify an item to use.")
                    continue
            else:
                combat_actions[choice[0]]()
        else:
            print("Invalid action. Try again.")
            continue

        if enemy["health"] <= 0:
            print(f"You have defeated the {enemy['name']}!")
            return "victory"

        # Enemy's turn
        enemy_damage = max(
            enemy["attack"] + random.randint(1, 10) - player["defense"], 0
        )
        player["health"] -= enemy_damage
        print(f"The {enemy['name']} deals {enemy_damage} damage to you!")

        if player["health"] <= 0:
            print(f"You have been defeated by the {enemy['name']}.")
            return "defeat"

        # Reset defense if it was increased
        if choice[0] == "defend":
            player["defense"] -= 5

    return "defeat"  # This should never be reached, but it's here as a fallback


def main():
    print("Welcome to the Castle Adventure!")
    player["name"] = input("Enter your name, brave adventurer: ")
    player["score"] = 0
    print(
        f"Welcome, {player['name']}! Your quest to explore the castle and defeat the Dragon King begins..."
    )

    commands = {
        "move": lambda direction: move_player(direction),
        "get": lambda item: get_item(item),
        "use": lambda item: use_item(item),
        "inventory": lambda: print("Your inventory: " + ", ".join(player["inventory"])),
        "look": lambda: display_room(rooms[player["current_room"]]),
        "fight": lambda: (
            combat(rooms[player["current_room"]]["enemy"])
            if "enemy" in rooms[player["current_room"]]
            else print("There is no enemy here.")
        ),
        "quit": lambda: "quit",
    }

    display_room(rooms[player["current_room"]])

    while True:
        action = input("What do you want to do? ").lower().split()

        if not action:
            print("Please enter a command.")
            continue

        command = action[0]
        args = action[1:]

        if command in commands:
            if command in ["move", "get", "use"] and not args:
                print(
                    f"Please specify a direction or item for the '{command}' command."
                )
                continue

            result = commands[command](*args)

            if result == "quit":
                print("Thanks for playing!")
                break

            if command == "fight":
                if result == "victory":
                    print("Congratulations! You've won the battle!")
                    if player["current_room"] == "boss_room":
                        print("You've defeated the final boss and won the game!")
                        break
                elif result == "defeat":
                    print("Game Over. You've been defeated.")
                    break
                elif result == "escape":
                    print("You've escaped from the battle.")

        else:
            print(
                "I don't understand that command. Try 'move', 'get', 'use', 'inventory', 'look', 'fight', or 'quit'."
            )

        # Check if player's health is zero
        if player["health"] <= 0:
            print("Your health has reached zero. Game Over.")
            break


if __name__ == "__main__":
    main()
