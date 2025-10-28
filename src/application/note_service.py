from typing import Sequence
from src.domain.entities.note import NoteEntity
from src.domain.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self, repo: NoteRepository):
        self.repo = repo

    def list_notes(self) -> Sequence[NoteEntity]:
        return self.repo.list_notes()

    def get_note(self, note_id: int) -> NoteEntity | None:
        return self.repo.get_note(note_id)

    def create_note(self, title: str, content: str) -> NoteEntity:
        return self.repo.create_note(NoteEntity(id=None, title=title, content=content))

    def update_note(self, note_id: int, title: str, content: str) -> NoteEntity | None:
        return self.repo.update_note(note_id, NoteEntity(id=note_id, title=title, content=content))

    def delete_note(self, note_id: int) -> NoteEntity | None:
        return self.repo.delete_note(note_id)


