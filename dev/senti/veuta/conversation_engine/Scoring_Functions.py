
import numpy as np

def scoring_average_matches(tokens, patterns):

    # copmute message matches = number of matches in the message / length of message tokens
    message_matches = [len(np.array(tokens)[np.in1d(tokens, pattern)]) / float(len(tokens)) for pattern in patterns]

    # compute pattern matches = number of matches in the pattern / length of pattern tokens
    pattern_matches = [len(np.array(pattern)[np.in1d(pattern, tokens)]) / float(len(pattern)) for pattern in patterns]

    # calculate score as average of message matches and pattern matches
    scores = np.divide(np.add(message_matches, pattern_matches), float(2))

    return scores
