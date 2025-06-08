import random
import math
import genWWDice
from createWWBoard import create_board

#def whirlWords():
"""
Play a word game with customizable grid sizes
"""

#Load English dictionary
with open(r"C:\Users\ynaev\Documents\Liz's Python Data\wordslist.txt") as f:
    dictionary = set(word.strip().lower() for word in f)

numDice = int(input("How many dice would you like to compete against?  "))
nearestPerfectSquare = (math.ceil(math.sqrt(numDice)) **2)  #Find the nearest perfect square
if nearestPerfectSquare != numDice:
    numDice = nearestPerfectSquare  #Reset numDice to updated value
    print(f"I've rounded the dice up to the nearest perfect square to create a nice grid of {int(math.sqrt(nearestPerfectSquare))} x {int(math.sqrt(nearestPerfectSquare))}")

"""
Example Adjustments:
User enters 6 → Adjusts to 9 (since sqrt(6) ≈ 2.45, rounds to 3, t
hen 3² = 9).
User enters 15 → Adjusts to 16 (sqrt(15) ≈ 3.87, rounds to 4, then 4² = 16).
User enters 20 → Adjusts to 25 (sqrt(20) ≈ 4.47, rounds to 5, then 5² = 25).
User enters 25 → Remains at 25.
"""
numFaces = int(input("How many faces would you like each die to have?  "))
dice = genWWDice.genWWDice(numDice, numFaces)  #Call the function and unpack the returned values.
gridSize = math.isqrt(numDice)  #Finds the square root of the number of dice, ensuring a square grid size.
chosenLetters = [random.choice(die).lower() for die in dice]  #Randomly choose one face from each die
wWGrid = [chosenLetters[i:i+gridSize] for i in range(0, len(chosenLetters), gridSize)]  #Arrange the letters into a grid

print("Can you find all the words hidden in this grid?  You've got 30 seconds.  Type 'end game' to stop.\nGo!\n")

#=================================================================================================
# Directions for moving in 8 directions (dx, dy)
directions = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

#=================================================================================================
def find_words(x, y, path, visited, word, words_found, dictionary):
    if word in dictionary and len(word) > 2:
        words_found.add(word)

    if len(word) > 10:  # You can adjust this limit if needed
        return

    rows, cols = len(wWGrid), len(wWGrid[0])

    # Explore neighbors
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
            find_words(nx, ny,
                       path + [(nx, ny)],
                       visited | {(nx, ny)},
                       word + wWGrid[nx][ny],
                       words_found, dictionary)

#=================================================================================================
#Search the board and store words into the dictionary.
def boggle_solver(wWGrid, dictionary):
    words_found = set()  #Introduce the words list
    rows, cols = len(wWGrid), len(wWGrid[0])
    for i in range(rows):
        for j in range(cols):
            find_words(i, j, [(i, j)], {(i, j)}, wWGrid[i][j], words_found, dictionary)  #Call to function find_words
    return words_found

#=================================================================================================
create_board(wWGrid)  #Call the function to display the board
found_words = boggle_solver(wWGrid, dictionary) #Create master word list for current game grid
print(found_words)

#Determine max length of word possible.

#Create a dictionary to store words of each possible length, minimum of 3.

#Count the total number of valid words hidden in the current game grid
#totalPossibleWords =  len.wWMasterList

"""
timerDuration = 30  #Set the duration for the timer in seconds
startTime = time.time()  # Store the start time
userWords = [] #Create a list for user's entries

# Prompt the user for input until the timer runs out
while True:
    elapsedTime = time.time() - startTime  #Track the elapsed time    
    if elapsedTime > timerDuration:
        print("Time's up!")
        break  #Exit the loop when time is up    
    userWord = input()  #Ask the user to input a word
    if len(userWord) < 3:
        print('Words must be at least 3 letters long.')
        input()
    if userWord in userWords:
        print("You've already found that one, keep looking!")
        input()
    if userWord == 'end game':
        break  #Exit game at the request of the user
    userWords.append(userWord)  #Add the word to the user's list

#Separate words into valid and invalid lists
validWords = [word for word in userWords if word in dictionary] 
invalidWords = [word for word in userWords if word not in dictionary]
      
#Display breakdown of user's words
print("Valid words:")
for word in validWords:
      print(word)
print("\nInvalid words")
for word in invalidWords:
      print(word)

def scoreWord(word):
    length = len(word)
    if length <= 4:
        return 1
    elif length == 5:
        return 2
    elif length == 6:
        return 3
    elif length == 7:
        return 5
    elif length > 7:
        return 11

userScore = sum(scoreWord(word) for word in validWords)  #Calculate user's score
#possibleScore = sum(scoreWord(word) for word in wWMasterList)  #Calculate possible score

print(f"You've scored {userScore}")
#, which calculates to {userScore}/{possibleScore}: .2%")
"""
