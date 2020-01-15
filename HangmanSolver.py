import math

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


def getPossibleWords(board, usedLetters, dictionary):
    """
    Uses regular expressions to select all rows of the dictionary dataframe that match the boards size and content
    :param board: the current state of the hangman game, used to find size and correct guesses
    :param incorrectGuesses: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: all possible words that could be the secret word bases on the correct and incorrect guesses and size of the secret word
    """
    # match words to correct guesses and secret word size
    regex = "(?=\\b\\w{"+str(len(board))+"}\\b)"

    if len(usedLetters) > 0:
        regex += "(?="
        for space in board:
            if space == "_":
                regex += "[^"+usedLetters+"]"
            else:
                regex += space
        regex += ")"

    print(regex)

    return dictionary[dictionary.words.str.match(regex)]


def findPossibleLetters(words, usedLetters):
    letters = []
    for word in words.values:
        word = word[0]
        for letter in word:
            if letter not in letters and letter not in usedLetters:
                letters.append(letter)

    return letters


def findLetterTotals(words):
    """
    Calculates the total number of times that letters appear in the dataframe of words given
    :param words: List of words to analyze
    :return: dictionary containing all observed letters and their occurrence frequency
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


def rankPossibleGuessesByFrequency(board, usedLetters, dictionary):
    """
    Ranks the remaining possible letters (from the english alphabet) based on the frequency that they occur in the possible words
    :param board: the current state of the hangman game
    :param usedLetters: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return freqs: chance that each of the remaining un-guessed letters appear in the secret word
    """
    possibleWords = getPossibleWords(board, usedLetters, dictionary)
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


def rankPossibleGuessesByOccurrences(board, usedLetters, dictionary):
    """
    Ranks the remaining possible letters by number of words they appear in
    :param board: the current state of the hangman game
    :param usedLetters: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: occurrences: number of times each letter was present in a possible word
    """
    possibleWords = getPossibleWords(board, usedLetters, dictionary)
    letters = findPossibleLetters(possibleWords, usedLetters)

    occurrences = {}
    for letter in letters:
        count = 0
        for word in possibleWords.values:
            word = word[0]
            if letter in word:
                count += 1
        occurrences[letter] = count

    return occurrences


def rankPossibleGuessesByAbsence(board, usedLetters, dictionary):
    """
    Ranks the remaining possible letters by number of words they do not appear in
    :param board: the current state of the hangman game
    :param usedLetters: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: occurrences: number of times each letter was not present in a possible word
    """
    possibleWords = getPossibleWords(board, usedLetters, dictionary)
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


def rankPossibleGuessesByEliminations(board, usedLetters, dictionary):
    """
    Ranks the remaining possible letters by number of words they appear in
    :param board: the current state of the hangman game
    :param usedLetters: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: occurrences: number of times each letter was present in a possible word
    """
    possibleWords = getPossibleWords(board, usedLetters, dictionary)
    letters = findPossibleLetters(possibleWords, usedLetters)

    eliminations = {}
    for letter in letters:
        count = 0
        for word in possibleWords.values:
            word = word[0]
            if letter in word:
                count += 1
        eliminations[letter] = count

    return eliminations


def rankPossibleGuessesByAvgOccurrenceInWord(board, usedLetters, dictionary):
    """
    Ranks the remaining possible letters by the average number of times they appear on a word when they appear
    :param board: the current state of the hangman game
    :param usedLetters: list of guesses letters that are not in the secret word
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: occurrenceInWord:
    """
    possibleWords = getPossibleWords(board, usedLetters, dictionary)
    possibleLetters = findPossibleLetters(possibleWords, usedLetters)

    letterCounts = findLetterTotals(possibleWords)[0]
    occurrences = rankPossibleGuessesByOccurrences(board, usedLetters, dictionary)

    occurrenceInWord = {}
    for letter in possibleLetters:
        occurrenceInWord[letter] = letterCounts[letter]/occurrences[letter]
    return occurrenceInWord


def runExample():
    # dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/testDict.txt"))
    dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/words_alpha.txt"))

    print("loaded", len(dictionary2), "words")

    #print("word: zwitterionic")
    #testBoard = "u___u__"
    print("word:  jazz")
    testBoard =  "___"
    guesses = ""
    print("board:", testBoard)
    print("bad guesses:", guesses)

    alg = getPossibleWords(testBoard, guesses, dictionary2)
    print(alg)
    possibilities = len(alg)
    print(possibilities, "w/ incorrect guesses:")

    print(findPossibleLetters(alg, guesses))

    letterRanks1 = rankPossibleGuessesByFrequency(testBoard, guesses, dictionary2)

    v = list(letterRanks1.values())
    k = list(letterRanks1.keys())
    heuristic1 = k[v.index(max(v))]
    print("Frequency says:", heuristic1)

    heuristic1 = k[v.index(min(v))]
    print("FrequencyB says:", heuristic1)

    letterRanks2 = rankPossibleGuessesByOccurrences(testBoard, guesses, dictionary2)
    v = list(letterRanks2.values())
    k = list(letterRanks2.keys())
    heuristic2 = k[v.index(max(v))]
    print("Occurrence says:", heuristic2)

    heuristic2 = k[v.index(min(v))]
    print("OccurrenceB says:", heuristic2)

    letterRanks3 = rankPossibleGuessesByAbsence(testBoard, guesses, dictionary2)
    v = list(letterRanks3.values())
    k = list(letterRanks3.keys())
    heuristic3 = k[v.index(max(v))]
    print("Absence says:", heuristic3)

    heuristic3 = k[v.index(min(v))]
    print("AbsenceB says:", heuristic3)

    letterRanks4 = rankPossibleGuessesByAvgOccurrenceInWord(testBoard, guesses, dictionary2)
    v = list(letterRanks4.values())
    k = list(letterRanks4.keys())
    heuristic4 = k[v.index(max(v))]
    print("OccurrenceInWord says:", heuristic4)

    heuristic4 = k[v.index(min(v))]
    print("OccurrenceInWordB says:", heuristic4)

    possibleLetters = findPossibleLetters(alg, guesses)
    print(possibleLetters)

    wordCount = len(alg)
    for letter in possibleLetters:
        frequency = letterRanks1[letter]
        avgOccInWrd = letterRanks4[letter]
        value = frequency*avgOccInWrd

        print(letter, "->", frequency, "*", avgOccInWrd, "=", value)


runExample()
