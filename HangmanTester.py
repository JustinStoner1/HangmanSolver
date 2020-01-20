import pandas
from HangmanGame import HangmanGame
import HangmanSolver


def testGame(word, words):
    game = HangmanGame(word, 8)

    heuristicFlag = False

    guessCount = 0
    while not game.complete:
        board = game.board
        usedLetters = game.usedLetters
        words = HangmanSolver.getPossibleWords(board, usedLetters, words)
        print("used letters:", usedLetters)

        if heuristicFlag:
            guess = HangmanSolver.getGuess("avgOccurrenceInWord", board, usedLetters, words)
        else:
            guess = HangmanSolver.getGuess("frequency", board, usedLetters, words)

        print("guessing:", guess)
        if guess[1] != "":
            game.guessWord(guess[1])
        else:
            game.guessesLetter(guess[0])

        guessCount += 1
        heuristicFlag = not heuristicFlag

    print("took", guessCount, "guesses")


def runTests():
    words = HangmanSolver.loadDictionary(r"dictionaries/words_alpha.txt")
    for word in words.values:
        word = word[0]
        testGame(word, words)

runTests()
#HangmanSolver.runExample()
