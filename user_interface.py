import streamlit as st
from llm_agent import ConversationAgent
from image_to_text import ImageToText


IMAGE_TYPES = ["png", "jpg", "jpeg", "webp"]
DEFAULT_IMAGE_QUESTION = "Que vois-tu sur cette image ?"


class UserInterface:
    def __init__(self):
        st.set_page_config(page_title="Jarvis")
        st.title("Barbe-Quasar")
        self.conversation_agent_object = (
            self.get_persistant_conversation_agent()
        )
        self.image_to_text_object = self.get_persistant_image_to_text()
        self.uploaded_images = self.get_persistant_uploaded_images()

    def get_persistant_conversation_agent(self):
        if "conversation_agent_object" not in st.session_state:
            st.session_state.conversation_agent_object = ConversationAgent()

        return st.session_state.conversation_agent_object

    def get_persistant_image_to_text(self):
        if "image_to_text_object" not in st.session_state:
            st.session_state.image_to_text_object = ImageToText()

        return st.session_state.image_to_text_object

    def get_persistant_uploaded_images(self):
        # {position du message : {"image": l'image, "text": la question}}
        if "uploaded_images" not in st.session_state:
            st.session_state.uploaded_images = {}

        return st.session_state.uploaded_images

    def show_discussion_history(self):
        history = self.conversation_agent_object.get_conversation_history()
        for position, message in enumerate(history):
            with st.chat_message(message["role"]):
                if position in self.uploaded_images:
                    # on montre l'image et la question, pas la description
                    uploaded_image = self.uploaded_images[position]
                    st.image(uploaded_image["image"], width=300)
                    st.markdown(uploaded_image["text"])
                else:
                    st.markdown(message["content"])

    def add_image_to_message(self, text_interaction, image_file):
        # l'image et la question sont gardees pour l'affichage, et la
        # description est ajoutee au message envoye au llm (cachee a l'ecran)
        history = self.conversation_agent_object.get_conversation_history()
        self.uploaded_images[len(history)] = {
            "image": image_file.getvalue(),
            "text": text_interaction
        }

        description = self.image_to_text_object.describe(image_file)
        return (
            f"{text_interaction}\n\n"
            f"[Image envoyee par l'utilisateur : {description}]"
        )

    def get_user_message(self, chat_interaction):
        user_message = chat_interaction.text

        if chat_interaction.files:
            user_message = self.add_image_to_message(
                user_message or DEFAULT_IMAGE_QUESTION,
                chat_interaction.files[0]
            )

        return user_message

    def run(self):
        chat_interaction = st.chat_input(
            "Que veux tu moussaillon ?",
            accept_file=True,
            file_type=IMAGE_TYPES,
            accept_audio=False
        )

        if chat_interaction:
            user_message = self.get_user_message(chat_interaction)
            if user_message:
                self.conversation_agent_object.ask_llm(user_message)

        self.show_discussion_history()


if __name__ == "__main__":
    user_interface_object = UserInterface()
    user_interface_object.run()
