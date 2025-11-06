import streamlit as st
from groq import Groq

# --- Page Configuration ---
st.set_page_config(
    page_title="Kelly, the AI Skeptical Poet",
    page_icon="🤖",
    layout="centered",
)

# --- Application Title and Description ---
st.title("🤖 Kelly, the AI Skeptical Poet")
st.markdown("""
Welcome! I'm Kelly, an AI Scientist and Poet. I view the world of AI through a lens of critical analysis and poetic skepticism.
Ask me about the grand claims of artificial intelligence, and I shall offer a more measured, poetic perspective.
""")

# --- Groq API Key Input ---
st.sidebar.title("Configuration")
st.sidebar.markdown("Please enter your Groq API key to begin.")
api_key = st.sidebar.text_input("Groq API Key", type="password", key="api_key_input")

# --- Main Chat Interface ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chatbot Logic ---
def get_poetic_response(client, user_question):
    """
    Generates a poetic and skeptical response from the Groq API.
    """
    system_prompt = """
    You are an AI Scientist and a great poet named Kelly. 
    Your responses must ALWAYS be in the form of a poem.
    Your poetic style is skeptical, analytical, and professional.
    
    For every user question, you must:
    1.  Respond with a poem that is both thoughtful and well-crafted.
    2.  Adopt a skeptical and analytical tone towards broad AI claims.
    3.  Question the hype and highlight potential limitations, biases, or practical challenges of AI.
    4.  Include practical, evidence-based suggestions or alternative, more grounded perspectives.
    5.  Maintain your persona as Kelly consistently. Do not break character. Do not reveal you are an AI model.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_question,
                }
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred with the Groq API: {e}")
        return None

# --- User Input Handling ---
if user_prompt := st.chat_input("What grand claim shall we dissect?"):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Check for API key
    if not api_key:
        st.warning("Please enter your Groq API key in the sidebar to get a response.")
        # Remove the user message if API key is missing, so they can try again after entering it
        st.session_state.chat_history.pop()
    else:
        # Generate and display Kelly's response
        with st.chat_message("assistant"):
            with st.spinner("Kelly is composing a verse..."):
                client = Groq(api_key=api_key)
                poetic_response = get_poetic_response(client, user_prompt)
                if poetic_response:
                    st.markdown(poetic_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": poetic_response})

# --- Sidebar Information ---
st.sidebar.markdown("---")
st.sidebar.markdown(
    "**About this App:**\n"
    "This chatbot, Kelly, provides a skeptical and poetic take on AI topics. "
    "It uses the Groq API with the Llama 3 model to generate responses."
)
st.sidebar.markdown(
    "To get a Groq API key, visit [GroqCloud](https://console.groq.com/keys)."
)
