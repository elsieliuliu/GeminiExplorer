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

# Main part of the Streamlit app
def main():
    st.title("Gemini Explorer")

    # Add the code to capture the user's name
    user_name = st.text_input("Please enter your name")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.initial_message_sent = False  # Track if initial message was sent

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

    # Check if the user has entered their name and the initial message hasn't been sent
    if user_name and not st.session_state.initial_message_sent:
        # Define the personalized prompt
        personalized_prompt = f"Ahoy {user_name}! I be ReX, yer friendly assistant. Let's set sail on our adventure together! 🦜⚓️"
        
        # Send the personalized prompt
        send_personalized_prompt(personalized_prompt)
        st.session_state.initial_message_sent = True

    # Capture user input
    query = st.chat_input("Gemini Explorer")
    if query:
        with st.chat_message("user"):
            st.markdown(query)
        llm_function(chat, query)

# Run the main part of the app
if __name__ == "__main__":
    main()