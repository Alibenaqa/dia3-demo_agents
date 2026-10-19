import streamlit as st 
from llm_agent import ask_llm, load_history, save_history


st.set_page_config(page_title="Jarvis")
st.title("Barbe-Quasar")


# Memoire : l'historique survit aux reruns de streamlit grace a session_state,
# et aux refresh de la page grace au fichier history.json
if "history" not in st.session_state:
	st.session_state.history = load_history()

for message in st.session_state.history:
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

	response = ask_llm(user_input, st.session_state.history)

	with st.chat_message("assistant"):
		st.markdown(response)

	st.session_state.history.append({"role": "user", "content": user_input})
	st.session_state.history.append({"role": "assistant", "content": response})
	save_history(st.session_state.history)
