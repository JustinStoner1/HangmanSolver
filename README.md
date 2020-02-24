# HangmanSolver

## Description

The goal of this project is to create a set of heuristics or strategies that a computer player could use to play games of Hangman. I will also be evaluating and testing heuristics with the Collins Scrabble Words (2019) dictionary to determine which strategies give the best of changing minimizing the number of guesses required to correctly guess the secret word.

## Implemented Heuristics

### Letter Frequency

Letter frequency is the perhaps the most basic strategy for choosing a letter. The frequency is the number of times a letter is found in the dictionary over the total number of letters. Guessing based on frequency gives the best chance of getting a letter on the board because it is based purely on what is most likely to occur. There are two pitfalls for frequency based guessing. One: words containing rare letters such as "Jazz"; rare letters are a problem for this strategy because they will be the last letters to guess. Two: the fact that words are not made of randomly chosen letters; meaning that while frequency is good for getting hits, it might not be as good for completeing words when the remaining possibilites are similar.

![Frequency](/Graphics/frequency.png)

### Occurrence

Occurrence is similar to frequency excecpt that letters are only counted once per word. The idea being that aften appear more than once, such as 't', 'i', or 'l' in words like "thought", "zwitterionic", and "literally" have a lesser impact on the frequency, allowing rarer letters to have a slightly better chance. It appears that this heuristic often guesess the same as frequency.

![Occurrence](/Graphics/occurrence.png)

### Absence

Absence is the literal opposite of occurrence, the letter that appears in the least number of words is guessed. The idea behind this one is that if the rarest letter is guessed, it would narrow down the possibilites very fast. While that might not be a bad strategy in some cases, such as "jazz", it seems to not work out in most cases.

### OccurrenceInWord

OccurrenceInWord weights guesses words that appear more times when they appear. 'q' for example, usually only appears once in a given word; 'i' on the other hand, occurs in words like "possibilites" many times. The strategy with this heuristic is that these letters, if correct, would give a lot of information.

![Repetition](/Graphics/repetition.png)

### PositionsInWord

PositionsInWord guesses letters based on the different number of positions or places they appear in. Words that appear often, but also show up in different postions in the word have a higher chance of being guessed.

![Position](/Graphics/position.png)


