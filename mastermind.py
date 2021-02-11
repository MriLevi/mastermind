### this code is forked and based off https://github.com/kweimann/mastermind
### I've had to adjust quite a few modules and functions, but a good amount of them have been left as is
### I will annotate which ones have been written by me or extensively rewritten by me.
### Most of the class based structure was already in place.

import random
from itertools import product

class CodeMaker(object):
    def make_code(self):
        """
        code maker invents a secret code
        """
        raise NotImplemented()

    def give_feedback(self, guess):
        """
        :param guess: guess made by code breaker
        :return: feedback that evaluates guess against secret code
        """
        raise NotImplemented()


class CodeBreaker(object):
    def make_guess(self):
        """
        :return: guess code
        """
        raise NotImplemented()

    def receive_feedback(self, guess, feedback):
        """
        code breaker may use feedback information to select next guess code
        :param guess: last guess made by code breaker
        :param feedback: feedback information from code maker
        """
        raise NotImplemented()


class HumanCodeMaker(CodeMaker):
    '''
    This class is used when the user selects to play as codemaker.
    it initializes, asks the user to input a code and validates it
    then it also asks for feedback, unless the program is started with the autofeedback flag.
    if feedback is done manually, we also evaluate it by calling validate_feedback
    '''

    def __init__(self, game_utils, auto_feedback=False):
        self._game_utils = game_utils
        self._auto_feedback = auto_feedback
        self._code = None

    def make_code(self):
        # user enters secret code
        while self._code is None:
            try:
                self._code = self._game_utils.validate_code(input("Enter secret code: "))
            except ValueError as e:
                print("Entered code is invalid: {}".format(e))

    def give_feedback(self, guess):
        # user enters feedback for guess code based on his secret code
        if self._code is not None:
            if self._auto_feedback:
                return _auto_feedback(self._code, guess)
            else:
                while True:
                    try:
                        guess_as_string = "".join([str(color) for color in guess])
                        return self._game_utils.validate_feedback(
                            input("Enter feedback for {} in the form of 1,2 where 1 is black pegs, 2 is white pegs: ".format(guess_as_string)))
                    except ValueError as e:
                        print("Entered feedback is invalid: {}".format(e))
        else:
            raise ValueError("no code to provide feedback for")


class ComputerCodeMaker(CodeMaker):
    '''
    This class is called when the codemaker is selected to be a computer.
    It initialises, loads game_utils, makes a random code
    and provides the other player (computer or human) with feedback
    '''

    def __init__(self, game_utils):
        self._game_utils = game_utils
        self._code = None

    def make_code(self):
        # computer invents a random secret code
        self._code = self._game_utils.random_code()
        print(f'secret code to guess: {self._code}')

    def give_feedback(self, guess):
        # computer gives automated feedback based on guess and secret code
        if self._code is not None:
            return _auto_feedback(self._code, guess)
        else:
            raise ValueError("no code to provide feedback for")


class HumanCodeBreaker(CodeBreaker):
    '''
    this class is used when user selects to play as codebreaker.
    It asks the user to input a guess, and validates that code.
    '''
    def __init__(self, game_utils):
        self._game_utils = game_utils

    def make_guess(self, tries):
        # user enters next guess
        while True:
            try:
                return self._game_utils.validate_code(input("Enter code: "))
            except ValueError as e:
                print("Entered code is invalid: {}".format(e))

    def receive_feedback(self, guess, feedback):
        # user receives feedback (already made visible by the game master)
        pass


