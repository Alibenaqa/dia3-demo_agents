from groq import Groq

from dotenv import load_dotenv
import os


WHISPER_MODEL = "whisper-large-v3-turbo"
# indice donne a whisper pour privilegier le francais et l'anglais
LANGUAGE_HINT = "Conversation en francais ou en anglais."


class SpeechToText:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])

    def transcribe(self, audio_file):
        transcription = self.groq_client.audio.transcriptions.create(
            file=(audio_file.name, audio_file.getvalue()),
            model=WHISPER_MODEL,
            response_format="text",
            prompt=LANGUAGE_HINT,
        )

        return transcription.strip()
