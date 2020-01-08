import os
import pandas


def loadDictionary(filePath):
    """

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
    regex = "(?="+board.replace('_', '.')+")(?=\\b\\w{"+str(len(board))+"}\\b)"  # Match words to correct guesses and secret word size
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

    # ensure words do not contain previous incorrect guesses
    regex += "(?=^[^"
    for guess in incorrectGuesses:
        regex += guess
    regex += "]*$)"

    return dictionary[dictionary.words.str.match(regex)]


def rankPossibleGuesses(board, incorrectGuesses, dictionary):
    """
    WIP: this function will rank the remaining possible letters (from the english alphabet) based on the frequency that they occur in the possible words
    :param board: the current state of the hangman game
    :param incorrectGuesses: guessed letters that were wrong
    :param dictionary: the dictionary the hangman word is believed to be from
    """
    print("wip")


# process arguments
dictionary2 = pandas.DataFrame(loadDictionary(r"dictionaries/words_alpha.txt"))
#print(dictionary2)
print("loaded", len(dictionary2), "words")

print("word: zwitterionic")
testBoard = "z___________"
badGuesses = ['b', 'f', 'h', 'p', 'g']
print("board:", testBoard)
print("bad guesses:", badGuesses)


heuristic1 = getPossibleWordsFromBoard(testBoard, dictionary2)
possibilities1 = len(heuristic1)
print(possibilities1, "w/out incorrect guesses:")

heuristic2 = getPossibleWordsFromGame(testBoard, badGuesses, dictionary2)
possibilities2 = len(heuristic2)
print(possibilities2, "w/ incorrect guesses:")

print(possibilities1-possibilities2, "fewer possibilities")
