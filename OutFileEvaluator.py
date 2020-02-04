import csv


def aggregateOutFileData(outFileName: str, aggDataFileName: str):
    with open(outFileName, "r") as outFileCSV:
        outFileReader = csv.DictReader(outFileCSV, delimiter=',')
        entryCount = 0  # len(outFileCSV.readlines())
        print("aggregating", entryCount, "entries")
        totalWordLength = 0
        totalAvgGuesses = 0
        totalAvgCorrectGuesses = 0
        totalAvgWrongGuesses = 0
        dataDict = {}
        for entry in outFileReader:
            print(entry)
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
                dataDict[wordLength] = (values[0] + guesses, values[1] + correctGuesses, values[2] + wrongGuesses, values[3] + 1)
            else:
                dataDict[wordLength] = (guesses, correctGuesses, wrongGuesses, 1)

        avgCorrectGuessesPerLetter = totalAvgGuesses/entryCount  # how many correct guesses it takes to find the secret word per letter in the secret word
        avgGuessesPerLetter = totalAvgCorrectGuesses/entryCount  # how many guesses it takes to find the secret word per letter in the secret word
        avgWrongGuessesPerLetter = totalAvgWrongGuesses/entryCount  # how many wrong guess are usually incurred in a game per letter in the secret word

        print("avgGuessesPerLetter", avgGuessesPerLetter)
        print("avgCorrectGuessesPerLetter", avgCorrectGuessesPerLetter)
        print("avgWrongGuessesPerLetter", avgWrongGuessesPerLetter)

    aggDataFileLines = "wordLength,avgGuessesPerLetter,avgCorrectGuessesPerLetter,avgWrongGuessesPerLetter"
    for k, v in sorted(dataDict.items()):
        # print("\nFor words of length", k)

        avgGuesses = v[0]/v[3]
        avgCorrectGuesses = v[1]/v[3]
        avgWrongGuesses = v[2]/v[3]
        aggDataFileLines += "\n" + str(k) + ',' + str(avgGuesses) + ',' + str(avgCorrectGuesses) + ',' + str(avgWrongGuesses)

    with open(aggDataFileName, "w") as aggDataFile:
        aggDataFile.write(aggDataFileLines)

    print("agg data written at:", aggDataFileName)
