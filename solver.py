import math

class solver:

    def __init__(self):
        self.history = []
        f = open("sgb-words.txt", "r")
        self.word_list = f.read().splitlines()
        self.candidates = [x for x in self.word_list]
        f.close()

    def compare(self, word, ans):
        result = [None for _ in range(5)]
        letter_counts = {}

        for c in ans:
            letter_counts[c] = letter_counts.get(c, 0) + 1
    
        # first give all the green and black responses
        for i in range(5):
            if word[i] == ans[i]:
                result[i] = 1
                letter_counts[word[i]] -= 1
            elif word[i] not in ans:
                result[i] = -1
    
        for i in range(5):
            if result[i] is None:
                if word[i] in ans and letter_counts[word[i]] >= 1:
                    result[i] = 0
                    letter_counts[word[i]] -= 1
                else:
                    result[i] = -1
    
        return result
    
    def receive(self, res, guess):
        # shrink the candidate set according to res
        for cand in self.candidates:
            if res != self.compare(guess, cand):
                self.candidates.remove(cand)
    
    def guess(self):
        max = 0.0
        max_word = ""

        for word in self.candidates:
            ent = self.entropy(word)
            if ent > max:
                max = ent
                max_word = word
                
        self.word_list.remove(max_word)

        return max_word

    def entropy(self, word):
        dict = {}

        for ans in self.candidates:
            res = str(self.compare(word, ans))
            if res in dict:
                dict[res] += 1
            else:
                dict[res] = 1

        total = sum(dict.values())
        entropy = sum([i/total * math.log(total/i, 2.0) for i in dict.values()])
        return entropy