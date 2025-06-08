import random
import math

#def genWWDice():
letterProbabilities = {  #Define exact probability percentages (sum should be ~100%)
    'A': 7,
    'B': 3,
    'C': 2,
    'D': 6,
    'E': 10,
    'F': 4,
    'G': 3,
    'H': 3,
    'I': 5,
    'J': 2,
    'K': 2,
    'L': 4,
    'M': 3,
    'N': 4,
    'O': 6,
    'P': 3,
    'Qu': 1,
    'R': 4,
    'S': 5,
    'T': 6,
    'U': 4,
    'V': 2,
    'W': 3,
    'X': 2,
    'Y': 4,
    'Z': 2
    }

numDice = int(input("Enter number of dice:  "))
numFaces = int(input("Enter number of faces per die:  "))

# Extract letters and their associated weights
letters = list(letterProbabilities.keys())
weights = list(letterProbabilities.values())

# Assign letters to dice faces based on probability
dice = []
for _ in range(numDice):
    dieFaces = random.choices(letters, weights=weights, k=numFaces)  # Select k faces based on probability
    dice.append(dieFaces)

# Print the generated dice
for i, die in enumerate(dice):
    print(f"Die {i+1}: {die}")
