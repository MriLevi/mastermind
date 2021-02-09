import random
import time


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
                            input("Enter feedback for {} in the form of 1,2 where 1 is black pegs, 2 is white pegs: ".format(guess_as_string)))
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
        print(self._code)

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

        # most recent feedback
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

        #populate the lists on initialization of the program
        for getal1 in range(1, 7):
            for getal2 in range(1, 7):
                for getal3 in range(1, 7):
                    for getal4 in range(1, 7):
                        self._allList.append([getal1, getal2, getal3, getal4])
                        self._possiblesecrets.append([getal1, getal2, getal3, getal4])

    def make_guess(self, tries):
        #keep track of the tries weve done so far
        self._tries = tries
        #this function might be redundant, could probably just call _make_guess instead

        return self._make_guess(_args.algorithm)


    def _make_guess(self, algorithm):
        #updated simple strategy
        #this is still not completely done, this takes 10 tries on average where
        #simple strategy should take about 5.7
        #find out wtf im not doing right yet


        if algorithm == 1:  ##simple strategy

            #make a copy of list of possible secrets
            templist = self._possiblesecrets.copy()
            recentfeedback = self._most_recent_feedback

            if self._tries == 0:
                current_guess = self._possiblesecrets[0]
                self._most_recent_guess = current_guess
                return current_guess

            elif len(self._possiblesecrets) > 1:
                for secret in templist:
                    if _auto_feedback(secret, self._most_recent_guess) != self._most_recent_feedback:
                        self._possiblesecrets.remove(secret)
                current_guess = self._possiblesecrets[0]
                self._most_recent_guess = current_guess
                return current_guess

            else:
                print(self._possiblesecrets)
                current_guess = self._possiblesecrets[0]
                return current_guess
        elif algorithm == 2: ## simple strategy with random choice
            # make a copy of list of possible secrets
            templist = self._possiblesecrets.copy()
            recentfeedback = self._most_recent_feedback

            if self._tries == 0:
                current_guess = [1, 1, 2, 3]
                self._most_recent_guess = current_guess
                return current_guess

            elif len(self._possiblesecrets) > 1:
                for secret in templist:
                    if _auto_feedback(secret, self._most_recent_guess) != self._most_recent_feedback:
                        self._possiblesecrets.remove(secret)
                current_guess = random.choice(self._possiblesecrets)
                self._most_recent_guess = current_guess
                return current_guess

            else:
                print(self._possiblesecrets)
                current_guess = self._possiblesecrets[0]
                return current_guess
        elif algorithm == 3:
            print('do nothing')

    def receive_feedback(self, guess, feedback):
        #save the most recently received feedback
        self._most_recent_feedback = feedback
        #save all feedback in a list
        self._received_feedback += [feedback]

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
        if feedback == [4,0]: #win the game!
            return True
        return False #keep going


def _auto_feedback(code, guess):
    #here we automatically generate feedback
    #this is useful to be able to simulate a lot of games to get statistics

    #make default feedback
    feedback = [0,0]
    #copy the code and the guess so we edit those and not the original
    codecopy = code.copy()
    guesscopy = guess.copy()

    #calculate the feedback
    #first, check for black pins, and remove the corresponding entries from the copied list
    for i in range(0, len(code)):
        if code[i] == guess[i]:
            feedback[0] += 1
            guesscopy.remove(guess[i])
            codecopy.remove(code[i])
    #then, check for white pins by checking if non-matched positions are present in trimmed copy list
    for i in range(0, len(guesscopy)):
        if guesscopy[i] in codecopy:
            feedback[1] +=1
            codecopy.remove(guesscopy[i]) #once we find a white pin, remove corresponding entry so we dont duplicate it

    return feedback


def play_mastermind(code_maker, code_breaker):
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