class ComputerCodeBreaker(CodeBreaker):
    '''
    This class is used when the computer is playing as the CodeBreaker.
    Most if not all of the code here was written by me.
    On initialization, it loads a few useful parameters and populates the starting list of possible secrets.
    In this class, we also can find the implemented guessing algorithms.
    Based on the value chosen for the -algorithm parser flag
    the computer can use different guessing algorithms to return a next guess.
    '''
    def __init__(self, game_utils):
        '''most of these variables were programmed in by Levi Verhoef'''
        self._game_utils = game_utils
        # list of all received feedback so far, not sure if this is gonna be used yet
        self._received_feedback = []
        #tries
        self._tries = 0
        #most recent guess
        self._most_recent_guess = ''
        #most recent feedback
        self._most_recent_feedback= []
        #list of all combinations
        self._allList = []
        #list of all current options
        self._possiblesecrets = []



        #populate the lists of possible secrets on initialization of the program
        self._possiblesecrets = list(product(range(1,7), repeat=4))
        self._allList = list(product(range(1,7), repeat=4))

    def make_guess(self, tries):
        '''
        All code below is made by Levi Verhoef
        Algorithm 1 is the simple strategy by Shapiro.
        Algorithm 2 is the simple strategy by shapiro but with a random guess instead of first list element
        '''
        algorithm = _args.algorithm
        #keep track of the tries weve done so far
        self._tries = tries


        if algorithm == 1:  ##simple strategy

            # make a copy of list of possible secrets
            templist = self._possiblesecrets.copy()
            recentfeedback = self._most_recent_feedback

            if self._tries == 0:
                current_guess = self._possiblesecrets[0]
                self._most_recent_guess = current_guess
                return current_guess

            elif len(self._possiblesecrets) > 1:
                _reduce(self, templist)
                current_guess = self._possiblesecrets[0]
                self._most_recent_guess = current_guess
                return current_guess

            else:
                current_guess = self._possiblesecrets[0]
                return current_guess
        elif algorithm == 2:  ## simple strategy with random choice
            # make a copy of list of possible secrets
            templist = self._possiblesecrets.copy()
            recentfeedback = self._most_recent_feedback

            if self._tries == 0:
                current_guess = [1, 1, 2, 3]
                self._most_recent_guess = current_guess
                return current_guess

            elif len(self._possiblesecrets) > 1:
                _reduce(self, templist)
                current_guess = random.choice(self._possiblesecrets)
                self._most_recent_guess = current_guess
                return current_guess

            else:
                current_guess = self._possiblesecrets[0]
                return current_guess

        elif algorithm == 3: ## worst case

            # make a copy of list of possible secrets so we dont screw up our for loop

            templist = self._possiblesecrets.copy()

            if self._tries == 0:
                current_guess = (1, 1, 2, 2)
                self._possiblesecrets.remove(current_guess)
                self._allList.remove(current_guess)
                self._most_recent_guess = current_guess
                return current_guess

            elif len(self._possiblesecrets) == 1:

                current_guess = self._possiblesecrets[0]
                self._possiblesecrets.remove(current_guess)
                return current_guess

            else:
                #reduce the amount of secrets in possiblesecrets
                _reduce(self, templist)
                #if the length < 3 we only have two correct guesses remaining which we then submit one of.

                if len(self._possiblesecrets) < 3:
                    current_guess = self._possiblesecrets[0]
                    self._possiblesecrets.remove(current_guess)
                    return current_guess

                scores = {}
                ##here we check all secrets vs the remaining possible answers
                ##we give them a score based on the maximum amount of possible answers it eliminates
                ##we then choose an option that eliminates the least amount of options
                for secret in self._allList:
                    feedbackdict = {}
                    for secret2 in self._possiblesecrets:
                            feedback = _auto_feedback(secret, secret2)  #check every secret with every other secret
                            feedback = tuple(feedback)                  #we can't pass lists as keys for dicts
                            try:                                        #save received feedback in feedback dictionary
                                feedbackdict[feedback] += 1             #start counting how often it occurs
                            except:
                                feedbackdict[feedback] = 1
                    tuplesecret = tuple(secret)                     #same thing, can't pass lists as key
                    scores[tuplesecret] = max(feedbackdict.values()) #save the tested secret and it's maximum matched score

                best = min(scores.values())                         #the best guess has the least matched scores
                #select the first guess that has the best score - there could be multiple
                best_guesses = [guess for guess in scores.keys() if scores[guess] == best]
                current_guess = ''
                for guess in best_guesses:
                    if guess in self._possiblesecrets:
                        current_guess = guess
                        self._possiblesecrets.remove(current_guess)
                        break

                if current_guess == '':
                    current_guess = best_guesses[0]

                self._allList.remove(current_guess)
                self._most_recent_guess = current_guess
                return current_guess

        elif algorithm == 4:
            print('do nothing')




    def receive_feedback(self, guess, feedback):
        #save the most recently received feedback
        self._most_recent_feedback = feedback
        #save all feedback in a list
        self._received_feedback += [feedback]

