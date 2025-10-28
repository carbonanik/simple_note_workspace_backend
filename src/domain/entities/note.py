from dataclasses import dataclass


@dataclass
class NoteEntity:
    id: int | None
    title: str
    content: str


