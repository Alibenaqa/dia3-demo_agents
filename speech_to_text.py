from groq import Groq

from dotenv import load_dotenv
import os


WHISPER_MODEL = "whisper-large-v3-turbo"
PRIORITY_LANGUAGES = ["french", "english"]
DEFAULT_LANGUAGE = "fr"


class SpeechToText:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])

    def request_whisper(self, audio_file, language=None):
        return self.groq_client.audio.transcriptions.create(
            file=(audio_file.name, audio_file.getvalue()),
            model=WHISPER_MODEL,
            response_format="verbose_json",
            language=language,
        )

    def transcribe(self, audio_file):
        transcription = self.request_whisper(audio_file)

        # francais et anglais en priorite : si whisper detecte une autre
        # langue, on refait la transcription en forcant le francais
        if transcription.language.lower() not in PRIORITY_LANGUAGES:
            transcription = self.request_whisper(
                audio_file,
                language=DEFAULT_LANGUAGE
            )

        return transcription.text.strip()
