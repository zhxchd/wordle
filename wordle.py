import random

class wordle:

    def __init__(self, ans=None, max_check=6, filename="sgb-words.txt"):
        f = open("sgb-words.txt", "r")
        word_list = f.read().splitlines()
        self.word_set = set(word_list)
        f.close()
        self.num_checks = 0
        self.max_check = max_check
        if ans is None:
            self.ans = random.sample(word_list, 1)[0]
            print("New wordle initialized with random answer!")
        else:
            try:
                self.__test_valid(ans)
                self.ans = ans
                print("New wordle initialized with given answer!")
            except ValueError as e:
                raise e
    
    def guess(self, guess):
        try:
            res = self.__check(guess)
        except ValueError as e:
            print(str(e))
            return
        
        self.__print_response(res)

    def __test_valid(self, word):
        if len(word) != 5:
            raise ValueError("Word length must be five!")
        elif word not in self.word_set:
            raise ValueError("Not an English word!")
        return word in self.word_set

    def __check(self, guess):
        try:
            self.__test_valid(guess)
        except ValueError as e:
            raise e

        self.num_checks += 1

        result = [None for _ in range(5)]
        letter_counts = {}

        for c in self.ans:
            letter_counts[c] = letter_counts.get(c, 0) + 1
    
        # first give all the green and black responses
        for i in range(5):
            if guess[i] == self.ans[i]:
                result[i] = 1
                letter_counts[guess[i]] -= 1
            elif guess[i] not in self.ans:
                result[i] = -1
    
        for i in range(5):
            if result[i] is None:
                if guess[i] in self.ans and letter_counts[guess[i]] >= 1:
                    result[i] = 0
                    letter_counts[guess[i]] -= 1
                else:
                    result[i] = -1
    
        return result
    
    def __print_response(self, res):
        dict = {-1:"\N{black large square}", 0:"\U0001F7E8", 1:"\U0001F7E9"}
        correct = True

        for i in res:
            if i != 1:
                correct = False
            print(dict[i], end="")
        
        if correct:
            print("\nCongrats! ({}/{})".format(self.num_checks, self.max_check))
        else:
            print("\nYou have", self.max_check - self.num_checks, "attempts left!")