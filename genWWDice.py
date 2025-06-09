import random

def gen_w_w_dice(num_dice, num_faces):
    letter_probabilities = {  #Define exact probability percentages (sum should be ~100%)
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

    #Extract letters and their associated weights
    letters = list(letter_probabilities.keys())
    weights = list(letter_probabilities.values())

    #Assign letters to dice faces based on probability
    dice = []

    for _ in range(num_dice):
        die_faces = random.choices(letters, weights=weights, k=num_faces)  #Select k faces based on probability
        dice.append(die_faces)

    return dice
