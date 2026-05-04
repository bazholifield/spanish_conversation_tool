import re
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Turn:
    question: str
    response: str
    turn_number: int
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Transcript:
    turns: list[Turn] = field(default_factory=list)
    started_at: datetime | None = None
    ended_at: datetime | None = None

    def start(self) -> None:
        self.started_at = datetime.now()

    def end(self) -> None:
        self.ended_at = datetime.now()

    def add_turn(self, turn: Turn) -> None:
        self.turns.append(turn)

    def duration_seconds(self) -> int:
        if self.started_at and self.ended_at:
            return int((self.ended_at - self.started_at).total_seconds())
        return 0

    def all_bot_words(self) -> list[str]:
        return [word for turn in self.turns for word in turn.question.split()]

    def all_user_words(self) -> list[str]:
        return [word for turn in self.turns for word in turn.response.split()]

    def unique_spanish_words(self) -> set[str]:
        all_words = self.all_bot_words() + self.all_user_words()
        cleaned = {re.sub(r"[^a-záéíóúüñ]", "", w.lower()) for w in all_words}
        return {w for w in cleaned if len(w) > 1}
