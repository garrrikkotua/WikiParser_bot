from collections import Counter
from statistics import mean, stdev
import pickle
from collections import defaultdict

"""
This class performs 
stats operations for the bot
"""


class Stats:
    @staticmethod
    def top(self, c, n, how):
        c = self.delete_stops(self, c)
        if how == 'dsc':
            return c.most_common(n)
        if how == 'asc':
            return c.most_common()[:-n - 1:-1]

    @staticmethod
    def make_counter(self, chat_id):
        path_t = 'texts{}.txt'.format(chat_id)
        path_c = 'counter{}.txt'.format(chat_id)
        with open(path_t, 'r', encoding='utf-8') as f:
            c = Counter()
            for line in f:
                c.update(line.split())
        with open(path_c, 'wb') as f1:
            pickle.dump(c, f1)

    @staticmethod
    def get_counter(self, chat_id):
        path_c = 'counter{}.txt'.format(chat_id)
        with open(path_c, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def stop_words(self, c):
        m = mean(c.values())
        std = stdev(c.values())
        left = m - 3 * std
        right = m + 3 * std
        l = []
        for a, b in c.items():
            if b < left or b > right:
                l.append(a)
        return l

    @staticmethod
    def delete_stops(self, c):
        stop = self.stop_words(self, c)
        d = Counter({i: c[i] for i in stop})
        c = c - d
        return c

    @staticmethod
    def words_near(self, chat_id, word):
        path_m = 'model{}.txt'.format(chat_id)
        with open(path_m, 'rb') as file:
            d = pickle.load(file)
            next_words = d[word]
        return sorted(next_words.items(), key=lambda x: x[1],
                      reverse=True)

    @staticmethod
    def dist_by_sentence(self, chat_id, word):
        d = defaultdict(lambda: 0)
        path_t = 'texts{}.txt'.format(chat_id)
        with open(path_t, 'r') as f:
            for line in f:
                if word in line.split():
                    i = line.split().index(word)
                    d[i] += 1
        return dict(d)
