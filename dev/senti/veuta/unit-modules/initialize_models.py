
import dev.senti.veuta.conversation_engine.Analytics_Interface as analytics
import dev.senti.veuta.conversation_engine.Datasets as datasets
import dev.senti.veuta.db_modules.MongoDB_Helper as db_helper


loaded_json = analytics.parse_json(datasets.MCDO_DUMP)

responses = loaded_json['response']
messages = loaded_json['message']

message_dictionary = analytics.generate_dictionary(inputs=messages,
                                                   max_features=1000)

# analytics.save_dictionary(message_dictionary, "C:\\dictionary.json")


models = analytics.initialize_models(messages=messages,
                                     responses=responses,
                                     message_dictionary=message_dictionary,
                                     model_type=['direct', 'radar'],
                                     confidence=0.50,  # default confidence value
                                     model_size=20,  # number of conversation models

                                     watchword_response_confidence=0.20,
                                     watchword_message_confidence=0.05,
                                     support_threshold=0.01)

# analytics.save_json(models, "C:\\conv_model.json")

client = db_helper.initialize_MongoDB()
db_helper.insert_conversation_model(client=client, conversation_models=models, name="mcdo")