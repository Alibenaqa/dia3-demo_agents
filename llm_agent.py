from groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()


MODEL_NAME = "openai/gpt-oss-120b"
CONTEXT_FILE = "./context.txt"


class ConversationAgent:
    """Agent conversationnel qui garde en memoire l'historique de la conversation."""

    def __init__(self, context_file=CONTEXT_FILE, model_name=MODEL_NAME):
        self.client = Groq(api_key=os.environ["GROQ_KEY"])
        self.model_name = model_name
        self.system_prompt = self.read_file(file_path=context_file)
        self.history = []

    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    def ask(self, question):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                *self.history,
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model=self.model_name,
            include_reasoning=False,
        )

        response = chat_completion.choices[0].message.content

        self.history.append({"role": "user", "content": question})
        self.history.append({"role": "assistant", "content": response})
        return response


if __name__ == "__main__":
    agent = ConversationAgent()
    while True:
        question = input("Pose ta question :\n")
        response = agent.ask(question)
        print("\n")
        print(response)
