from typing import Sequence
from sqlmodel import Session, select
from src.domain.entities.note import NoteEntity
from src.domain.repositories.note_repository import NoteRepository
from src.models.note import Note


class SqlNoteRepository(NoteRepository):
    def __init__(self, session: Session):
        self.session = session

    def list_notes(self) -> Sequence[NoteEntity]:
        notes = self.session.exec(select(Note)).all()
        return [NoteEntity(id=n.id, title=n.title, content=n.content) for n in notes]

    def get_note(self, note_id: int) -> NoteEntity | None:
        db_note = self.session.exec(select(Note).where(Note.id == note_id)).first()
        if not db_note:
            return None
        return NoteEntity(id=db_note.id, title=db_note.title, content=db_note.content)

    def create_note(self, note: NoteEntity) -> NoteEntity:
        db_note = Note(title=note.title, content=note.content)
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return NoteEntity(id=db_note.id, title=db_note.title, content=db_note.content)

    def update_note(self, note_id: int, note: NoteEntity) -> NoteEntity | None:
        db_note = self.session.exec(select(Note).where(Note.id == note_id)).first()
        if not db_note:
            return None
        db_note.title = note.title
        db_note.content = note.content
        self.session.add(db_note)
        self.session.commit()
        self.session.refresh(db_note)
        return NoteEntity(id=db_note.id, title=db_note.title, content=db_note.content)

    def delete_note(self, note_id: int) -> NoteEntity | None:
        db_note = self.session.exec(select(Note).where(Note.id == note_id)).first()
        if not db_note:
            return None
        self.session.delete(db_note)
        self.session.commit()
        return NoteEntity(id=db_note.id, title=db_note.title, content=db_note.content)


