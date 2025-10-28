from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from src.application.note_service import NoteService
from src.domain.entities.note import NoteEntity
from src.infrastructure.repositories.sql_note_repository import SqlNoteRepository
from src.database.database import get_session


def get_note_service(session: Session = Depends(get_session)) -> NoteService:
    repo = SqlNoteRepository(session)
    return NoteService(repo)


class NoteController:
    def __init__(self, service: NoteService = Depends(get_note_service)):
        self.service = service

    def list_notes(self) -> list[NoteEntity]:
        return list(self.service.list_notes())

    def get_note(self, note_id: int) -> NoteEntity:
        note = self.service.get_note(note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        return note

    def create_note(self, title: str, content: str) -> NoteEntity:
        return self.service.create_note(title=title, content=content)

    def update_note(self, note_id: int, title: str, content: str) -> NoteEntity:
        note = self.service.update_note(note_id=note_id, title=title, content=content)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        return note

    def delete_note(self, note_id: int) -> NoteEntity:
        note = self.service.delete_note(note_id)
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
        return note


