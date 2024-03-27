from SentenceEmbeddings import TextEmbedder

# mongo url path
mongo_url =""

textEmbedder = TextEmbedder(mongo_url)

query = ["What are the most popular imaging techniques used?"]
embeddings = textEmbedder.generate_embeddings(query)

# print(embeddings)

pipeline = [
  {
    '$vectorSearch': {
      'index': 'vector_index',  # vector_index  Inn_Hub_Vect_Index
      'path': 'embedding',
      'queryVector': embeddings[0].embedding,
      'numCandidates': 20,
      'limit': 2
    }
  }, {
    '$project': {
      "_id": 1,
      "text": 1,
      "embedding": 1,
      "page_number": 1,
      "score": { "$meta": "vectorSearchScore" }
    }
  }
]

db = textEmbedder.mongoInit.db
collection = textEmbedder.mongoInit.collection

result = textEmbedder.mongoInit.clientMongo["Inn_hub_db"]["Inn_hub_db_fullpage"].aggregate(pipeline)
print("=======")
# print(result)
context = ""
for i in result:
    context = context + i["text"]
    print(i["page_number"])
    
# print(context)
print("=======")
print(textEmbedder.generate_response_with_context(query[0], context))