import streamlit as st
from llm_agent import ConversationAgent


class UserInterface:
    def __init__(self):
        pass

    def run(self):
        st.set_page_config(page_title="Jarvis")
        st.title("Barbe-Quasar")

        # l'agent (et donc sa memoire) est cree une seule fois par session
        if "conversation_agent_object" not in st.session_state:
            st.session_state.conversation_agent_object = ConversationAgent()

        # on n'affiche pas le message "system" (la personnalite)
        conversation_agent = st.session_state.conversation_agent_object
        for message in conversation_agent.conversation_history[1:]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        user_input = st.chat_input(
            "Que veux tu moussaillon ?",
            accept_file=False,
            accept_audio=False
        )

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)

            response = conversation_agent.ask_llm(user_input)

            with st.chat_message("assistant"):
                st.markdown(response)


if __name__ == "__main__":
    user_interface = UserInterface()
    user_interface.run()
