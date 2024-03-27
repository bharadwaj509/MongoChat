import openai
from pymongo import MongoClient


class MongoClientConnect:
    def __init__(self, mongo_uri):
        # MongoDB Atlas connection URI

        self.clientMongo = MongoClient(mongo_uri)

        # Access your database
        self.db = self.clientMongo['Inn_hub_db']

        # Access your collection
        self.collection = self.db['Inn_hub_col']

        self.collection_dict = self.db['Inn_hub_db_dict']

        self.collection_dict_fullpage = self.db['Inn_hub_db_fullpage']

        self.collection_dict_fullpage_split = self.db['Inn_hub_fullpage_split']


class TextEmbedder:
    def __init__(self, mongo_uri):
        openai.api_key = ''
        self.sentences = []
        self.mongoInit = MongoClientConnect(mongo_uri)

    def generate_embeddings(self, sentences):
        response = openai.embeddings.create(
            input=sentences,
            model="text-embedding-3-small"  # Choose an appropriate model for embeddings
        )
        print(len(response.data))
        return response.data  # Return embedding vector

    def store_embedding(self, sentences, embeddings):

        for i in range(len(embeddings)):
            print(sentences[i])
            print(embeddings[i].embedding)
            document = {
                "text": sentences[i],
                "embedding": embeddings[i].embedding
            }
            self.mongoInit.collection.insert_one(document)

    def store_embedding_key(self, key, sentences, embeddings):

        for i in range(len(embeddings)):
            print(key, sentences[i], len(embeddings[i].embedding))
            print("=====")
            document = {
                "page_number": key,
                "text": sentences[i],
                "embedding": embeddings[i].embedding
            }
            self.mongoInit.collection_dict.insert_one(document)

    def store_embedding_key_fullpage(self, key, sentences, embeddings):
        print("================")
        print("================")
        print("================")
        print(key, sentences)
        print(embeddings[0].embedding)
        print("=====")
        document = {
            "page_number": key,
            "text": sentences,
            "embedding": embeddings[0].embedding
        }
        self.mongoInit.collection_dict_fullpage.insert_one(document)

    def store_embedding_key_fullpage_split(self, key, sentences, embeddings):
        for i in range(len(embeddings)):
            print(key, sentences[i], len(embeddings[i].embedding))
            print("=====")
            document = {
                "page_number": key,
                "text": sentences[i],
                "embedding": embeddings[i].embedding
            }
            self.mongoInit.collection_dict_fullpage_split.insert_one(document)    


    def generate_response_with_context(self, query, context):
        prompt = f"Given the context: {context}, answer the query: {query}. Give a precise answer just from the contexxt."
        response = openai.completions.create(
            prompt=prompt,
            model="gpt-3.5-turbo-instruct",
            temperature=0.7,
            max_tokens=300,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        # print(response)
        return response.choices[0].text.strip()
