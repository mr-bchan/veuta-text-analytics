
import dev.senti.veuta.db_modules.MongoDB_Helper as db_helper

client = db_helper.initialize_MongoDB()

db_helper.getCollections(client)

client.get_collection('LDA-watchwords').count()

client.get_collection('LDA-watchwords').find()[1]

