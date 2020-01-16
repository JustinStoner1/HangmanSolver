import pandas
from HangmanGame import HangmanGame
import HangmanSolver

dict = HangmanSolver.loadDictionary(r"dictionaries/words_alpha.txt")
game = HangmanGame("calculation", 8)

while not game.complete:
    board = game.board
    usedLetters = game.usedLetters
    guess = HangmanSolver.getGuess("frequency", board, usedLetters, dict)
    print("guessing:", guess)
    if guess[1] != "":
        game.guessWord(guess[1])
    else:
        game.guessesLetter(guess[0])
