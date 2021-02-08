import random


def mastermind():
    print("level? (1/2/3/4)")
    level = int(raw_input("> "))
    if level < 3:
        colours = ["a", "b", "c", "d", "e", "f"]
    else:
        colours = ["a", "b", "c", "d", "e", "f", "g"]

    random.shuffle(colours)
    code = ""
    if level % 2 == 1:
        for i in range(4):
            code += colours[i]
    else:
        for i in range(4):
            code += random.choice(colours)

    count = 10
    list_of_answers = "\n"
    while count != 0:
        count -= 1
        print("Make a guess!")
        guess = input()
        while len(guess) != 4:
            print("Guess 4 letters!")
            guess = input()
        if guess == code:
            print("\nYou win!")
            print("Again? (Y/N)")
            if input().upper() == "Y":
                mastermind()
                return
            else:
                return
        rs, ws = 0, 0
        codematch = code
        for i in range(4):
            if guess[i] == code[i]:
                rs += 1
            elif guess[i] in codematch:
                indices = [j for j, x in enumerate(codematch) if x == guess[i]]
                for index in indices:
                    if guess[index] == guess[i]:
                        continue
                    else:
                        ws += 1
                        codematch = codematch[0:index] + "x" + codematch[index + 1:]
                        break

        list_of_answers += guess + "        " + "r" * rs + "w" * ws + "\n"
        print(list_of_answers)
    print("You lose! The code was " + code)
    mastermind()


class Solver(object):
    def __init__(self):
        self.colours = ["a", "b", "c", "d", "e", "f"]
        self.responses = []

    def get_response(self, guess):
        print("\nI guess: " + guess)
        return input("How right was I?")

    def solve(self):
        """currently only level 1 solved"""
        self.current_colours = [c for c in self.colours]
        random.shuffle(self.current_colours)
        guess = ""
        for i in range(4):
            guess += self.current_colours[i]
        print("think of a sequence of 4 containing a,b,c,d,e,f with no repeats.")
        response = self.get_response(guess)
        self.responses.append((guess, response))
        self.right_colours = guess
        if len(response) < 4:
            self.right_colours = self.solve_for_colours(guess, response)
            print("I know the colours! " + self.right_colours)
        self.solve_for_places()

    def solve_for_colours(self, guess, response):
        if len(response) == 2:
            letters = explode(guess)
            random.shuffle(letters)
            kept = []
            for i in range(2):
                kept.append(letters.pop())
            guess = kept + [l for l in self.current_colours if l not in guess]
            guess = implode(guess)
            response = self.get_response(guess)
            self.responses.append((guess, response))
            if len(response) == 2:
                return implode([l for l in self.current_colours if l not in kept])
            elif len(response) == 3:
                pair1 = implode([l for l in guess if l not in kept])
                pair2 = [l for l in kept]
                pair3 = [l for l in self.current_colours if l not in pair1 and l not in pair2]
                guess = pair1 + pair2[0] + pair3[0]
                response = self.get_response(guess)
                self.responses.append((guess, response))
                if len(response) == 2:
                    return pair1 + pair2[1] + pair3[1]
                elif len(response) == 3:
                    guess = pair1 + pair2[0] + pair3[1]
                    response = self.get_response(guess)
                    self.responses.append((guess, response))
                    if len(response) == 2:
                        return pair1 + pair2[1] + pair3[0]
                    else:
                        return guess
                else:
                    return guess
            else:
                return guess

        else:
            first_guess = guess
            letters = explode(guess)
            random.shuffle(letters)
            kept = []
            for i in range(3):
                kept.append(letters.pop())
            changed_to = None
            for c in self.current_colours:
                if c in guess:
                    continue
                else:
                    changed_to = c
                    break
            guess = implode(kept + [changed_to])
            response = self.get_response(guess)
            self.responses.append((guess, response))
            if len(response) == 2:
                self.current_colours.remove(changed_to)
                required = [i for i in self.current_colours if i not in first_guess]
                changed = [i for i in first_guess if i not in kept]
                while True:
                    to_change = random.choice([i for i in first_guess if i not in changed])
                    changed.append(to_change)
                    guess = implode([i for i in first_guess if i != to_change] + required)
                    response = self.get_response(guess)
                    self.responses.append((guess, response))
                    if len(response) == 4:
                        return guess
            elif len(response) == 3:
                required = [changed_to]
                changed = [i for i in first_guess if i not in kept]
                ###########################################################################
                # Bug here! Can also be length 2, in which case required is not required!
                while True:
                    to_change = random.choice([i for i in first_guess if i not in changed])
                    changed.append(to_change)
                    guess = implode([i for i in first_guess if i != to_change] + required)
                    response = self.get_response(guess)
                    self.responses.append((guess, response))
                    if len(response) == 4:
                        return guess
            elif len(response) == 4:
                return guess

    def solve_for_places(self):
        # Here columns are letters, rows are places. If letter l is possible in place p, p_t_l[p][l] = 1
        self.place_to_letter = [[1] * 4 for i in range(4)]
        self.search_for_patterns(self.responses)
        print(self.place_to_letter)
        while True:
            ### Maximum matching algorithm required!
            guess = self.max_match()
            response = self.get_response(guess)
            if response == "rrrr":
                print("Hooray!")
                return
            self.search_for_patterns([(guess, response)])

    def max_match(self):
        guess = []
        # Here rows are letters, columns are places. If letter l is possible in place p, l_t_p[l][p] = 1
        self.letter_to_place = zip(*self.place_to_letter)
        for i in range(4):
            ps = [l for l, p in zip(self.right_colours, self.place_to_letter[i]) if p == 1 and l not in guess]
            if ps:
                guess.append(random.choice(ps))
            else:
                ps.append("x")
        while "x" in guess:
            places = explode(guess)
            index = places.index("x")
            nodes = [index]
            letter1 = random.choice([l for l, x in enumerate(self.place_to_letter[index]) if x == 1])
            nodes.append(letter1)
            while self.right_colours[nodes[len(nodes) - 1]] in places:
                placen = random.choice([p for p, x in enumerate(self.letter_to_place[nodes[len(nodes - 1)]]) if
                                        x == 1 and p not in nodes[::2]])
                nodes.append(placen)
                lettern = random.choice([l for l, x in enumerate(self.place_to_letter[nodes[len(nodes - 1)]]) if
                                         x == 1 and l not in nodes[1::2]])
                nodes.append(lettern)
            for i in range(len(nodes) / 2):
                guess[nodes[2 * i]] = self.right_colours[nodes[2 * i + 1]]

        return implode(guess)

    def search_for_patterns(self, responses):
        for guess, response in responses:
            if "r" not in response:
                for i in range(4):
                    if guess[i] in self.right_colours:
                        l = self.right_colours.index(guess[i])
                        self.place_to_letter[i][l] = 0


def explode(s):
    return [l for l in s]


def implode(l):
    s = ""
    for i in l:
        s += str(i)
    return s


solve = input("Do you want to be the codemaster? (Y/N) ").upper() == "Y"
if solve:
    s = Solver()
    s.solve()
else:
    mastermind()