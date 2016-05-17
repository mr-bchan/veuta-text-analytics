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
                      ngram_range=(1,1), max_response_terms=1000, model_size=20, confidence=0.5, csv_filename=None, support_threshold=0.01):

    message_terms = message_dictionary['terms']
    message_features = message_dictionary['features']

## initialize response dictionary

    print "\nBuilding Responses Dictionary."
    response_dictionary = conversation_engine.build_tfidf_dictionary(inputs=responses, max_features=max_response_terms, ngram_range=ngram_range,
                                                                     min_df=1, max_df=1.0, vocab=None)
    response_features = response_dictionary['features']
    response_terms = response_dictionary['terms']

## cluster responses to model_clusters
    model_clusters = conversation_engine.build_cluster_labels(response_features, model_size)
    data_frame_model = conversation_engine.build_modeldataframe(models=model_clusters, messages=messages, responses=responses)

    #optional - save csv to observe correctness of model assignment to the response
    if(csv_filename is not None):
        conversation_engine.save_csv_modeldataframe(data_frame_model, filename=csv_filename)

## generate response patterns from resposne TF dictionary
    response_patterns_dictionary = conversation_engine.build_tf_dictionary(inputs=responses, vocab=response_terms, binary=True, max_features=max_response_terms,
                                                                           min_df=1, max_df=1.0, ngram_range=ngram_range)

    response_patterns = conversation_engine.build_patterns(modeldataframe=data_frame_model, model_size=model_size, terms=response_terms,
                                                           features=response_patterns_dictionary['features'], column="responses",
                                                           threshold=watchword_response_confidence)

## generate message patterns from resposne TF dictionary
    message_patterns = conversation_engine.build_patterns(modeldataframe=data_frame_model, model_size=model_size,
                                                          terms=message_terms, features=message_features, column="messages",
                                                          threshold=watchword_message_confidence)

## build model outputs
    models = conversation_engine.build_conversation_models(model_size = model_size, model_type=model_type, message_patterns=message_patterns, response_patterns=response_patterns,
                                                           confidence=confidence, support_threshold=support_threshold)

    print "\nConversation models successfully generated. " + str(len(models)) + " generated models. \n"

    return models

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