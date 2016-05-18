
import dev.senti.veuta.db_modules.MongoDB_Helper as db_helper

client = db_helper.initialize_MongoDB()

db_helper.getCollections(client)

client.get_collection('LDA-watchwords').count()

client.get_collection('LDA-watchwords').find()[1]


from pymongo import MongoClient

uri = "mongodb://testdbuser:testdbabcd51234e@dev.mongo1.veuta.com:27017/?authSource=testdb"

client = MongoClient(uri)
db = client['testdb']

db['watch_words_classifications'].find()[0]
db.collection_names()
data = db.twitter_public_test.find() # sample public feed
#data = db.twitter_direct_test.find() # sample direct messages