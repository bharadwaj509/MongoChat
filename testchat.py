import streamlit as st

# Inject custom CSS to set the width of the sidebar
# st.markdown(
#     """
#     <style>
#     [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
#     width: 1000px;
#     }
#     [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
#     width: 500px;
#     margin-left: -1000px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Example sidebar content
# st.sidebar.header("This is the sidebar")
# st.sidebar.text("This is some text in the sidebar")

# # Example main content
# st.header("This is the Main Content Area")
# st.text("This is some text in the main content area")


# import streamlit as st
# from streamlit_float import *
# st.set_page_config(layout="wide")
# float_init(theme=True, include_unstable_primary=False)

# def chat_content(role):
#     st.session_state['contents'].append({"role": role, "content": st.session_state.content})

# if 'contents' not in st.session_state:
#     st.session_state['contents'] = []
#     border = False
# else:
#     border = True

# col1, col2 = st.columns([1,1])
# with col1:
#     # with st.container(border=True):
#     st.write('Hello streamlit')

# with col2:
#     with st.container():
#         with st.container():
#             prompt = st.chat_input(key='content', on_submit=chat_content) 
#             button_b_pos = "0rem"
#             button_css = float_css_helper(width="2.2rem", bottom=button_b_pos, transition=0)
#             float_parent(css=button_css)
#         with st.chat_message("user"):
#             st.write(prompt)
#         if content:=st.session_state.content:
#             with st.chat_message("assistant"):
#                 for c in st.session_state.contents:
#                     st.write(c)


import streamlit as st
from streamlit_chat import message
########################################________LANGCHAIN________####################
import os

def chatquery(payload):
    return "hello"

st.set_page_config(
    page_title="Assistant",
    page_icon=":robot:"
)

st.header("Welcome to Assistant")

# state to hold generated output of llm
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

# state to hold past user messages
if 'past' not in st.session_state:
    st.session_state['past'] = []

# streamlit text input
def get_text():
    input_text = st.text_input("Input Message: ","", key="input")
    return input_text 

user_input = get_text()

# check if text input has been filled in
if user_input:
    # run langchain llm function returns a string as output
    output = chatquery({
        "inputs": {
            "past_user_inputs": st.session_state.past,
            "generated_responses": st.session_state.generated,
            "text": user_input,
        },"parameters": {"repetition_penalty": 1.33},
    })

    # append user_input and output to state
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# If responses have been generated by the model
if st.session_state['generated']:
    # Reverse iteration through the list
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        # message from streamlit_chat
        message(st.session_state['past'][::-1][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][::-1][i], key=str(i))

# I would expect get_text() needs to be called here as a callback
# But i have issues with retreving user_input