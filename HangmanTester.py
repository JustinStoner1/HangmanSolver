import pandas
from HangmanGame import HangmanGame
import HangmanSolver

words = HangmanSolver.loadDictionary(r"dictionaries/words_alpha.txt")
game = HangmanGame("calculation", 8)

guessCount = 0
while not game.complete:
    board = game.board
    usedLetters = game.usedLetters
    words = HangmanSolver.getPossibleWords(board, usedLetters, words)
    guess = HangmanSolver.getGuess("frequency", board, usedLetters, words)
    print("guessing:", guess)
    if guess[1] != "":
        game.guessWord(guess[1])
    else:
        game.guessesLetter(guess[0])
    guessCount += 1

print("took", guessCount, "guesses")
