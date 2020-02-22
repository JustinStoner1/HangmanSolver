import pandas


def loadDictionary(filePath: str) -> pandas.core.frame.DataFrame:
    """
    Loads a dictionary txt file where each line is assumed to be a word
    :param filePath: dictionary text file where each line is another word
    :return: a dataframe made from the dictionary file
    """
    with open(filePath) as word_file:  #
        lines = word_file.readlines()
        dictList = [line.rstrip('\n').lower() for line in lines]
        dictFrame = pandas.DataFrame(dictList)
        dictFrame.columns = ["words"]

    return pandas.DataFrame(dictFrame)


def getPossibleWords(board: str, usedLetters: str, dictionary: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    Uses regular expressions to select all rows of the dictionary dataframe that match the boards size and content
    :param board: the current state of the hangman game, used to find size and correct guesses
    :param usedLetters: list of letters that have been used already, both correct and incorrect
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: all possible words that could be the secret word bases on the correct and incorrect guesses and size of the secret word
    """
    regex = "(?=\\b\\w{"+str(len(board))+"}\\b)"

    if len(usedLetters) > 0:
        regex += "(?="
        for space in board:
            if space == "_":
                regex += "[^"+usedLetters+"]"
            else:
                regex += space
        regex += ")"

    return dictionary[dictionary.words.str.match(regex)]


def findPossibleLetters(words: pandas.core.frame.DataFrame, usedLetters: str) -> list:
    """
    Finds all remaining guessable letters based on the possible words minus letters that have already been used
    :param words: List of words to analyze
    :param usedLetters: list of letters that have been used already, both correct and incorrect
    :return: letters: list of remaining possible guesses
    """
    letters = []
    for word in words.values:
        word = word[0]
        for letter in word:
            if letter not in letters and letter not in usedLetters:
                letters.append(letter)

    return letters


def findLetterTotals(words: pandas.core.frame.DataFrame) -> (list, int):
    """
    Calculates the total number of times that letters appear in the dataframe of words given
    :param words: List of words to analyze
    :return: totals, letterCount: dictionary containing all observed letters and their occurrence frequency, total number of letters counted
    """
    totals = {}
    letterCount = 0
    for word in words.values:
        word = word[0]
        for letter in word:
            letterCount += 1
            if letter in totals:
                totals[letter] = totals[letter] + 1
            else:
                totals[letter] = 1

    return totals, letterCount


def rankPossibleGuessesByFrequency(board: str, usedLetters: str, possibleWords: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    Ranks the remaining possible letters (from the english alphabet) based on the frequency that they occur in the possible words
    :param board: the current state of the hangman game
    :param usedLetters: list of letters that have been used already, both correct and incorrect
    :param possibleWords: list of words the hangman word is believed to be from/in
    :return freqs: chance that each of the remaining un-guessed letters appear in the secret word
    """
    results = findLetterTotals(possibleWords)

    totals = results[0]
    letterCount = results[1]
    freqs = {}
    for k, v in totals.items():
        if k not in usedLetters:  # if letter is not already used, add it to possible moves
            freqs[k] = v
        else:  # letter has already been guessed, remove it from the options
            letterCount -= v  # remove occurrence count of used letters from the total count
    for k, v in freqs.items():
        freqs[k] = v / letterCount  # recalculate frequency

    return freqs


def rankPossibleGuessesByOccurrences(board: str, usedLetters: str, possibleWords: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    Ranks the remaining possible letters by number of words they appear in
    :param board: the current state of the hangman game
    :param usedLetters: list of letters that have been used already, both correct and incorrect
    :param possibleWords: list of words the hangman word is believed to be from/in
    :return: occurrences: number of times each letter was present in a possible word
    """
    letters = findPossibleLetters(possibleWords, usedLetters)
    '''
    occurrences = {}
    for letter in letters:
        count = 0
        for word in possibleWords.values:
            word = word[0]
            if letter in word:
                count += 1
        occurrences[letter] = count

    '''
    '''
    occurrences = {}
    for word in possibleWords.values:
        word = word[0]
        for letter in letters:
            if letter in word:
                if letter in occurrences:
                    occurrences[letter] = occurrences[letter] + 1
                else:
                    occurrences[letter] = 1
    '''
    occurrences = {}
    for word in possibleWords.values:
        word = word[0]
        seenLetters = ""  # list of characters already seen in the word so far
        for letter in word:
            if letter in letters and letter not in seenLetters:
                seenLetters += letter
                if letter in occurrences:
                    occurrences[letter] = occurrences[letter] + 1
                else:
                    occurrences[letter] = 1

    return occurrences


def rankPossibleGuessesByAbsence(board: str, usedLetters: str, possibleWords: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    Ranks the remaining possible letters by number of words they do not appear in
    :param board: the current state of the hangman game
    :param usedLetters: list of letters that have been used already, both correct and incorrect
    :param possibleWords: list of words the hangman word is believed to be from/in
    :return: occurrences: number of times each letter was not present in a possible word
    """
    letters = findPossibleLetters(possibleWords, usedLetters)

    absences = {}
    for letter in letters:
        count = 0
        for word in possibleWords.values:
            word = word[0]
            if letter not in word:
                count += 1
        absences[letter] = count

    return absences


def rankPossibleGuessesByAvgOccurrenceInWord(board: str, usedLetters: str, possibleWords: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    Ranks the remaining possible letters by the average number of times they appear on a word when they appear
    :param board: the current state of the hangman game
    :param usedLetters: list of letters that have been used already, both correct and incorrect
    :param possibleWords: list of words the hangman word is believed to be from/in
    :return: avgOccurrenceInWord: average number of times a letter appears in a word when it appears
    """
    possibleLetters = findPossibleLetters(possibleWords, usedLetters)

    letterCounts = findLetterTotals(possibleWords)[0]
    occurrences = rankPossibleGuessesByOccurrences(board, usedLetters, possibleWords)

    avgOccurrenceInWord = {}
    for letter in possibleLetters:
        avgOccurrenceInWord[letter] = letterCounts[letter]/occurrences[letter]

    return avgOccurrenceInWord


def rankPossibleGuessesByPositionsInWord(board: str, usedLetters: str, possibleWords: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    Ranks the remaining possible letters by the number of different positions they appear in
    :param board: the current state of the hangman game
    :param usedLetters: list of letters that have been used already, both correct and incorrect
    :param possibleWords: list of words the hangman word is believed to be from/in
    :return: occurrenceInWord: number of different positions a word appears in
    """
    positions = len(board)
    oneHotEncodings = {}
    for word in possibleWords.values:
        position = 0
        word = word[0]
        for letter in word:
            if letter in usedLetters:
                continue
            if letter in oneHotEncodings:
                oneHotEncodings[letter][position] = oneHotEncodings[letter][position] + 1
            else:
                oneHotEncodings[letter] = [0 for i in range(0, positions)]
                oneHotEncodings[letter][position] = oneHotEncodings[letter][position] + 1
            position += 1
    ranks = {}
    for k, v in oneHotEncodings.items():
        # ranks[k] = len([c for c in v if c > 0])/len(possibleWords.values)
        ranks[k] = sum([c/len(possibleWords.values) for c in v if c > 0])*len([c for c in v if c > 0])/len(possibleWords.values)

    return ranks


def getGuess(heuristic: str, board: str, usedLetters: str, dictionary: pandas.core.frame.DataFrame) -> (str, str):
    """
    Retrieves a guess based on the heuristic, current board, used letters, and dictionary
    :param heuristic: the name of the heuristic to use
    :param board: the current state of the hangman game
    :param usedLetters: list of letters that have been used already, both correct and incorrect
    :param dictionary: dictionary dataframe assumed to contain the secret word
    :return: letter, word: the best letter to guess based on the given heuristic, the last remaining word if only one is left, otherwise an empty string
    """
    if heuristic == "frequency":
        letterRanks = rankPossibleGuessesByFrequency(board, usedLetters, dictionary)
    elif heuristic == "occurrence":
        letterRanks = rankPossibleGuessesByOccurrences(board, usedLetters, dictionary)
    elif heuristic == "absence":
        letterRanks = rankPossibleGuessesByAbsence(board, usedLetters, dictionary)
    elif heuristic == "avgOccurrenceInWord":
        letterRanks = rankPossibleGuessesByAvgOccurrenceInWord(board, usedLetters, dictionary)
    elif heuristic == "positionsInWord":
        letterRanks = rankPossibleGuessesByPositionsInWord(board, usedLetters, dictionary)
    else:
        print("Heuristics are:")
        print("frequency")
        print("occurrence")
        print("absence")
        print("avgOccurrenceInWord")
        print("positionsInWord")
        letterRanks = rankPossibleGuessesByFrequency(board, usedLetters, dictionary)
    v = list(letterRanks.values())
    k = list(letterRanks.keys())

    possibleWords = getPossibleWords(board, usedLetters, dictionary)
    if possibleWords.size == 1:  # can guess word
        word = possibleWords.words.iloc[0]
    else:
        word = ""

    return k[v.index(max(v))], word


def runExample():
    #dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/testDict.txt"))
    #dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/words_alpha.txt"))
    dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/Collins Scrabble Words (2019).txt"))

    print("loaded", len(dictionary2), "words\n")

    #print("word: zwitterionic")
    #testBoard = "u___u__"
    print("word:  zwitterionic")
    testBoard =  "__i____i__i_"
    #used:     pp
    guesses = "i"
    print("board:", testBoard)
    print("guesses:", guesses)

    alg = getPossibleWords(testBoard, guesses, dictionary2)
    print(alg)
    possibilities = len(alg)
    print(possibilities, "w/ incorrect guesses:")

    #print(findPossibleLetters(alg, guesses))

    letterRanks1 = rankPossibleGuessesByFrequency(testBoard, guesses, alg)

    v = list(letterRanks1.values())
    k = list(letterRanks1.keys())
    heuristic1 = k[v.index(max(v))]
    print("Frequency says:", heuristic1)

    heuristic1 = k[v.index(min(v))]
    print("FrequencyB says:", heuristic1)
    print(letterRanks1)

    letterRanks2 = rankPossibleGuessesByOccurrences(testBoard, guesses, alg)
    v = list(letterRanks2.values())
    k = list(letterRanks2.keys())
    heuristic2 = k[v.index(max(v))]
    print("Occurrence says:", heuristic2)

    heuristic2 = k[v.index(min(v))]
    print("OccurrenceB says:", heuristic2)
    print(letterRanks2)

    letterRanks3 = rankPossibleGuessesByAbsence(testBoard, guesses, alg)
    v = list(letterRanks3.values())
    k = list(letterRanks3.keys())
    heuristic3 = k[v.index(max(v))]
    print("Absence says:", heuristic3)

    heuristic3 = k[v.index(min(v))]
    print("AbsenceB says:", heuristic3)
    print(letterRanks3)

    letterRanks4 = rankPossibleGuessesByAvgOccurrenceInWord(testBoard, guesses, alg)
    v = list(letterRanks4.values())
    k = list(letterRanks4.keys())
    heuristic4 = k[v.index(max(v))]
    print("AvgOccurrenceInWord says:", heuristic4)

    heuristic4 = k[v.index(min(v))]
    print("AvgOccurrenceInWordB says:", heuristic4)
    print(letterRanks4)

    letterRanks5 = rankPossibleGuessesByPositionsInWord(testBoard, guesses, alg)
    v = list(letterRanks5.values())
    k = list(letterRanks5.keys())
    heuristic5 = k[v.index(max(v))]
    print("PositionsInWord says:", heuristic5)

    heuristic5 = k[v.index(min(v))]
    print("PositionsInWord says:", heuristic5)
    print(letterRanks5)