class MastermindGameUtils(object):
    '''

    This class contains a few useful functions that are used throughout the game.
    On initalization it sets n_colors and n_positions based on flags used
    It also contains the utility to validate code and validate feedback
    '''

    def __init__(self, n_colors=6, n_positions=4, duplicates_allowed=True):
        if not duplicates_allowed and n_positions > n_colors:
            raise ValueError("not enough colors for this number of positions")
        self.n_colors = n_colors
        self.n_positions = n_positions
        self.duplicates_allowed = duplicates_allowed

    def validate_code(self, code):
        '''
        This function validates a given code. It starts by converting the code to a list of ints.
        Then it checks wether the code is of the right length
        Then it checks if the colors are all between the chosen n_colors.
        '''
        try:
            code = [int(color) for color in code]
        except (TypeError, ValueError):
            raise ValueError("code must be an iterable of numbers")
        if len(code) != self.n_positions:
            raise ValueError("code must consist of exactly {} colors".format(self.n_positions))
        if not self.duplicates_allowed and len(set(code)) != self.n_positions:
            raise ValueError("duplicates are not allowed")
        for color in code:
            if not 1 <= color <= self.n_colors:
                raise ValueError("color must be a number between 1 and {} (inclusive)".format(self.n_colors))
        return code

    def validate_feedback(self, feedback):
        '''
        function rewritten by Levi Verhoef
        this function validates feedback given by user
        it's kinda hacky but it works
        it checks if given feedback follows the x,y format
        it also checks if theres not more white or black pins than there are positions
        and lastly it checks wether the sum of white and black pins doesnt exceed the amount of positions
        '''
        #check if feedback input is in right format x,y where x,y are ints
        if len(feedback) != 3 or feedback[1] != ',' or not feedback[0].isnumeric() or not feedback[2].isnumeric():
            raise ValueError("feedback must be in format x,y where x is black bins and y is white pins")
        #check if user does not give more pins than there are positions
        elif int(feedback[0]) > self.n_positions < int(feedback[2]):
            raise ValueError(f'cant give more feedback than positions')
        #check if user does not give more total pins than positions
        elif int(feedback[0]) + int(feedback[2]) > self.n_positions:
            raise ValueError(f'youre giving too many pins')

        feedback = [int(feedback[0]), int(feedback[2])] #zet de feedback om naar juiste format

        return feedback

    def random_code(self, duplicates_allowed=None):
        '''
        This function returns a random code based on given parameters.
        '''
        if duplicates_allowed is None:
            duplicates_allowed = self.duplicates_allowed
        elif duplicates_allowed is True and self.duplicates_allowed is False:
            raise ValueError("duplicates are not allowed")
        if duplicates_allowed:
            return [random.randint(1, self.n_colors) for _ in range(self.n_positions)]
        else:
            return random.sample(range(1, self.n_colors + 1), self.n_positions)

def _reduce(self, list):
    for secret in list:
        if _auto_feedback(secret, self._most_recent_guess) != self._most_recent_feedback:
            self._possiblesecrets.remove(secret)
def _is_guess_correct(feedback):
    '''
    Function written by Levi Verhoef
    This simple function simply checks if we've found the right answer.
    '''

    if feedback is not None:
        if feedback == [4,0]: #win the game!
            return True
        return False #keep going


