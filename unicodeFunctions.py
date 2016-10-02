#See this link for unicode explanation (Specifically, read about "Unicode Sandwich")
    #http://nedbatchelder.com/text/unipain.html

import sys

#used to convert byte strings to unicode (used for inner workings)
def toUnicode(txt):
    return txt.decode("utf-8", errors='ignore')
def utf8(txt):
    return txt.encode(sys.stdout.encoding, errors='ignore')