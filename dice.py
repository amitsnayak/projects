import random

print(""
" Welcome to the Dice Roller Simulator!")

while True:
    input("Press Enter to roll the dice... ")
    dice_roll = random.randint(1, 6)
    print(f"You rolled a {dice_roll}!")

    again = input("Roll again? (yes/no): ").lower()
    if again != "yes":
        print("Goodbye! ")
        break
