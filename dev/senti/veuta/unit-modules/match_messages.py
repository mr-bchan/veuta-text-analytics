import numpy as np

import dev.senti.veuta.conversation_engine.Analytics_Interface as analytics
import dev.senti.veuta.conversation_engine.Datasets as datasets
import dev.senti.veuta.conversation_engine.Scoring_Functions as scores

# [1] Load messages
messages = analytics.parse_json(datasets.MCDO_DUMP)['message']

# [2] Load conversation models
models = analytics.parse_json("C:\\conv_model.json")

# [3] Load dictionary terms
watch_words = analytics.load_json("C:\\dictionary.json")['terms']


matches = analytics.match_messages(messages=messages[120],
                                   models=models,
                                   watch_words=watch_words,
                                   func_scoring=scores.scoring_average_matches,
                                   confidence=0.1); matches

np.array(matches)[([match['id'] > 0 for match in matches])]


[models[models['id'] == match['id']]  for match in matches]
[match['score'] for match in matches]
