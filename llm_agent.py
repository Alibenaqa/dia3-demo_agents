from groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()


MODEL_NAME = "openai/gpt-oss-120b"
CONTEXT_FILE = "./context.txt"


class ConversationAgent:
    """Agent conversationnel qui garde en memoire l'historique de la conversation."""

    def __init__(self, context_file=CONTEXT_FILE, model_name=MODEL_NAME):
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.model_name = model_name
        self.conversation_history = []
        self.update_conversation_history(
            role="system",
            content=self.read_file(file_path=context_file)
        )

    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()

    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
                "role": role,
                "content": content
            }
        )

    def ask_llm(self, question):
        self.update_conversation_history(role="user", content=question)

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history,
            model=self.model_name,
            include_reasoning=False,
        ).choices[0].message.content

        self.update_conversation_history(role="assistant", content=response)
        return response


if __name__ == "__main__":
    agent = ConversationAgent()
    while True:
        question = input("Pose ta question :\n")
        response = agent.ask_llm(question)
        print("\n")
        print(response)
