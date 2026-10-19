import streamlit as st 
from llm_agent import ConversationAgent


st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")


# st.cache_resource cree l'agent une seule fois et le garde dans la memoire du serveur :
# son historique survit aux reruns ET aux actualisations de la page (pas au redemarrage)
@st.cache_resource
def get_agent():
	return ConversationAgent()

agent = get_agent()

# on n'affiche pas le message "system" (la personnalite), seulement la conversation
for message in agent.conversation_history[1:]:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])


user_input = st.chat_input(
	"Que veux tu moussaillon ?",
	accept_file=False,
	accept_audio=False
	)

if user_input :
	with st.chat_message("user"):
		st.markdown(user_input)

	response = agent.ask_llm(user_input)

	with st.chat_message("assistant"):
		st.markdown(response)
