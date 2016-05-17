
# Input - tweet response string format -> ['word1 word2 word3 word4 ...]
# Output - preprocessed response in unigram format -> [word1, word2, word3, word4, ...]

import re

import stop_words as stop
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

#get stopwords from stop_words package and provide additional stop words
additional_stop_words = ['hello', 'hi', 'just', 'can', 've', 'll', 'nt','get', 'got', 'shall','still', 'didn', 'aren', 're', 'don', 'isn', 'please','us', 'ain\'t','th',
                         'will']
stop_words = stop.get_stop_words('english')
stop_words.extend(additional_stop_words)

emoticons_str = r"""
    (?:
        [X:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:[\w_d]+[.|\w_d]*@[\w_d]+.[\w_d]+[.[\w_d]+]*)', #email address
    r'(?:\\u[\wd_]+[\\u[\wd_]+]*)',  # emojis in unicode format
    r'(?:\\x[\wd_]+[\\x[\wd_]+]*)',  # emojis in unicode format
    r'(?:\\\w)',  # escape characters
    r'(?:@[\w_]+)', # @-mentions
    r'(?:&[\w_]+)',  # &-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z\-_\']+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)

def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)

def lemmatize(word):
    return wordnet_lemmatizer.lemmatize(word)

def tokenize(s):
    tokens_re.findall(s)
    return tokens_re.findall(s)

def clean_tokens(tokens):

    clean_tokens = []

    for token in tokens:

        if(token[0:2] == '\U'): # emoji unicode format
            clean_tokens.append('<emoji:'+ token + '>')

        if token[0] == '@' or token[0] == '&' or token[0] == '\\' : #mentions and escape characters
            continue

        if len(token) == 1: #one word, punctuation marks
            continue

        if token[0] == 'a' and hasNumbers(token[1]):
            continue

        if hasNumbers(token[0]) == True: #remove words with starting numbers
            continue

        if token in stop_words: #remove other stop words
            continue

        if(token[len(token)-1] == '.'):
            token = token[0:len(token)-1]
            clean_tokens.append(token.lower())

        else:
          token = lemmatize(token.decode('utf-8'))
          clean_tokens.append(token.lower())

    return clean_tokens

def cleanMePlease(tweet):

    tweet = tweet.encode('unicode_escape')

    tokens = tokenize(tweet)

    tokens = clean_tokens(tokens)

    return tokens


