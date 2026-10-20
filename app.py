import streamlit as st 
from llm_agent import ConversationAgent
import random





st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")

if "conversation_agent_object" not in st.session_state:
	st.session_state.conversation_agent_object = ConversationAgent() 


def show_discussion_history():
	for message in st.session_state.conversation_agent_object.get_conversation_history():
		with st.chat_message(message["role"]):
			st.markdown(message["content"])



text_interaction = st.chat_input(
	"Que veux tu moussaillon ?",
	accept_file=False,
	accept_audio=False
	)

if text_interaction :
	st.session_state.conversation_agent_object.ask_llm(text_interaction)
	
	show_discussion_history()



















	# response = ask_llm(user_input)
	# with st.chat_message("user"):
	# 	st.markdown(user_input)

	# with st.chat_message("system"):
	# 	st.markdown(response)


