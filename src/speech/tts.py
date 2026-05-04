import os
import tempfile
from gtts import gTTS
import pygame
from config.settings import Settings


class TextToSpeech:
    def __init__(self, settings: Settings):
        self.settings = settings
        pygame.mixer.init()

    def speak(self, text: str) -> None:
        tts = gTTS(text=text, lang=self.settings.TTS_LANGUAGE, slow=self.settings.TTS_SLOW)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name
        try:
            tts.save(tmp_path)
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        finally:
            pygame.mixer.music.unload()
            os.unlink(tmp_path)
