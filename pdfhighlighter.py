import streamlit as st
import fitz
from SentenceEmbeddings import TextEmbedder

st.set_page_config(layout="wide")

styl = f"""
<style>
    .stTextInput {{
      position: fixed;
      bottom: 3rem;
    }}
</style>
"""
st.markdown(styl, unsafe_allow_html=True)

# Load the PDF file
original_doc = "intro.pdf"
page_number = "2"
text_lookup = "While the healthcare costs have been constantly rising, the quality of care provided to the pa- tients in the United States have not seen considerable improvements."


mongo_url ="mongodb+srv://bobberrider509:Mymongomywish@cluster0.abminxx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
textEmbedder = TextEmbedder(mongo_url)


col1, col2 = st.columns([1,1])


def get_bot_response(query, textEmbedder):
    # query = ["What are the most popular imaging techniques used?"]
    embeddings = textEmbedder.generate_embeddings([query])

    # print(embeddings)

    pipeline = [
        {
            '$vectorSearch': {
            'index': 'vector_index',
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
            "page_number": 1,
            "score": { "$meta": "vectorSearchScore" }
            }
        }
    ]


    result = textEmbedder.mongoInit.clientMongo["Inn_hub_db"]["Inn_hub_fullpage_split"].aggregate(pipeline)

    # print(result)
    context = ""
    page_numbers = []
    top_result = []
    for i in result:
        top_result.append(i["text"])
        context = context + i["text"]
        print(i["text"])
        page_numbers.append(i["page_number"])
    # print(context)
    print("=======")
    response = textEmbedder.generate_response_with_context(query[0], context)
    # print(response)
    return response, top_result[0], page_numbers[0]

with col1:
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
        response, context, page_number = get_bot_response(query=prompt, textEmbedder=textEmbedder)
        # Display assistant response in chat message container

        original_doc = "intro.pdf"
        text_lookup = context

        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})       

with col2:
    if original_doc:
        with fitz.open(original_doc) as doc:
            # Rest of the code goes here
            print(original_doc, page_number)
            page = doc.load_page(int(page_number) - 1)
            # text_lookup = "Examples of such signals include the electroneu- rogram (ENG), electromyogram (EMG), electrocardiogram (ECG), electroencephalogram (EEG), electrogastrogram (EGG), phonocardiogram (PCG), and so on"
            if text_lookup:
                areas = page.search_for(text_lookup)

                for area in areas:
                    page.add_rect_annot(area)

                pix = page.get_pixmap(dpi=120).tobytes()
                st.image(pix, use_column_width=True)




# with st.sidebar:
#     text_lookup = st.text_input("Look for", max_chars=50)

#     if original_doc:
#         with fitz.open(original_doc) as doc:
#             for page_number in range(doc.page_count):
#                 page = doc.load_page(page_number)
#                 if text_lookup:
#                     areas = page.search_for(text_lookup)
#                     for area in areas:
#                         page.add_rect_annot(area)
#                     pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
#                     st.image(pix, use_column_width=True)   

# if original_doc:
#     with fitz.open(original_doc) as doc:
#         page_number = st.sidebar.number_input(
#             "Page number", min_value=1, max_value=doc.page_count, value=1, step=1
#         )
#         page = doc.load_page(page_number - 1)
#         if text_lookup:
#             areas = page.search_for(text_lookup)
#             for area in areas:
#                 page.add_rect_annot(area)
#             pix = page.get_pixmap(dpi=120).tobytes()
#             st.image(pix, use_column_width=True)

# with st.sidebar:
#     original_doc = st.file_uploader(
#         "Upload PDF", accept_multiple_files=False, type="pdf"
#     )
#     text_lookup = st.text_input("Look for", max_chars=50)


# if original_doc:
#     with fitz.open(stream=original_doc.getvalue()) as doc:
#         page_number = st.sidebar.number_input(
#             "Page number", min_value=1, max_value=doc.page_count, value=1, step=1
#         )
#         page = doc.load_page(page_number - 1)

#         if text_lookup:
#             areas = page.search_for(text_lookup)

#             for area in areas:
#                 page.add_rect_annot(area)

#             pix = page.get_pixmap(dpi=120).tobytes()
#             st.image(pix, use_column_width=True)
                    


# the most popular imaging techniques used in biomedical                    