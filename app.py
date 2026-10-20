import streamlit as st
from llm_agent import ConversationAgent


st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")


if "conversation_agent_object" not in st.session_state:
    st.session_state.conversation_agent_object = ConversationAgent()


user_input = st.chat_input(
    "Que veux tu moussaillon ?",
    accept_file=False,
    accept_audio=False
)

if user_input:
    st.session_state.conversation_agent_object.ask_llm(user_input)


# on affiche tout l'historique, sauf le message "system" (la personnalite)
conversation_agent = st.session_state.conversation_agent_object
for message in conversation_agent.conversation_history[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
