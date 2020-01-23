import pandas
from HangmanGame import HangmanGame
import HangmanSolver
import csv


def testGame(word, words, heuristic):
    game = HangmanGame(word, 8)

    heuristicFlag = False

    guessCount = 0
    correctGuessCount = 0
    incorrectGuessCount = 0
    while not game.complete:
        board = game.board
        usedLetters = game.usedLetters
        words = HangmanSolver.getPossibleWords(board, usedLetters, words)
        # print("used letters:", usedLetters)

        guess = HangmanSolver.getGuess(heuristic, board, usedLetters, words)

        # print("guessing:", guess)
        if guess[1] != "":
            result = game.guessWord(guess[1])[3]
        else:
            result = game.guessLetter(guess[0])[3]

        if result:
            correctGuessCount += 1
        else:
            incorrectGuessCount += 1

        guessCount += 1

    return word, len(word), guessCount, correctGuessCount, incorrectGuessCount, game.usedLetters


def runTests(words, heuristic, outFileName):
    with open(outFileName, "w") as outFile:
        outFile.write("gameNumber,word,wordLength,guessCount,correctGuessCount,incorrectGuessCount,usedLetters")
    with open(outFileName, "a") as outFile:
        gameNumber = 0
        for word in words.values:
            gameNumber += 1
            word = word[0]
            print(word)
            gameResult = testGame(word, words, heuristic)
            outFile.write("\n" + str(gameNumber) + "," + gameResult[0] + "," + str(gameResult[1]) + "," + str(gameResult[2]) + "," + str(gameResult[3]) + "," + str(gameResult[4]) + "," + str(gameResult[5]))


def runTestsFrom(gameNumber, words, heuristic, outFileName):
    with open(outFileName, "a") as outFile:
        wordVals = words.values[gameNumber:]

        for word in wordVals:
            gameNumber += 1
            word = word[0]
            print(word)
            gameResult = testGame(word, words, heuristic)
            outFile.write("\n" + str(gameNumber) + "," + gameResult[0] + "," + str(gameResult[1]) + "," + str(gameResult[2]) + "," + str(gameResult[3]) + "," + str(gameResult[4]) + "," + str(gameResult[5]))


dict = HangmanSolver.loadDictionary(r"dictionaries/Collins Scrabble Words (2019).txt")

# runTests(dict, "frequency", r"outFiles/frequency_Collins Scrabble Words (2019).csv")
# runTestsFrom(254730, dict, "frequency", r"outFiles/frequency_Collins Scrabble Words (2019).csv")
# testGame("jazz", dict, "frequency")
HangmanSolver.runExample()
