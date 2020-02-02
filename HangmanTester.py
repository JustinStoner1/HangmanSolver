from HangmanGame import HangmanGame
import OutFileEvaluator
import HangmanSolver


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

        guess = HangmanSolver.getGuess(heuristic, board, usedLetters, words)

        # Alternating heuristic usage
        '''
        if heuristicFlag:
            guess = HangmanSolver.getGuess("frequency", board, usedLetters, words)
        else:
            guess = HangmanSolver.getGuess("avgOccurrenceInWord", board, usedLetters, words)
        heuristicFlag = not heuristicFlag
        '''

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
            gameResult = testGame(word, words, heuristic)
            print(gameResult)
            outFile.write("\n" + str(gameNumber) + "," + gameResult[0] + "," + str(gameResult[1]) + "," + str(gameResult[2]) + "," + str(gameResult[3]) + "," + str(gameResult[4]) + "," + str(gameResult[5]))


def runTestsFrom(gameNumber, words, heuristic, outFileName):
    with open(outFileName, "a") as outFile:
        wordVals = words.values[gameNumber:]

        for word in wordVals:
            gameNumber += 1
            word = word[0]
            gameResult = testGame(word, words, heuristic)
            print(gameResult)
            outFile.write("\n" + str(gameNumber) + "," + gameResult[0] + "," + str(gameResult[1]) + "," + str(gameResult[2]) + "," + str(gameResult[3]) + "," + str(gameResult[4]) + "," + str(gameResult[5]))


def runDict(words, heuristic, outFileName):
    try:
        print("loading existing out file")
        with open(outFileName, "r") as outFile:
            # get the last line of the file, split it by , and grab the first element of the list
            gameNumber = int(outFile.readlines()[-1].split(',')[0])
    except(FileNotFoundError, ValueError):
        print("creating out file")
        with open(outFileName, "w") as outFile:
            outFile.write("gameNumber,word,wordLength,guessCount,correctGuessCount,incorrectGuessCount,usedLetters")
        gameNumber = 0
    # game numbers start at one, so game x uses word x - 1
    print("last word:", gameNumber, words.values[gameNumber-1])
    print("starting at:", gameNumber+1, words.values[gameNumber])

    with open(outFileName, "a") as outFile:
        wordVals = words.values[gameNumber:]

        for word in wordVals:
            gameNumber += 1
            word = word[0]
            gameResult = testGame(word, words, heuristic)
            print(gameResult)
            outFile.write("\n" + str(gameNumber) + ',' + gameResult[0] + ',' + str(gameResult[1]) + ',' + str(gameResult[2]) + ',' + str(gameResult[3]) + ',' + str(gameResult[4]) + ',' + str(gameResult[5]))


dictFrame = HangmanSolver.loadDictionary(r"dictionaries/Collins Scrabble Words (2019).txt")

# print(testGame("jazz", dictFrame, "positionsInWord"))
# HangmanSolver.runExample()
runDict(dictFrame, "occurrence", r"outFiles/occurrence_Collins Scrabble Words (2019).csv")
OutFileEvaluator.aggregateOutFileData(r"outFiles/occurrence_Collins Scrabble Words (2019).csv", r"aggFiles/aggData_occurrence_Collins Scrabble Words (2019).csv")
