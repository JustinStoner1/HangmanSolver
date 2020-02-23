import pandas
from HangmanGame import HangmanGame
import OutFileEvaluator
import HangmanSolver
from multiprocessing import Pool


def testGame(word: str, words: pandas.core.frame.DataFrame, heuristic: str) -> (str, int, int, int, int, str):
    """
    Runs a game of hangman with the provided settings and returns the details
    :param word: the secret word
    :param words: the dictionary the secret is (believed) to be from
    :param heuristic: the strategy the function will use to make guesses
    :return: (the secret word, the length of the secret word, the total number of guesses used, the total number of correct guesses, the total number of incorrect guesses, the letters guesses in the order they were guessed)
    """
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
        # print(guess)

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


def makeDictFromDict(words):
    print("WIP")
    results = HangmanSolver.findLetterTotals(words)

    totals = results[0]
    letterCount = results[1]
    freqs = {}
    for k, v in totals.items():
        occurrences = v  # re-find occurrence count of the letter
        freqs[k] = occurrences
    for k, v in freqs.items():
        freqs[k] = v / letterCount  # recalculate frequency
    print(freqs)
    sum = 0
    for v in freqs.values():
        sum += v
    print(sum)


def runTestsOnDict(words: pandas.core.frame.DataFrame, heuristic: str, outFileName: str):
    """
    Runs the "testGame" function on every word in the dictionary. If the file already exists, it will pick up where it left off
    :param words: the dictionary the secret is (believed) to be from
    :param heuristic: the strategy the function will use to make guesses
    :param outFileName: name of the file that the program should append results to
    """
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


def runTestsOnSectionOfDict(words: pandas.core.frame.DataFrame, heuristic: str, outFileName: str, start: int, finish: int) -> str:
    """
    Runs the "testGame" function on every word in the range provided. The words are indexed in the order they appear in the dictionary. If the file already exists, it will pick up where it left off.
    :param words: the dictionary the secret is (believed) to be from
    :param heuristic: the strategy the function will use to make guesses
    :param outFileName: name of the file that the program should append results to
    :param start: the index of the beginning of the range; includes this word
    :param finish: the index of the end of the range; this word will not be included
    :return: the completed game details each in its own line
    """
    try:
        print("loading existing out file")
        with open(outFileName, "r") as outFile:
            # get the last line of the file, split it by , and grab the first element of the list
            gameNumber = int(outFile.readlines()[-1].split(',')[0])
            print("last word tested was:", gameNumber, words.values[gameNumber-1])
    except(FileNotFoundError, ValueError):
        print("creating out file")
        with open(outFileName, "w") as outFile:
            outFile.write("gameNumber,word,wordLength,guessCount,correctGuessCount,incorrectGuessCount,usedLetters")
        #gameNumber = 0
    gameNumber = start
    # game numbers start at one, so game x uses word x - 1
    print("last word:", start, words.values[start-1])
    print("starting at:", start+1, words.values[start])
    print("stopping at:", finish, words.values[finish-1])

    tests = ""
    with open(outFileName, "a") as outFile:
        wordVals = words.values[gameNumber:]

        for word in wordVals:
            gameNumber += 1
            if gameNumber >= finish:
                break
            word = word[0]
            gameResult = testGame(word, words, heuristic)
            print(gameResult)
            tests += "\n" + str(gameNumber) + ',' + gameResult[0] + ',' + str(gameResult[1]) + ',' + str(gameResult[2]) + ',' + str(gameResult[3]) + ',' + str(gameResult[4]) + ',' + str(gameResult[5])
    return tests


def runTestsOnSectionMulti(words: pandas.core.frame.DataFrame, heuristic: str, outFileName: str, start: int, finish: int) -> str:
    print("starting chunk -> words", start, "to", finish,)
    gameNumber = start
    chunkLength = finish - start
    tests = ""
    lastProgress = 0
    with open(outFileName, "a") as outFile:
        wordVals = words.values[gameNumber:]

        for word in wordVals:
            gameNumber += 1
            progress = int(100.0 / float(chunkLength) * float(gameNumber - start))
            if progress != lastProgress:
                print("chunk with words", start, "to", finish, "is", progress, "% done")
            lastProgress = progress
            if gameNumber >= finish:
                break
            word = word[0]
            gameResult = testGame(word, words, heuristic)
            #print(gameResult)
            tests += "\n" + str(gameNumber) + ',' + gameResult[0] + ',' + str(gameResult[1]) + ',' + str(gameResult[2]) + ',' + str(gameResult[3]) + ',' + str(gameResult[4]) + ',' + str(gameResult[5])
    return tests

def runTestsOnDictMulti(words, heuristic, outFileName, processCount):
    wordCount = len(words)
    chunkSize = int(wordCount/processCount)

    print("words", wordCount)
    print("chunk size", chunkSize)

    # assign chunks to processes
    chunkPool = Pool(processes=processCount)
    parameters = []
    for i in range(0, processCount):
        start = i*chunkSize
        if i < 5:
            finish = (i+1)*chunkSize
        else:
            finish = wordCount
        print("chunk:", i, "-> words", start, "to", finish)
        parameters.append((words, heuristic, outFileName, start, finish))
    print("assigning chunks to processes")
    chunks = chunkPool.starmap(runTestsOnSectionMulti, parameters)
    #print(chunks)
    with open(outFileName, "w") as outFile:
        outFile.write("gameNumber,word,wordLength,guessCount,correctGuessCount,incorrectGuessCount,usedLetters"+chunks)


if __name__ == '__main__':
    #freeze_support()

    dictFrame = HangmanSolver.loadDictionary(r"dictionaries/Collins Scrabble Words (2019).txt")
    print("loaded", len(dictFrame), "words\n")

    # print(testGame("zwitterionic", dictFrame, "positionsInWord"))
    # HangmanSolver.runExample()
    # makeDictFromDict(dictFrame)
    # runTestsOnDict(dictFrame, "positionsInWord", r"outFiles/positionsInWord_Collins Scrabble Words (2019).csv")
    # runTestsOnSectionOfDict(dictFrame, "positionsInWord", r"outFiles/positionsInWord_Collins Scrabble Words (2019).csv", 71613, 71620)
    # OutFileEvaluator.aggregateOutFileData(r"outFiles/positionsInWord_Collins Scrabble Words (2019).csv", r"aggFiles/aggData_positionsInWord_Collins Scrabble Words (2019).csv")
    runTestsOnDictMulti(dictFrame, "positionsInWord", r"outFiles/positionsInWord_Collins Scrabble Words (2019).csv", 6)
