import mlconjug3


PRONOUNS = ["yo", "tú", "él/ella", "nosotros", "vosotros", "ellos/ellas"]

TENSES_TO_SHOW = [
    ("Presente",    "Indicativo Presente"),
    ("Pretérito",   "Indicativo Pretérito perfecto simple"),
    ("Imperfecto",  "Indicativo Pretérito imperfecto"),
    ("Futuro",      "Indicativo Futuro"),
]

INFINITIVE_ENDINGS = ("ar", "er", "ir", "arse", "erse", "irse")


class SpanishConjugator:
    def __init__(self):
        self._conjugator = mlconjug3.Conjugator(language="es")

    def conjugate(self, infinitive: str) -> dict | None:
        try:
            verb = self._conjugator.conjugate(infinitive)
            if verb is None:
                return None
            return self._format(verb)
        except Exception:
            return None

    def looks_like_infinitive(self, word: str) -> bool:
        return word.endswith(INFINITIVE_ENDINGS)

    def _format(self, verb) -> dict:
        result = {}
        for display_name, tense_key in TENSES_TO_SHOW:
            try:
                forms = list(verb[tense_key].values())
                result[display_name] = dict(zip(PRONOUNS, forms))
            except (KeyError, TypeError, AttributeError):
                continue
        return result if result else None
