from groq import Groq

from dotenv import load_dotenv
import json
import os

load_dotenv()



def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


HISTORY_FILE = "./history.json"


def load_history():
    """Recharge la conversation sauvegardee (liste vide si aucune)."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_history(history):
    """Sauvegarde la conversation pour qu'elle survive a un refresh / redemarrage."""
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def ask_llm(question, history=None):
    """history : liste des messages precedents [{"role": ..., "content": ...}]"""
    if history is None:
        history = []

    client = Groq(api_key=os.environ["GROQ_KEY"])

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": read_file(file_path="./context.txt")
            },
            *history,
            {
                "role": "user",
                "content": question,
            }
        ],
        model="openai/gpt-oss-120b",
        include_reasoning=False,
    )


    response = chat_completion.choices[0].message.content
    return response


if __name__ == "__main__":
    history = load_history()
    while True:
        question = input("Pose ta question :\n")
        response = ask_llm(question, history)
        print("\n")
        print(response)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": response})
        save_history(history)