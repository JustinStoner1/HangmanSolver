import csv


def aggregateOutFileData(outFileName: str, aggDataFileName: str):
    with open(outFileName, "r") as outFileCSV:
        outFileReader = csv.DictReader(outFileCSV, delimiter=',')
        entryCount = 0  # len(outFileCSV.readlines())
        totalWordLength = 0
        totalAvgGuesses = 0
        totalAvgCorrectGuesses = 0
        totalAvgWrongGuesses = 0
        dataDict = {}
        for entry in outFileReader:
            # print(entry)
            entryCount += 1
            wordLength = int(entry["wordLength"])
            guesses = int(entry["guessCount"])
            correctGuesses = int(entry["correctGuessCount"])
            wrongGuesses = int(entry["incorrectGuessCount"])

            # raw aggregate
            totalWordLength += wordLength  # entry(2)
            totalAvgGuesses += guesses/wordLength  # entry(3)
            totalAvgCorrectGuesses += correctGuesses/wordLength  # entry(4)
            totalAvgWrongGuesses += wrongGuesses/wordLength  # entry(5)

            # specific data
            if wordLength in dataDict:
                values = dataDict[wordLength]
                dataDict[wordLength] = (values[0] + guesses, values[1] + guesses*guesses, values[2] + correctGuesses, values[3] + correctGuesses*correctGuesses, values[4] + wrongGuesses, values[5] + wrongGuesses*wrongGuesses, values[6] + 1)
            else:
                dataDict[wordLength] = (guesses, guesses*guesses, correctGuesses, correctGuesses*correctGuesses, wrongGuesses, wrongGuesses*wrongGuesses, 1)

        avgCorrectGuessesPerLetter = totalAvgGuesses/entryCount  # how many correct guesses it takes to find the secret word per letter in the secret word
        avgGuessesPerLetter = totalAvgCorrectGuesses/entryCount  # how many guesses it takes to find the secret word per letter in the secret word
        avgWrongGuessesPerLetter = totalAvgWrongGuesses/entryCount  # how many wrong guess are usually incurred in a game per letter in the secret word

        print("avgGuessesPerLetter", avgGuessesPerLetter)
        print("avgCorrectGuessesPerLetter", avgCorrectGuessesPerLetter)
        print("avgWrongGuessesPerLetter", avgWrongGuessesPerLetter)

    aggDataFileLines = "wordLength,avgGuessesPerLetter,avgCorrectGuessesPerLetter,avgWrongGuessesPerLetter,stddevGuessesPerLetter,stddevCorrectGuessesPerLetter,stddevWrongGuessesPerLetter"
    # find mean
    means = {}
    for k, v in sorted(dataDict.items()):
        # print("\nFor words of length", k)

        avgGuesses = v[0]/v[6]
        avgCorrectGuesses = v[2]/v[6]
        avgWrongGuesses = v[4]/v[6]

        stddevGuesses = v[1]/v[6]-avgGuesses*avgGuesses
        stddevCorrectGuesses = v[3]/v[6]-avgCorrectGuesses*avgCorrectGuesses
        stddevWrongGuesses = v[5]/v[6]-avgWrongGuesses*avgWrongGuesses

        aggDataFileLines += "\n" + str(k) + ',' + str(avgGuesses) + ',' + str(avgCorrectGuesses) + ',' + str(avgWrongGuesses) + ',' + str(stddevGuesses) + ',' + str(stddevCorrectGuesses) + ',' + str(stddevWrongGuesses)

        means[k] = (avgGuesses, avgCorrectGuesses, avgWrongGuesses)

    with open(aggDataFileName, "w") as aggDataFile:
        aggDataFile.write(aggDataFileLines)

    print("agg data written at:", aggDataFileName)
