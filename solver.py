from audioop import mul
from enum import unique
from operator import truediv
from letterScore import letterScores


def filterByGreenLetter(words, puzzle):
    outputList = words.copy()
    ## Will hold (index, letter) of all green entries
    tupleList = []
    for i in range(0, 5):
        if puzzle[i][1] == 'green':
            ## Remove all words that do not have this tuple's letter in the same index
            tupleList.append((i, puzzle[i][0]))
    for word in words:
        for tuple in tupleList:
            if word[tuple[0]] != tuple[1]:
                outputList.remove(word)
                break
        
    return outputList

def filterByYellowLetter(words, puzzle):
    outputList = words.copy()
    tupleList = []
    for i in range(0, 5):
        if puzzle[i][1] == 'yellow':
            tupleList.append((i, puzzle[i][0]))
    for word in words:
        for tuple in tupleList:
            if (word[tuple[0]] == tuple[1]) or (tuple[1] not in word):
                outputList.remove(word)
                break
    return outputList


def filterByBlackLetter(words, puzzle):
    outputList = words.copy()
    blackListLetters = []
    for i in range(0, 5):
        if puzzle[i][1] == 'black':
            blackListLetters.append(puzzle[i][0])
    ## We should remove all words that contain blacklisted letters
    for word in words:
        for letter in word:
            if letter in blackListLetters:
                outputList.remove(word)
                break
    return outputList 


def updatePuzzle(guess, answer, puzzle):
    for i in range(0, 5):
        if guess[i] in answer:
            if guess[i] == answer[i]:
                puzzle[i] = (guess[i], 'green')
            else:
                puzzle[i] = (guess[i], 'yellow')
        else:
            puzzle[i] = (guess[i], 'black')

## Look at each letter in the word and give it a score based on how common
## the letters in the word are. Ignore duplicates (we should find a different way to address this
# than just ignoring right? Hurts words with duplicates too much)
def wordScore(word, multiplier):
    ## For now, use the frequencies listed in https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
    ## Other ideas: Overall word frequency, letters based on percent appearing in words (E is in 12.49 percent of words)
    ## https://www.wired.com/story/best-wordle-tips/
    score = 0
    lettersUsed = []
    for letter in word:
        if letter not in lettersUsed:
            lettersUsed.append(letter)
            ## Use the total relative word frequency, no duplicates
            score += letterScores[letter][1]
        else:
            score += (letterScores[letter][1] * multiplier)
    return score

def solve(answer, multiplier):
    ## Puzzle is represented by an array of tuples, where each tuple is {letter, green|yellow|black}. Index of the array will be index of the letter
    puzzle = [('', ''), ('', ''), ('', ''), ('', ''), ('', '')]
    words = list(line.strip() for line in open('words.txt'))
    # words = []
    # for word in words1:
    #     if len(word) == len(set(word)):
    #         words.append(word)
    numGuesses = 0
    
    while numGuesses < 7:
        ## We should first make guesses based on word/letter frequency (could make this little bit a function, don't want to redeclare variables each loop)
        maxWordScore = 0
        bestWord = ""
        for word in words:
            thisWordScore = wordScore(word, multiplier)
            if thisWordScore > maxWordScore:
                maxWordScore = thisWordScore
                bestWord = word

        currentGuess = bestWord
        print("Current Guess based on WordScore: " + currentGuess)
        numGuesses += 1

        print()
        print("----wordle-solver----")
        print("Current Guess: " + currentGuess)
        if currentGuess == answer:
            return numGuesses
            # exit("You win! It took " + str(numGuesses) + " guesses!")
        print()
        print("Running queries based on current info...")
        print()

        ## We have a guess right? Let's compare it to the answer!
        updatePuzzle(currentGuess, answer, puzzle)
        print(puzzle)
                
        ## Now that we have the updated puzzle and letter lists, let's filter down the list of words and make a guess!
        ## (This is where we'd start if applied pratically, since the site would update the puzzle for us)
        
        ## FINISH LATER: We can probably combine the three functions below
        ## Let's start by removing all of the words that do not match the green letters exactly
        words = filterByGreenLetter(words, puzzle)

        ## Now, remove the words that do not contain the yellow letters at all (this should be a sublist of the above)
        words = filterByYellowLetter(words, puzzle)
        
        ## Now, remove the words that DO contain letters that have been blacklisted
        words = filterByBlackLetter(words, puzzle)

    return 7

solve("those", 0.15)