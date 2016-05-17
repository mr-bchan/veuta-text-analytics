
import dev.senti.veuta.conversation_engine.ConversationEngine as conversation_engine

#=========================================================#
kfc_dump = "C:\\@KFC_UKI-dump-1033 tweets-sample.json"
mcdo_dump = "C:\\@mcdonaldsuk-dump-1420 tweets-sample.json"
bk_dump = "C:\\@BurgerKingUK-dump-983 tweets-sample.json"

all_dump = [kfc_dump, mcdo_dump, bk_dump]
#############################################################

loaded_json = conversation_engine.parse_json(bk_dump)
responses = loaded_json['response']
messages = loaded_json['message']

message_dictionary = conversation_engine.generate_dictionary(message=messages, max_features=2000, ngram_range=(1,1))

models = conversation_engine.initialize_models(messages=messages, message_dictionary=message_dictionary,
                                               max_response_terms=500, ngram_range=(1, 1),
                                               model_type=['radar', 'mention', 'direct'], responses=responses, confidence=0.50,
                                               model_size=30, watchword_message_confidence=0.05, watchword_response_confidence=0.2)

conversation_engine.save_json(models, "C:\\BKING_conversation_model.json")

