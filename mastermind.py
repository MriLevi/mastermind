import random
import itertools as iter


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
                            input("Enter feedback for {}: ".format(guess_as_string)))
                    except ValueError as e:
                        print("Entered feedback is invalid: {}".format(e))
        else:
            raise ValueError("no code to provide feedback for")


class ComputerCodeMaker(CodeMaker):
    def __init__(self, game_utils):
        self._game_utils = game_utils
        self._code = None

    def make_code(self):
        # computer invents a random secret code
        self._code = self._game_utils.random_code()

    def give_feedback(self, guess):
        # computer gives automated feedback based on guess and secret code
        if self._code is not None:
            return _auto_feedback(self._code, guess)
        else:
            raise ValueError("no code to provide feedback for")


class HumanCodeBreaker(CodeBreaker):
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
    def __init__(self, game_utils, algorithm):
        self._game_utils = game_utils
        # valid_guess matrix (n_positions, n_colors) describes
        # all possible guesses by enumerating (position, color) pairs
        self._valid_guess = [[True for _ in range(game_utils.n_colors)] for _ in range(game_utils.n_positions)]
        # set of all yet unseen colors
        self._unseen_colors = set([color for color in range(game_utils.n_colors)])
        # set of all right colors
        self._right_colors = set()
        # flag whether all right colors have been found
        self._right_colors_found = False
        # most recent feedback
        self._received_feedback = []
        #tries
        self._tries = 0
        #list of all combinations
        self._allList = []
        #list of all current options
        self._optionList = []
        for getal1 in range(1, 7):
            for getal2 in range(1, 7):
                for getal3 in range(1, 7):
                    for getal4 in range(1, 7):
                        self._allList.append([getal1, getal2, getal3, getal4])
                        self._optionList.append([getal1, getal2, getal3, getal4])

    def make_guess(self, tries):
        current_guess = [None] * self._game_utils.n_positions
        # remove colors that are wrong
        colors_to_check = [color in self._right_colors or color in self._unseen_colors for color in
                           range(self._game_utils.n_colors)]
        self._tries = tries

        return self._make_guess(_args.algorithm)


    def _make_guess(self, algorithm):
        # performs depth first search for a valid guess using information in the guess matrix
        # for selecting a color in any given position

        if algorithm == 1:  ##simple strategy
            # prepare all viable colors at this position given information so far
            if self._tries == 0:
                current_guess = [1,1,2,3]
            else:
                current_guess = random.choice(self._allList)
            feedback = self._received_feedback

            return current_guess

        elif algorithm == 2:
            print('do nothing')
        elif algorithm == 3:
            print('do nothing')

    def receive_feedback(self, guess, feedback):
        # !!! this part is still wrong !!!
        # !!! it uses feedback pegs in a positional way, but feedback pegs do not give positional information !!!
        # !!! need to rewrite this !!!

        # updates guess matrix according to the information from code maker
        self._received_feedback += [guess, feedback]

class MastermindGameUtils(object):
    def __init__(self, n_colors=6, n_positions=4, duplicates_allowed=True):
        if not duplicates_allowed and n_positions > n_colors:
            raise ValueError("not enough colors for this number of positions")
        self.n_colors = n_colors
        self.n_positions = n_positions
        self.duplicates_allowed = duplicates_allowed

    def validate_code(self, code):
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
        if len(feedback) != self.n_positions:
            raise ValueError("feedback must consist of exactly {} pegs".format(self.n_positions))
        for peg in feedback:
            if peg not in "bw.":
                raise ValueError("peg must be one of following: 'b', 'w', '.'")
        return feedback

    def random_code(self, duplicates_allowed=None):
        if duplicates_allowed is None:
            duplicates_allowed = self.duplicates_allowed
        elif duplicates_allowed is True and self.duplicates_allowed is False:
            raise ValueError("duplicates are not allowed")
        if duplicates_allowed:
            return [random.randint(1, self.n_colors) for _ in range(self.n_positions)]
        else:
            return random.sample(range(1, self.n_colors + 1), self.n_positions)


def _is_guess_correct(feedback):
    if feedback is not None:
        for peg in feedback:
            if peg != 'b':
                return False
        return True
    return False


def _auto_feedback(code, guess):
    feedback = ""
    for guessed_color, actual_color in zip(guess, code):
        if guessed_color == actual_color:
            feedback += 'b'
        elif guessed_color in code:
            feedback += 'w'
        else:
            feedback += '.'
    return feedback


def play_mastermind(code_maker, code_breaker):
    code_maker.make_code()
    tries=0
    while True:
        tries+=1 #keep track of the amount of tries
        guess = code_breaker.make_guess(tries)
        if guess is not None:
            feedback = code_maker.give_feedback(guess)
            guess_as_string = "".join([str(color) for color in guess])
            print(guess_as_string, feedback)
            if _is_guess_correct(feedback):
                with open('results.txt', "a") as f: #append the results to a txt file, used for me to check big samples quickly, probably not in final product
                    f.write(f'{tries}\n')
                    f.close()
                return print(f'Correct! in {tries}')
            else:
                code_breaker.receive_feedback(guess, feedback)
        else:
            return print("Guess could not be made. Make sure your input is valid.")


if __name__ == "__main__":
    """
    usage: mastermind.py [-h] [-colors COLORS] [-positions POSITIONS] [--maker]
                         [--breaker] [--no_duplicates] [--auto_feedback] [--rules]
    
    play mastermind board game
    
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
        _code_breaker = ComputerCodeBreaker(_game_utils, _args.algorithm)

    play_mastermind(_code_maker, _code_breaker)