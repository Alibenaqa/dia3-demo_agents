from groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()



def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


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
    history = []
    while True:
        question = input("Pose ta question :\n")
        response = ask_llm(question, history)
        print("\n")
        print(response)
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": response})