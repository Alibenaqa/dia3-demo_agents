from groq import Groq

from dotenv import load_dotenv
import base64
import os


VISION_MODEL = "qwen/qwen3.8-27b"
VISION_PROMPT = (
    "Decris cette image en francais, en 3 a 5 phrases, sans liste : "
    "les objets, les personnes, le texte visible, les couleurs et le contexte."
)


class ImageToText:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])

    @staticmethod
    def encode_image(image_file):
        image_base64 = base64.b64encode(image_file.getvalue()).decode()
        return f"data:{image_file.type};base64,{image_base64}"

    def describe(self, image_file):
        return self.groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": VISION_PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": self.encode_image(image_file)
                            }
                        }
                    ]
                }
            ],
            model=VISION_MODEL,
            reasoning_format="hidden",
        ).choices[0].message.content.strip()