def _auto_feedback(code, guess):
    '''
    function written by Levi Verhoef
    this function automatically generates feedback for guesses
    this is used by default for computercodebreaker
    can also be used for a human codebreaker by using the flag --auto_feedback
    '''
    #make default feedback
    feedback = [0,0]
    #copy the code and the guess so we edit those and not the original
    codecopy = list(code)
    guesscopy = list(guess)

    #calculate the feedback
    #first, check for black pins, and remove the corresponding entries from the copied list
    for i in range(0, len(code)):
        if code[i] == guess[i]:
            feedback[0] += 1
            guesscopy.remove(guess[i])
            codecopy.remove(code[i])

    #then, check for white pins by checking if non-matched positions are present in trimmed copy list
    #once we find a white pin, remove corresponding entry to prevent assigning too many white pins.
    for i in range(0, len(guesscopy)):
        if guesscopy[i] in codecopy:
            feedback[1] +=1
            codecopy.remove(guesscopy[i])

    return feedback


def play_mastermind(code_maker, code_breaker):
    '''
    this is the main game loop and is used in any configuration (human vs human, cpu vs human or cpu vs cpu)
    i slightly modified this by adding a counter to keep track of the amount of tries
    i also added a text output module so I can run this file a lot of times to generate a big sample size
    to be able to test my algorithms and get an idea of average tries
    '''
    code_maker.make_code()
    tries=0
    while True:
        guess = code_breaker.make_guess(tries)
        tries += 1  # keep track of the amount of tries
        if guess is not None:
            feedback = code_maker.give_feedback(guess)
            guess_as_string = "".join([str(color) for color in guess]) #convert code to string for nice looks
            print(guess_as_string, feedback)
            if _is_guess_correct(feedback): #if the game is won
                with open('results.txt', "a") as f: #append the results to a txt file, probably not in final product
                    f.write(f'{tries}\n')
                    f.close()
                return print(f'Correct! in {tries}')
            else: #if the game hasnt been won
                code_breaker.receive_feedback(guess, feedback)
        else:
            return print("Guess could not be made. Make sure your input is valid.")


if __name__ == "__main__":
    """
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
    """
    import argparse

    _parser = argparse.ArgumentParser(description="play mastermind board game")
    _parser.add_argument("-colors", type=int, default=6, help="number of colors")
    _parser.add_argument("-positions", type=int, default=4, help="number of positions in code")
    _parser.add_argument("-algorithm", type= int, default=1, help="algorithm to use, 1 2 3")
    _parser.add_argument("--maker", action="store_true", default=False, help="play as code maker")
    _parser.add_argument("--breaker", action="store_true", default=False, help="play as code breaker")
    _parser.add_argument("--no_duplicates", action="store_true", default=False, help="disallow duplicate colors")
    _parser.add_argument("--auto_feedback", action="store_true", default=False,
                         help="automatically give feedback when user is playing as code maker")
    _parser.add_argument("--rules", action="store_true", default=False, help="show rules and exit")
    _args = _parser.parse_args()

    if _args.rules:
        print("""Rules:
        User may assume any of the two roles: code maker or code breaker.
        Role(s) not selected by the user will be played by computer.
        
        Code maker invents a secret code and provides feedback to the code breaker.
        Code breaker tries to guess the secret code invented by the code maker.
        
        Code is a combination of {} colors numbered from 1 to {}. 
        Colors may{}repeat.
        
        Feedback is a sequence of markers for each position.
        There are three valid markers:
            b   right color in the right position
            w   right color in a wrong position
            .   wrong color""".format(_args.positions, _args.colors, " not " if _args.no_duplicates else " "))
        exit()

    _game_utils = MastermindGameUtils(_args.colors, _args.positions, not _args.no_duplicates)

    if _args.maker:
        print("Code maker is played by the user.")
        _code_maker = HumanCodeMaker(_game_utils, _args.auto_feedback)
    else:
        print("Code maker is played by computer.")
        _code_maker = ComputerCodeMaker(_game_utils)

    if _args.breaker:
        print("Code breaker is played by the user.")
        _code_breaker = HumanCodeBreaker(_game_utils)
    else:
        print("Code breaker is played by computer.")
        print(f"Code breaker is using algorithm {_args.algorithm}")
        _code_breaker = ComputerCodeBreaker(_game_utils)

    play_mastermind(_code_maker, _code_breaker)