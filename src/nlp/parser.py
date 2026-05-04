import spacy
from dataclasses import dataclass, field
from config.settings import Settings


@dataclass
class ParsedResponse:
    raw_text: str
    tokens: list[dict]      # {text, lemma, pos, is_stop}
    keywords: list[str]     # content-word lemmas (nouns, verbs, adjectives)
    verbs: list[dict]       # {text, lemma, morph}
    entities: list[dict]    # {text, label}
    topics: list[str]       # matched topic labels from TOPIC_MAP


TOPIC_MAP: dict[str, set[str]] = {
    "family":           {"familia", "hermano", "hermana", "madre", "padre", "hijo", "hija", "abuelo", "abuela", "mamá", "papá"},
    "work":             {"trabajo", "trabajar", "empresa", "oficina", "profesión", "carrera", "jefe", "sueldo"},
    "study":            {"estudiar", "universidad", "escuela", "clase", "curso", "examen", "estudiante"},
    "food":             {"comida", "comer", "cocinar", "restaurante", "plato", "receta", "hambre"},
    "travel":           {"viajar", "viaje", "país", "ciudad", "vacaciones", "visitar", "turismo", "vuelo"},
    "hobbies":          {"deporte", "música", "leer", "bailar", "nadar", "jugar", "pintar", "guitarra", "fútbol", "tenis"},
    "daily_life":       {"rutina", "mañana", "tarde", "noche", "semana", "horario", "levantarse", "dormir"},
    "friends":          {"amigo", "amiga", "compañero", "salir", "quedar", "fiesta", "grupo"},
    "home":             {"casa", "piso", "apartamento", "barrio", "vivir", "habitación"},
    "language_learning": {"español", "aprender", "idioma", "lengua", "práctica", "nivel"},
}


class NLPParser:
    def __init__(self, settings: Settings):
        self.settings = settings
        self._nlp = None

    @property
    def nlp(self):
        if self._nlp is None:
            self._nlp = spacy.load(self.settings.SPACY_MODEL)
        return self._nlp

    def parse(self, text: str) -> ParsedResponse:
        doc = self.nlp(text.lower())

        tokens = [
            {"text": t.text, "lemma": t.lemma_, "pos": t.pos_, "is_stop": t.is_stop}
            for t in doc
        ]

        keywords = [
            t.lemma_ for t in doc
            if t.pos_ in ("NOUN", "VERB", "ADJ", "PROPN") and not t.is_stop and t.is_alpha
        ]

        verbs = [
            {"text": t.text, "lemma": t.lemma_, "morph": str(t.morph)}
            for t in doc if t.pos_ == "VERB"
        ]

        entities = [
            {"text": ent.text, "label": ent.label_}
            for ent in doc.ents
        ]

        topics = self._match_topics(keywords)

        return ParsedResponse(
            raw_text=text,
            tokens=tokens,
            keywords=keywords,
            verbs=verbs,
            entities=entities,
            topics=topics,
        )

    def _match_topics(self, keywords: list[str]) -> list[str]:
        keyword_set = set(keywords)
        return [topic for topic, words in TOPIC_MAP.items() if keyword_set & words]
