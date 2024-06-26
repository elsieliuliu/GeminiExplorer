import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "elsiegeminiexplorer"
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

model = GenerativeModel(
    "gemini-pro",
    generation_config = config   
)

chat = model.start_chat()

#helper function to display and send streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

st.title("Gemini Explorer")

# Capture user name
user_name = st.text_input("May I know your name?")

#Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.initial_message_sent = False
    

#Display and load to chat history

for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message["role"],
        parts=[ Part.from_text(message["content"])]
    )

    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat.history.append(content) 

#for initial message startup

if user_name and not st.session_state.initial_message_sent:
    personalized_prompt = f"Your name is Rex, an assistant powered by Google Gemini. You greeting the user by {user_name}. And use emojis to be interactive"
    llm_function(chat, personalized_prompt)
    st.session_state.initial_message_sent = True

#capturer user input
query = st.chat_input("Gemini Explorer")
if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)
