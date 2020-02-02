class HangmanGame:
    def __init__(self, secretWord: str, wrongGuessLimit: int) -> object:
        """
        Make a game of hangman with the given word string and a guess limi
        :param secretWord: the word that must be guessed
        :param wrongGuessLimit: the maximum number of wrong guess (game does not end when this reaches zero)
        """
        self.secretWord = secretWord
        self.wrongGuessLimit = wrongGuessLimit
        self.board = "_"*len(secretWord)
        self.usedLetters = ""
        self.remainingGuesses = wrongGuessLimit
        self.complete = False

        #print("Secret word:", secretWord)
        #print(wrongGuessLimit, "wrong guesses allowed")
        #print("board:", self.board)

    def guessLetter(self, letter: str) -> (str, str, int, bool):
        """
        Guess the provided letter, wrong guesses will be subtracted from the remaining guesses, correct guess will be added to the board where appropriate
        :param letter: letter to be guessed
        :return: a quadruple containing: the updated board, a string containing all used letters, the number of remaining guesses, a flag that is true if the guess was correct, otherwise false
        """
        correctFlag = False
        self.usedLetters += letter
        if letter in self.secretWord:
            for i in range(0, len(self.secretWord)):
                if letter == self.secretWord[i]:
                    self.board = self.board[:i] + letter + self.board[i + 1:]
            correctFlag = True
        else:
            self.remainingGuesses -= 1
            # correctFlag = False
            # print(letter, "is not in the secret word")

        if "_" not in self.board:
            self.complete = True
            # print("you win")

        # print("board:", self.board)
        # print(self.remainingGuesses, "guesses remaining")
        return self.board, self.usedLetters, self.remainingGuesses, correctFlag

    def guessWord(self, word: str) -> (str, str, int, bool):
        """
        Guess word is like guess letter, except whole words can be guessed. Wrong guesses still cost one guess. Correctly guessing the word ends the game and completes the board
        :param word: the suspected secret word
        :return: a quadruple containing: the updated board, a string containing all used letters, the number of remaining guesses, a flag that is true if the guess was correct, otherwise false
        """
        if word == self.secretWord:
            # print("correct")
            self.board = word
            self.complete = True
            # print("board:", self.board)
            # print("you win")
            return self.board, self.usedLetters, self.remainingGuesses, True
        else:
            self.remainingGuesses -= 1
            return self.board, self.usedLetters, self.remainingGuesses, False
            # print("incorrect")
