import pandas
import time

def loadDictionary(filePath):
    """
    Loads a dictionary txt file where each line is assumed to be a word
    :param filePath: dictionary text file where each line is another word
    :return: a dataframe made from the dictionary file
    """

    with open(filePath) as word_file:  #
        lines = word_file.readlines()
        dictList = [line.rstrip('\n') for line in lines]
        dictFrame = pandas.DataFrame(dictList)
        dictFrame.columns = ["words"]
    return dictFrame


def getPossibleWords(board, incorrectGuesses, dictionary):
    """
    Uses regular expressions to select all rows of the dictionary dataframe that match the boards size and content
    :param board: the current state of the hangman game, used to find size and correct guesses
    :param incorrectGuesses: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: all possible words that could be the secret word bases on the correct and incorrect guesses and size of the secret word
    """

    usedLetters = ""
    for element in incorrectGuesses+[letter for letter in board if letter != "_"]:
        usedLetters += str(element)

    # match words to correct guesses and secret word size
    regex = "(?="
    for space in board:
        if space == "_":
            regex += "[^"+usedLetters+"]"
        else:
            regex += space

    regex += ")(?=\\b\\w{"+str(len(board))+"}\\b)"

    return dictionary[dictionary.words.str.match(regex)]


def findLetterTotals(words):
    """
    Calculates the total number of times that letters appear in the dataframe of words given
    :param words: List of words to analyze
    :return: dictionary containing all observed letters and their occurrence frequency
    """

    freqs = {}
    letterCount = 0
    for word in words.values:
        word = word[0]
        for letter in word:
            letterCount += 1
            if letter in freqs:
                freqs[letter] = freqs[letter] + 1
            else:
                freqs[letter] = 1
    return freqs, letterCount


def rankPossibleGuessesByFrequency(board, incorrectGuesses, dictionary):
    """
    Ranks the remaining possible letters (from the english alphabet) based on the frequency that they occur in the possible words
    :param board: the current state of the hangman game
    :param incorrectGuesses: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return freqs: chance that each of the remaining un-guessed letters appear in the secret word
    """

    usedLetters = incorrectGuesses+[letter for letter in board if letter != "_"]

    possibleWords = getPossibleWords(board, incorrectGuesses, dictionary)
    results = findLetterTotals(possibleWords)

    totals = results[0]
    letterCount = results[1]
    freqs = {}
    for k, v in totals.items():
        occurrences = v  # re-find occurrence count of the letter
        if k not in usedLetters:  # if letter is not already used, add it to possible moves
            freqs[k] = occurrences
        else:  # letter has already been guessed, remove it from the options
            letterCount -= occurrences  # remove occurrence count of used letters from the total count
    for k, v in freqs.items():
        freqs[k] = v / letterCount  # recalculate frequency
    return freqs


def rankPossibleGuessesByOccurrences(board, incorrectGuesses, dictionary):
    """
    Ranks the remaining possible letters by number of words they appear in
    :param board: the current state of the hangman game
    :param incorrectGuesses: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: occurrences: number of times each letter was present in a possible word
    """
    usedLetters = incorrectGuesses+[letter for letter in board if letter != "_"]

    possibleWords = getPossibleWords(board, incorrectGuesses, dictionary)

    letters = []
    for word in possibleWords.values:
        word = word[0]
        for letter in word:
            if letter not in letters and letter not in usedLetters:
                letters.append(letter)

    occurrences = {}
    for letter in letters:
        count = 0
        for word in possibleWords.values:
            word = word[0]
            if letter in word:
                count += 1
        occurrences[letter] = count

    return occurrences


def rankPossibleGuessesByEliminations(board, incorrectGuesses, dictionary):
    """
    Ranks the remaining possible letters by number of words they appear in
    :param board: the current state of the hangman game
    :param incorrectGuesses: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: occurrences: number of times each letter was present in a possible word
    """
    usedLetters = incorrectGuesses+[letter for letter in board if letter != "_"]

    possibleWords = getPossibleWords(board, incorrectGuesses, dictionary)

    letters = []
    for word in possibleWords.values:
        word = word[0]
        for letter in word:
            if letter not in letters and letter not in usedLetters:
                letters.append(letter)

    eliminations = {}
    for letter in letters:
        count = 0
        for word in possibleWords.values:
            word = word[0]
            if letter in word:
                count += 1
        eliminations[letter] = count

    return eliminations


# process arguments
#dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/testDict.txt"))
dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/words_alpha.txt"))

print("loaded", len(dictionary2), "words")

#print("word:  zwitterionic")
#testBoard =  "__i____i__i_"
print("word:  cats")
testBoard =  "____"
badGuesses = ['f']
print("board:", testBoard)
print("bad guesses:", badGuesses)

alg = getPossibleWords(testBoard, badGuesses, dictionary2)
possibilities = len(alg)
print(possibilities, "w/ incorrect guesses:")

letterRanks1 = rankPossibleGuessesByFrequency(testBoard, badGuesses, dictionary2)

v = list(letterRanks1.values())
k = list(letterRanks1.keys())
heuristic1 = k[v.index(max(v))]
print("heuristic1 says:", heuristic1)

v = list(letterRanks1.values())
k = list(letterRanks1.keys())
heuristic1 = k[v.index(min(v))]
print("heuristic1b says:", heuristic1)

letterRanks2 = rankPossibleGuessesByOccurrences(testBoard, badGuesses, dictionary2)
v = list(letterRanks2.values())
k = list(letterRanks2.keys())
heuristic2 = k[v.index(max(v))]
print("heuristic2 says:", heuristic2)

v = list(letterRanks2.values())
k = list(letterRanks2.keys())
heuristic2 = k[v.index(min(v))]
print("heuristic2b says:", heuristic2)
