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
SENTENCES_COUNT = 10


if __name__ == "__main__":
    #url = sys.argv[1]
    #parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    parser = PlaintextParser.from_file("D:\Projects\story.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    #fp = open(os.path.join(os.path.join(path,dire),'summary.txt'), 'w')
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        #print(type(sentence))
        print(sentence)
        #fp.write(str(sentence) + "\n")
    #fp.close()
