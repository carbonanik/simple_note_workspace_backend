from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from src.models.response_model import ResponseModel
from src.database.database import get_session
from src.models.note import CreateNote, Note


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=ResponseModel[list[Note]], status_code=status.HTTP_200_OK)
async def read_notes(
    session: Session = Depends(get_session),
):
    statement = select(Note)
    notes = session.exec(statement).all()
    return ResponseModel(data=notes, message="Notes fetched successfully")

@router.get("/{note_id}", response_model=ResponseModel[Note])
async def read_note(
    note_id: int,
    session: Session = Depends(get_session),
):
    statement = select(Note).where(Note.id == note_id)
    note = session.exec(statement).one()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Note not found"
        )
    
    return ResponseModel(data=note, message="Note fetched successfully")


@router.post("/", response_model=ResponseModel[Note], status_code=status.HTTP_201_CREATED)
async def create_note(
    note: CreateNote,
    session: Session = Depends(get_session),
):
    try:
        db_note = Note.model_validate(note)
        session.add(db_note)
        session.commit()
        session.refresh(db_note)
        return ResponseModel(data=db_note, message="Note created successfully")
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create note: {str(e.__cause__ or e)}",
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}",
        )
    


@router.put("/{note_id}", response_model=ResponseModel[Note])
async def update_note(
    note_id: int,
    note: Note,
    session: Session = Depends(get_session),
):
    statement = select(Note).where(Note.id == note_id)
    db_note = session.exec(statement).first()
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    # Update only the fields that changed
    update_data = note.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_note, key, value)

    session.add(db_note)  # this is safe now, because db_note is tracked
    session.commit()
    session.refresh(db_note)

    return ResponseModel(data=db_note, message="Note updated successfully")


@router.delete("/{note_id}", response_model=ResponseModel[Note], status_code=status.HTTP_200_OK)
async def delete_note(
    note_id: int,
    session: Session = Depends(get_session),
):
    statement = select(Note).where(Note.id == note_id)
    db_note = session.exec(statement).one()
    if db_note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Note not found"
        )
    session.delete(db_note)
    session.commit()
    return ResponseModel(data=db_note, message="Note deleted successfully")
    