import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "elsiegeminiexplorer"
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    temperature=0.4,
    top_k=40,
    top_p=0.9
)

model = GenerativeModel(
    "gemini-pro",
    generation_config = config,
    
)

chat = model.start_chat()

st.title('Gemini Explorer Chat')

user_input = st.text_input("Type your message:")

if st.button('Send'):
    if user_input:
        response = chat.send_message(user_input)
        st.text_area("Response:", value=response.candidates[0].content.parts[0].text, height=300)
    else:
        st.write("Please type a message to send.")

