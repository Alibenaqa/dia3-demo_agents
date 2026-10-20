import streamlit as st
from llm_agent import ConversationAgent
from speech_to_text import SpeechToText


class UserInterface:
    def __init__(self):
        st.set_page_config(page_title="Jarvis")
        st.title("Barbe-Quasar")
        self.conversation_agent_object = (
            self.get_persistant_conversation_agent()
        )
        self.speech_to_text_object = self.get_persistant_speech_to_text()

    def get_persistant_conversation_agent(self):
        if "conversation_agent_object" not in st.session_state:
            st.session_state.conversation_agent_object = ConversationAgent()

        return st.session_state.conversation_agent_object

    def get_persistant_speech_to_text(self):
        if "speech_to_text_object" not in st.session_state:
            st.session_state.speech_to_text_object = SpeechToText()

        return st.session_state.speech_to_text_object

    def show_discussion_history(self):
        history = self.conversation_agent_object.get_conversation_history()
        for message in history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def get_user_message(self, chat_interaction):
        # un vocal est transcrit en texte, sinon on prend le texte tape
        if chat_interaction.audio:
            return self.speech_to_text_object.transcribe(
                chat_interaction.audio
            )

        return chat_interaction.text

    def run(self):
        chat_interaction = st.chat_input(
            "Que veux tu moussaillon ?",
            accept_file=False,
            accept_audio=True
        )

        if chat_interaction:
            user_message = self.get_user_message(chat_interaction)
            if user_message:
                self.conversation_agent_object.ask_llm(user_message)

        self.show_discussion_history()


if __name__ == "__main__":
    user_interface_object = UserInterface()
    user_interface_object.run()
