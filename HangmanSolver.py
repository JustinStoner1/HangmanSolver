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


def possibleWords(board, dictionary):
    """
    Uses regular expressions to select all rows of the dictionary dataframe that match the boards size and content
    :param board: the current state of the hangman game
    :param dictionary: the dictionary the hangman word is believed to be from
    :return: all possible words that could be the secret word bases on the correct guesses and size of the secret word
    """
    regex = board.replace('_', '.')
    regex = "\\b\\w{"+str(len(board))+"}\\b"
    regex = "(?="+board.replace('_', '.')+")(?=\\b\\w{"+str(len(board))+"}\\b)"
    print("regex: "+regex)
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
print(dictionary2)

print("zwitterionic")
testBoard = "z___________"
print(testBoard)
maybies = possibleWords(testBoard, dictionary2)
print(maybies)

