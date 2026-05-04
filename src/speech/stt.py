import speech_recognition as sr
from config.settings import Settings


class SpeechToText:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

    def listen(self, timeout: int = 10, phrase_time_limit: int = 30) -> str | None:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
                text = self.recognizer.recognize_google(
                    audio, language=self.settings.STT_LANGUAGE
                )
                return text
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                return None
            except sr.RequestError as e:
                raise RuntimeError(f"STT service unavailable: {e}") from e
