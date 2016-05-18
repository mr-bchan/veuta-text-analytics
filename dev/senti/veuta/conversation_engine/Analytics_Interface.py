#######################################################################
## Veuta Text Analytics Engine Team
## @Conversation Engine Module Source Code
#######################################################################

import dev.senti.veuta.conversation_engine.Conversation_Engine as conversation_engine
import dev.senti.veuta.conversation_engine.Message_Matcher as matcher
import dev.senti.veuta.conversation_engine.Scoring_Functions as scorers

#####################################################
# JSON Helper Functions
#####################################################
def save_json(output, file): return conversation_engine.save_json(output, file)
def parse_json(file): return conversation_engine.parse_json(file)
def load_json(file): return conversation_engine.load_json(file)
#####################################################
# @input variables:
#     - message: array of text under 'message' key
#     - ngram_range: (1,1) for unigram; (1,2) for bigrams etc...
#     - max_features: max number of terms in dictionary
#
#  @output variables:
#      - terms: unique terms in the watch word dictionary
#      - features: transformed feature vectors (term-frequency) of input text
#
#[1] generate initial watch word dictionary and tf-feature vectors from scraped data -----> topic modelling module
def generate_dictionary(inputs, max_features=None, ngram_range=(1, 1), min_df=1, max_df=1.0, vocab=None, binary=False, name="Default Dictionary Name"):

    output_dictionary = conversation_engine.build_tf_dictionary(inputs=inputs, ngram_range=ngram_range,
                                                                max_features=max_features, vocab=vocab, min_df=min_df, max_df=max_df, binary=binary)
    initial_terms = output_dictionary['terms']
    initial_features = output_dictionary['features']
    return {"terms" : initial_terms, "features": initial_features, "name" : name}

#####################################################
# @input variables:
#     - messages: array of text under 'message' key
#     - message terms = initialized message terms from initial watch word generation
#     - message features - TF counts of message terms
#     - responses: array of text under 'response' key
#     - ngram_range: (1,1) for unigram; (1,2) for bigrams etc...
#     - max_response_terms: maximum number of terms in response dictionary
#     - model_size: number of models --> paramater in k-means clustering algorithm
#     - model_type: {radar, mention, direct etc., }
#     - watchword_confidence: threshold set for the inclusion of a watchword to the message or response pattern
#     - confidence: confidence threshold set for rule matching and sentiment classification
#
#  @output variables:
#      - conversation_model:
#           - id: integer identifier
#           - name: name. Default: Model 1, Model 2,...
#           - type: message type {radar, mention, direct message, etc.}
#           - and_rule: INCLUSION pattern of watch words
#           - not_rule: EXCLUSION pattern of watch words
#           - positive_template: template response for positive sentiment message
#           - neutral_template: template response for neutral sentiment message
#           - negative_template: template response for negative sentiment message --> most common response terms are suggested here!
#           - confidence: confidence threshold set for rule matching and sentiment classification
#           - suggested_response: list of suggested response watchwords based on input responses
#           - message_support: number of messages belonging in the clustered response template
# [2] generate conversation models from response inputs ** PER conversation model type**
def initialize_models(messages, message_dictionary, responses, model_type, watchword_message_confidence=0.10, watchword_response_confidence=0.20,
                      ngram_range=(1,1), max_response_terms=1000, model_size=20, confidence=0.5, support_threshold=0.01):
    return conversation_engine.initialize_models(messages=messages, message_dictionary=message_dictionary, responses=responses, model_type=model_type,
                                                 watchword_message_confidence=watchword_message_confidence, watchword_response_confidence=watchword_response_confidence,
                                                 ngram_range=ngram_range, max_response_terms=max_response_terms, model_size=model_size,
                                                 confidence=confidence, support_threshold=support_threshold)

#####################################################
# @input variables:
#   - message: input raw messages (message text or collections)
#   - models: list of conversation models
#   - watch_words: watchword dictionary terms
#   - func_scoring: scoring for computing similarity
#   - confidence: confidence set to filter out matches with lower scores. DEFAULT-0.00

# @output variables:
#   - matched_watchwords: list of words in the message which matches the model pattern
#   - id: conversation model ID
#   - message: raw message text
#   - score: computed similarity score

def match_messages(messages, models, watch_words, func_scoring = scorers.scoring_average_matches, confidence=0):
    return matcher.match_messages(messages=messages, models=models, watch_words=watch_words, func_scoring=func_scoring, confidence=confidence)

def tokenize(s):
    s = s.lower()
    return conversation_engine.build_tokens(s)

def save_dictionary(dictionary, filename):
    new_dict = dictionary.copy()
    new_dict['features'] = new_dict['features'].tolist()
    save_json(new_dict, filename)