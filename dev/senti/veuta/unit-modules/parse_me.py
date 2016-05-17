import  sys

import  dev.senti.veuta.conversation_engine.Preprocessor as cleaner

if __name__ == '__main__':

    if(len(sys.argv) < 2): print 'No input sentence found! :('

    else:
        sentence = sys.argv[1]
        print 'Input sentence: ' + sentence
        print 'Tokens: ' + str(cleaner.cleanMePlease(sentence))
