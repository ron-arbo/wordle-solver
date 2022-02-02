from solver import solve

multiplierValues = [0, 0.05, 0.10, 0.15, 0.20]
finalList = []
noSolve = []

for val in multiplierValues:
    words = list(line.strip() for line in open('words.txt'))

    totalGuesses = 0
    didntSolve = 0
    for word in words:
        guessesTaken = solve(word, val)
        totalGuesses += guessesTaken
        if guessesTaken == 7:
            didntSolve += 1

    guessPerQ = totalGuesses / len(words)
    print("Guesses per Question: " + str(guessPerQ))
    print("Could not solve " + str(didntSolve) + " questions")
    finalList.append(guessPerQ)
    noSolve.append(didntSolve)

print("FinalList: ")
print(finalList)
print("Couldn't solve: ")
print(noSolve)