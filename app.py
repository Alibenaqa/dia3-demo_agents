import streamlit as st 
from llm_agent import ask_llm


st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")


# Memoire : st.cache_resource garde la liste dans la memoire du serveur streamlit,
# elle survit donc aux reruns ET aux actualisations de la page (pas au redemarrage)
@st.cache_resource
def get_history():
	return []

history = get_history()

for message in history:
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

	response = ask_llm(user_input, history)

	with st.chat_message("assistant"):
		st.markdown(response)

	history.append({"role": "user", "content": user_input})
	history.append({"role": "assistant", "content": response})
