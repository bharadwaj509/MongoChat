import streamlit as st
from SentenceEmbeddings import TextEmbedder


# Simple chatbot logic
def get_bot_response(user_message, textEmbedder):
    query = ["What are the most popular imaging techniques used?"]
    embeddings = textEmbedder.generate_embeddings(query)

    # print(embeddings)

    pipeline = [
        {
            '$vectorSearch': {
            'index': 'Inn_Hub_Vect_Index',
            'path': 'embedding',
            'queryVector': embeddings[0].embedding,
            'numCandidates': 20,
            'limit': 5
            }
        }, {
            '$project': {
            "_id": 1,
            "text": 1,
            "embedding": 1,
            "score": { "$meta": "vectorSearchScore" }
            }
        }
    ]


    result = textEmbedder.mongoInit.clientMongo["Inn_hub_db"]["Inn_hub_col"].aggregate(pipeline)

    # print(result)
    context = ""
    for i in result:
        context = context + i["text"]
        print(i["text"])
    print(context)
    print("=======")
    print(textEmbedder.generate_response_with_context(query[0], context))

    return "Hello"




# Streamlit app layout
st.title("Simple Chatbot")

user_input = st.text_input("You: ", "")

if user_input:
    response = get_bot_response(user_input, textEmbedder)    
    st.text_area("Chatbot:", value=response, height=100, max_chars=None, key=None)
