import numpy as np

import dev.senti.veuta.conversation_engine.Preprocessor as cleaner


def __match_message__(message, models, func_scoring, watch_words, confidence):

    EMPTY_MATCH = {}

    tokens = np.array(cleaner.cleanMePlease(message))

    watch_words_list = np.array(watch_words)[np.in1d(watch_words,tokens)]

    #[1] check if token list is not empty
    if len(tokens) is 0: return EMPTY_MATCH

    not_patterns = models['not_rule']
    not_pattern_matches = [len(tokens[np.in1d(tokens, not_pattern)]) is 0 for not_pattern in not_patterns]

    #remove models having no matches with its NOT pattern
    models = models[not_pattern_matches]

    #[2] check if model list is not empty
    if len(models) is 0: return  EMPTY_MATCH

    patterns = models['and_rule']; [np.array(pattern)[np.in1d(pattern,tokens)] for pattern in patterns]

    scores = func_scoring(tokens, patterns)

    candidate_scores = np.sort(scores)[::-1]
    candidate_idxs =   np.argsort(scores)[::-1]

    #[3] check if  matches are found
    if candidate_scores[0] is  0 or candidate_scores[0] <= confidence: return EMPTY_MATCH

    matched_pattern = models.loc[candidate_idxs[0]]["and_rule"]
    matched_words = np.array(matched_pattern)[np.in1d(matched_pattern, tokens)]

    return {"model": models.loc[candidate_idxs[0]] ,
            "match_confidence": round(candidate_scores[0],2),
            "matched_watchwords" : matched_words,
            "tokens" : tokens,
            'watchwords' : watch_words_list}


def match_messages(messages, models, watch_words, confidence, func_scoring):
    match_models = []
    if isinstance(messages, basestring): messages = [messages] # input is a string object --> change to list type

    for message in messages:
        match = __match_message__(message=message,
                                      models=models,
                                      watch_words=watch_words,
                                      confidence=confidence,
                                      func_scoring=func_scoring)
        if len(match) is 0:
            model_id = -99
            model_name = ""
            score = 0
            matches = []
            tokens = []
            watch_words_list = []

        else:
            model_id = match['model']['id']
            score = match['match_confidence']
            matches = match['matched_watchwords']
            tokens = match['tokens']
            watch_words_list = match['watchwords']
            model_name = match['model']['name']

        match_models.append({"id" : model_id,
                             "score" : score,
                             "matched_watchwords": matches,
                             "message": message,
                             "watchwords" : watch_words_list,
                             "tokens" : tokens,
                             "name" : model_name})

    return match_models
