class HangmanGame:
    def __init__(self, secretWord, wrongGuessLimit):
        self.secretWord = secretWord
        self.wrongGuessLimit = wrongGuessLimit
        self.board = "_"*len(secretWord)
        self.usedLetters = ""
        self.remainingGuesses = wrongGuessLimit
        self.complete = False

        #print("Secret word:", secretWord)
        #print(wrongGuessLimit, "wrong guesses allowed")
        #print("board:", self.board)

    def guessLetter(self, letter):
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

    def guessWord(self, word):
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
