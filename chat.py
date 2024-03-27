import streamlit as st
from SentenceEmbeddings import TextEmbedder


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
    response = textEmbedder.generate_response_with_context(query[0], context)
    print(response)
    return response




st.title("Echo Bot")

mongo_url ="mongodb+srv://bobberrider509:Mymongomywish@cluster0.abminxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
textEmbedder = TextEmbedder(mongo_url)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call get_bot_response method to get the response
    response = get_bot_response(prompt, textEmbedder)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})