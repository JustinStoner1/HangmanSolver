import pandas


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


def getPossibleWordsFromBoard(board, dictionary):
    """
    Uses regular expressions to select all rows of the dictionary dataframe that match the boards size and content
    :param board: the current state of the hangman game, used to find size and correct guesses
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: all possible words that could be the secret word bases on the correct guesses and size of the secret word
    """

    # Match words to correct guesses and secret word size
    regex = "(?="+board.replace('_', '.')+")(?=\\b\\w{"+str(len(board))+"}\\b)"

    return dictionary[dictionary.words.str.match(regex)]


def getPossibleWordsFromGame(board, incorrectGuesses, dictionary):
    """
    Uses regular expressions to select all rows of the dictionary dataframe that match the boards size and content
    :param board: the current state of the hangman game, used to find size and correct guesses
    :param incorrectGuesses: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: all possible words that could be the secret word bases on the correct and incorrect guesses and size of the secret word
    """

    # match words to correct guesses and secret word size
    regex = "(?="+board.replace('_', '.')+")(?=\\b\\w{"+str(len(board))+"}\\b)"

    if len(incorrectGuesses) > 0:
        # ensure words do not contain previous incorrect guesses
        regex += "(?=^[^"
        for guess in incorrectGuesses:
            regex += guess
        regex += "]*$)"

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

    possibleWords = getPossibleWordsFromGame(board, incorrectGuesses, dictionary)
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


def rankPossibleGuessesByOccurrenceCount(board, incorrectGuesses, dictionary):
    """
    Ranks the remaining possible letters by number of words they appear in
    :param board: the current state of the hangman game
    :param incorrectGuesses: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: eliminations: number of times each letter was present in a possible word
    """
    usedLetters = incorrectGuesses+[letter for letter in board if letter != "_"]

    possibleWords = getPossibleWordsFromGame(board, incorrectGuesses, dictionary)

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
dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/words_alpha.txt"))

print("loaded", len(dictionary2), "words")

print("word:  zwitterionic")
testBoard =  "__i____i__i_"
badGuesses = []
print("board:", testBoard)
print("bad guesses:", badGuesses)

alg1 = getPossibleWordsFromBoard(testBoard, dictionary2)
possibilities1 = len(alg1)
print(possibilities1, "w/out incorrect guesses:")

alg2 = getPossibleWordsFromGame(testBoard, badGuesses, dictionary2)
possibilities2 = len(alg2)
print(possibilities2, "w/ incorrect guesses:")

print(possibilities1-possibilities2, "fewer possibilities")

letterFreqs = findLetterTotals(alg2)
#print("letter freqs:", letterFreqs)

letterRanks1 = rankPossibleGuessesByFrequency(testBoard, badGuesses, dictionary2)
#print("letter ranks:", letterRanks)

v = list(letterRanks1.values())
k = list(letterRanks1.keys())
heuristic1 = k[v.index(max(v))]
print("heuristic1 says:", heuristic1)

letterRanks2 = rankPossibleGuessesByOccurrenceCount(testBoard, badGuesses, dictionary2)
v = list(letterRanks2.values())
k = list(letterRanks2.keys())
heuristic2 = k[v.index(max(v))]
print("heuristic2 says:", heuristic2)
