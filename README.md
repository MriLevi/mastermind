# Mastermind
Python implementation of [Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game)) board game. Both roles may be played by either the user or computer. Furthermore, computer can use multiple algorithms.

# Rules
User may assume any of the two roles: code maker or code breaker. Role(s) not selected by the user will be played by computer.
        
Code maker invents a secret code and provides feedback to the code breaker. Code breaker tries to guess the secret code invented by the code maker.
        
By default, code is a combination of 4 colors numbered from 1 to 6. Colors may repeat.
        
Feedback is given in the form of x,y

x represents the amount of colors that are correct, and in the correct position

y represents the amount of colors that are correct, but in the wrong position

#Algorithms
I've implemented multiple guessing algorithms. Some are better than others.

Algorithm 1 = Simple Strategy by Shapiro.

```10000 tests of Algorithm 1
Average tries: 5.7627. Program took 108.25434517860413 seconds to run. We took 0.0108 seconds per try.
```

Algorithm 2 = Simple Strategy with random choice by me. 
```10000 tests of Algorithm 2
Average tries: 4.628. Program took 83.18712830543518 seconds to run. We took 0.0083 seconds per try.
```

Algorithm 3 = Worst Case strategy by Donald Knuth. 
This algorithm is based on Donald Knuth's worst case algorithm. It's significantly slower than the others.
For normal gameplay, the speed is perfectly fine. For simulations, it can be quite slow.
```10000 tests of Algorithm 3
Average tries was 4.471582181259601. Program took 6386.86208987236023 seconds to run. We took 0.6386 seconds per try.
```

Algorithm 4 = Human Color Elimination Algorithm by Levi Verhoef
This algorithm tries to eliminate 2 colors before switching over to the simple strategy.
```10000 tests of Algorithm 4
Average tries was 7.8485. Program took 80.93378806114197 seconds to run. We took 0.008 seconds per try.
```

# Usage
```
    usage: mastermind.py [-h] [-colors COLORS] [-positions POSITIONS] [--maker]
                         [--breaker] [--no_duplicates] [--auto_feedback] [--rules]
    
    play mastermind board game, computer guesses based on a selected algorithm
    
    
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
