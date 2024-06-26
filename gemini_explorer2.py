import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = "elsiegeminiexplorer"
vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

model = GenerativeModel(
    "gemini-pro",
    generation_config=config   
)

chat = model.start_chat()

# Helper function to display and send Streamlit messages
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

# Function to send the personalized prompt
def send_personalized_prompt(prompt):
    st.write(prompt)
    st.session_state.initial_message_sent = True  # Update state to reflect message sent

# Main part of the Streamlit app
def main():
    st.title("Gemini Explorer")

    # Check if the user's name is already stored; if not, ask for it
    if "user_name" not in st.session_state or not st.session_state.user_name:
        st.session_state.user_name = st.text_input("Ahoy, what's your name?", key="user_name_input")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.initial_message_sent = False

    # Display and load chat history
    for index, message in enumerate(st.session_state.messages):
        content = Content(
            role=message["role"],
            parts=[Part.from_text(message["content"])]
        )

        if index != 0:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        chat.history.append(content)

    # If name is entered and initial message not sent, send personalized prompt
    if st.session_state.user_name and not st.session_state.initial_message_sent:
        personalized_prompt = f"Ahoy {st.session_state.user_name}! I be ReX, yer friendly assistant. Let's set sail on our adventure together! 🦜⚓️"
        send_personalized_prompt(personalized_prompt)

    # Capture user input
    query = st.chat_input("Gemini Explorer")
    if query:
        with st.chat_message("user"):
            st.markdown(query)
        llm_function(chat, query)

# Run the main part of the app
if __name__ == "__main__":
    main()
