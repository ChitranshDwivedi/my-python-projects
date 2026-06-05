import random

def sort(name):
    houses = ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]
    return random.choice(houses)

def main():
    name = input("What is your name? ").strip()
    house = sort(name)
    print(f"{name}, you belong in {house}!")

main()