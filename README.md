# Mastermind
Python implementation of [Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) board game. Both roles may be played by either the user or computer. Furthermore, computer can use multiple algorithms.

# Rules
User may assume any of the two roles: code maker or code breaker. Role(s) not selected by the user will be played by computer.
        
Code maker invents a secret code and provides feedback to the code breaker. Code breaker tries to guess the secret code invented by the code maker.
        
By default, code is a combination of 4 colors numbered from 1 to 6. Colors may repeat.
        
Feedback is given in the form of x,y

x represents the amount of colors that are correct, and in the correct position

y represents the amount of colors that are correct, but in the wrong position
# Usage
```
    usage: mastermind.py [-h] [-colors COLORS] [-positions POSITIONS] [--maker]
                         [--breaker] [--no_duplicates] [--auto_feedback] [--rules]
    
    play mastermind board game, computer guesses based on a selected algorithm
    Algorithm 1 = Simple Strategy by Shapiro. Average guesses: 5.76
    Algorithm 2 = Simple Strategy with random choice by me. Average guesses: 4,62
    Algorithm 3 = Worst Case strategy. not implemented yet.
    
    optional arguments:
      -h, --help            show this help message and exit
      -colors COLORS        number of colors
      -positions POSITIONS  number of positions in code
      --maker               play as code maker
      --breaker             play as code breaker
      --no_duplicates       disallow duplicate colors
      --auto_feedback       automatically give feedback when user is playing as
                            code maker
      --rules               show rules and exit
```

# Example
`python3 mastermind.py --maker --auto_feedback` output:
```
Code maker is played by the user.
Code breaker is played by computer.
Code breaker is using algorithm 1
Enter secret code: 3145
1111 [1, 0]
1222 [0, 1]
3133 [2, 0]
3144 [3, 0]
3145 [4, 0]
Correct! in 5

```
