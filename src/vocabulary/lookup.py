from deep_translator import GoogleTranslator
from config.settings import Settings


class VocabularyLookup:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._cache: dict[str, dict] = {}
        self._translator = GoogleTranslator(source="es", target="en")

    def lookup(self, word: str) -> dict:
        if word in self._cache:
            return self._cache[word]

        result = {
            "word": word,
            "translation": self._translate(word),
            "conjugation": None,
        }
        self._cache[word] = result
        return result

    def lookup_batch(self, words: list[str]) -> dict[str, dict]:
        return {w: self.lookup(w) for w in words if w}

    def _translate(self, word: str) -> str:
        try:
            return self._translator.translate(word) or ""
        except Exception:
            return ""
