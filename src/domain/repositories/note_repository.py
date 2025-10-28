from abc import ABC, abstractmethod
from typing import Sequence
from src.domain.entities.note import NoteEntity


class NoteRepository(ABC):
    @abstractmethod
    def list_notes(self) -> Sequence[NoteEntity]:
        ...

    @abstractmethod
    def get_note(self, note_id: int) -> NoteEntity | None:
        ...

    @abstractmethod
    def create_note(self, note: NoteEntity) -> NoteEntity:
        ...

    @abstractmethod
    def update_note(self, note_id: int, note: NoteEntity) -> NoteEntity | None:
        ...

    @abstractmethod
    def delete_note(self, note_id: int) -> NoteEntity | None:
        ...


