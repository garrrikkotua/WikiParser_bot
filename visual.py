from wordcloud import WordCloud
from matplotlib import pyplot as plt
from io import BytesIO

"""
This class performs operations 
to make graphs, wordcloud for the bot
"""


class Visual:
    @staticmethod
    def cloud(self, freq, colormap):
        wc = WordCloud(
           colormap=colormap).generate_from_frequencies(freq)
        image = wc.to_image()
        bio = BytesIO()
        image.save(bio, 'PNG')
        bio.seek(0)
        return bio

    @staticmethod
    def word_dist(self, c):
        freq = sorted(list(c.values()), reverse=True)
        ranks = list(range(1, len(freq) + 1))
        plt.title("Word Frequencies")
        plt.ylabel("Total Number of Occurrences")
        plt.xlabel("Rank of words")
        plt.loglog(ranks, freq, basex=10)
        plt.grid()
        plt.legend()
        image = BytesIO()
        plt.savefig(image, format='PNG')
        plt.close()
        image.seek(0)
        return image

    @staticmethod
    def word_lens(self, c):
        lens = [len(i) for i in c.keys()]
        lens.sort(reverse=True)
        ranks = list(range(1, len(lens) + 1))
        plt.title("Word Lengths")
        plt.ylabel("Length")
        plt.xlabel("Rank of words")
        plt.loglog(ranks, lens, basex=10)
        plt.grid()
        plt.legend()
        image = BytesIO()
        plt.savefig(image, format='PNG')
        plt.close()
        image.seek(0)
        return image

    @staticmethod
    def word_rank(self, c, word):
        freq = sorted(list(c.values()), reverse=True)
        ranks = list(range(1, len(freq) + 1))
        word_freq = c[word]
        word_rank = ranks[freq.index(word_freq)]
        plt.title("Info about {}".format(word))
        plt.ylabel("Total Number of Occurrences")
        plt.xlabel("Rank of words")
        plt.loglog(ranks, freq, basex=10)
        plt.plot(word_rank, word_freq, 'r*',
                 label='{}\'s frequency is {}\n its rank is {}'.format(
                     word, word_freq, word_rank
                 ))
        plt.grid()
        plt.legend()
        image = BytesIO()
        plt.savefig(image, format='PNG')
        plt.close()
        image.seek(0)
        return image

    @staticmethod
    def dist_by_sentence(self, d, word):
        plt.title('Distribution of {}\'s'
                  ' positions in sentences'.format(word))
        plt.ylabel("Number of Occurrences")
        plt.xlabel("Position in sentence")
        pos = sorted(d.keys())
        occur = [d[i] for i in pos]
        plt.plot(pos, occur)
        plt.plot(pos, occur, 'r*')
        plt.grid()
        plt.legend()
        image = BytesIO()
        plt.savefig(image, format='PNG')
        plt.close()
        image.seek(0)
        return image
