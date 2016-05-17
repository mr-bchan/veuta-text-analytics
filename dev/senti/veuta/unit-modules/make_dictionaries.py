import dev.senti.veuta.conversation_engine.Analytics_Interface as analytics
import dev.senti.veuta.conversation_engine.Datasets as datasets
import dev.senti.veuta.db_modules.MongoDB_Helper as mongoDB
#############################################################

db = mongoDB.initialize_MongoDB()


loaded_json = analytics.parse_json(datasets.ALL_DUMP)
responses = loaded_json['response']
messages = loaded_json['message']

file_label = ['mcdo', 'kfc', 'burger_king']

message_dictionary = analytics.generate_dictionary(inputs=messages, max_features=500, name=file_label[2])

# file = 'dict-'+file_label[2] + "-" + str(len(message_dictionary['terms']))

mongoDB.insert_dictionary(client=db, message_dictionary=message_dictionary)

# mongoDB.getCollections(db)
#
# db.get_collection("LDA-watchwords").remove()

db["TermDocumentMatrix"].find_one()