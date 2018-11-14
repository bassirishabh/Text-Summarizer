from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import sys
import os
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
print(sys.argv)
SENTENCES_COUNT = int(sys.argv[1])
path_name = sys.argv[2]
filename = str(sys.argv[3])
path = str(sys.argv[4])
dire = str(sys.argv[5])

if __name__ == "__main__":
    #url = "http://www.zsstritezuct.estranky.cz/clanky/predmety/cteni/jak-naucit-dite-spravne-cist.html"
    #parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    parser = PlaintextParser.from_file(path_name, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    fp = open(os.path.join(os.path.join(path,dire),'summary.txt'), 'w')
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(type(sentence))
        print(sentence)
        fp.write(str(sentence) + "\n")
    fp.close()
