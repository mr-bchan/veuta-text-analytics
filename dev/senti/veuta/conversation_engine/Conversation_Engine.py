import collections
import json

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

import dev.senti.veuta.conversation_engine.Preprocessor as cleaner


def load_json(file_name):
    print "Reading file name: " + file_name
    with open(file_name, 'r') as f:
        json_tweets = json.load(f)

    return json_tweets

def save_json(output, file):
    with open(file, 'w') as f:
        json.dump(output, f, ensure_ascii=True)
        print 'Saved filename: ' + file


def parse_json(filename):

    if isinstance(filename, basestring): filename = [filename] # input is a string object --> change to list type

    inputs = []
    df_inputs = pd.DataFrame()

    for input in filename:
        json_tweets = load_json(input)
        print "Number of inputs: " + str(len(json_tweets))
        inputs.extend(json_tweets)

    keys = json_tweets[0].keys()
    for key in keys:
            df_inputs[key] = map(lambda tweet: tweet[key], inputs)

    print "\nTotal Number of inputs: " + str(len(df_inputs))
    return  df_inputs

def save_csv_modeldataframe(modeldataframe, filename="C:\\model_response_mapping.csv"):

    #response_dataframe = modeldataframe.sort_values("models")
    response_dataframe = modeldataframe.ix[:,{0,2}]

    response_dataframe.to_csv(filename, encoding='utf-8', index=False)
    print "Model-Response pairs saved to " + filename
    return


def get_support_count(item):
    return item['message_support']

###########################################################################################################

def build_cluster_labels(features, k=5):
    num_clusters = k
    km = KMeans(n_clusters=num_clusters)

    km.fit(features)
    clusters = km.labels_.tolist()
    return clusters

def build_tfidf_dictionary( inputs, ngram_range, max_features, vocab, min_df, max_df):

    vectorizer = TfidfVectorizer(use_idf=True, tokenizer=cleaner.cleanMePlease, ngram_range=ngram_range,
                                 smooth_idf=True, norm='l2', max_features=max_features,
                                 lowercase=True, encoding='utf-8', vocabulary=vocab, min_df=min_df, max_df=max_df)

    response_vocab_features = vectorizer.fit_transform(inputs).toarray()
    response_vocab = vectorizer.get_feature_names()

    print'\nTF-IDF Dictionary length:' + str(len(response_vocab))
    print response_vocab
    return {"terms": response_vocab, "features":response_vocab_features, 'idf': vectorizer.idf_}

def build_tf_dictionary(inputs, ngram_range, vocab, max_features, binary, min_df, max_df):
    vectorizer = CountVectorizer(tokenizer=cleaner.cleanMePlease, ngram_range=ngram_range,
                                 lowercase=True, encoding='utf-8', binary=binary, vocabulary=vocab, min_df=min_df, max_df=max_df,
                                 max_features=max_features)

    if(vocab is None): vectorizer.fit(inputs)

    response_vocab_features = vectorizer.transform(inputs).toarray()
    response_vocab = vectorizer.get_feature_names()

    print  '\nTF Dictionary length:' + str(len(response_vocab))
    print response_vocab
    return {"terms": response_vocab, "features":response_vocab_features}

def build_modeldataframe(messages, responses, models):

    df_model = pd.DataFrame()

    df_model.insert(loc=0, column='models', value=models)
    df_model.insert(loc=1, column='messages', value=messages)
    df_model.insert(loc=2, column='responses', value=responses)

    return df_model



def build_patterns(modeldataframe, features, terms, model_size, column, threshold=0.05):
    word_patterns = []
    support_list = []

    for model_num in range(model_size):

        terms_list = []
        text_per_model = modeldataframe[modeldataframe['models'] == model_num][column]
        text_per_model_features = features[np.where(modeldataframe['models'] == model_num)]

        # compute for frequency matrix
        freq_matrix = (np.transpose(np.dot(np.transpose(text_per_model_features), np.ones(shape=(len(text_per_model),1)))) / len(text_per_model))[0]

        sorted_freq_idx= np.argsort(freq_matrix)[::-1]
        filtered_freq_idx =  (np.where(freq_matrix > threshold)[0])##output is column names
        freq_idx = sorted_freq_idx[np.in1d(sorted_freq_idx,filtered_freq_idx)]

        for ctr in freq_idx:
                #terms_list.append([terms[ctr], round(freq_matrix[ctr],2)])
                 terms_list.append(terms[ctr])
        word_patterns.append(terms_list)
        support_list.append(round(len(text_per_model) / float(len(modeldataframe)),2))
    return [word_patterns, support_list]

###############################################################################################################################
#  @output variables:
#      - conversation_model:
#           - id: integer identifier
#           - name: name. Default: Model 1, 2,...
#           - type: message type {radar, mention, direct message, etc.}
#           - and_rule: INCLUSION pattern of watch words
#           - not_rule: EXCLUSION pattern of watch words
#           - positive_template: template response for positive sentiment message
#           - neutral_template: template response for neutral sentiment message
#           - negative_template: template response for negative sentiment message --> most common response terms are suggested here!
#           - confidence: confidence threshold set for rule matching and sentiment classification
#           - suggested_response: list of suggested response watchwords

def build_conversation_models(model_size,model_type,message_patterns,response_patterns, confidence, support_threshold):

    if isinstance(model_type, basestring): model_type = [model_type] # input is a string object --> change to list type

    model_list = []


    for ctr in range(model_size):

        if len(message_patterns[0][ctr]) != 0 and len(response_patterns[0][ctr]) != 0 and message_patterns[1][ctr] > support_threshold:
            model = (("id",(ctr+1)),
                 ("label", "Model " + str(ctr+1)),
                 ("type", model_type),
                 ("and_rule", message_patterns[0][ctr]),
                 ("not_rule", []),
                 ("positive_template", None),
                 ("neutral template", None),
                 ("negative template", None),
                 ("suggested_response_words", response_patterns[0][ctr]),
                 ("confidence",confidence),
                 ("message_support", message_patterns[1][ctr]))

            model_list.append(collections.OrderedDict(model))

    model_list.sort(key=get_support_count, reverse=True)
    return  model_list

def build_tokens(message):
    return cleaner.cleanMePlease(message)