from fastapi import APIRouter, Depends, status

from src.models.response_model import ResponseModel
from src.interfaces.controllers.note_controller import NoteController
from src.interfaces.schemas.note import NoteCreateSchema, NoteUpdateSchema
from src.domain.entities.note import NoteEntity
from src.infrastructure.security.dependencies import get_current_username


router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=ResponseModel[list[NoteEntity]], status_code=status.HTTP_200_OK)
async def read_notes(controller: NoteController = Depends(), username: str = Depends(get_current_username)):
    notes = controller.list_notes()
    return ResponseModel(data=notes, message="Notes fetched successfully")


@router.get("/{note_id}", response_model=ResponseModel[NoteEntity])
async def read_note(note_id: int, controller: NoteController = Depends(), username: str = Depends(get_current_username)):
    note = controller.get_note(note_id)
    return ResponseModel(data=note, message="Note fetched successfully")


@router.post("/", response_model=ResponseModel[NoteEntity], status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteCreateSchema, controller: NoteController = Depends(), username: str = Depends(get_current_username)):
    note = controller.create_note(title=payload.title, content=payload.content)
    return ResponseModel(data=note, message="Note created successfully")


@router.put("/{note_id}", response_model=ResponseModel[NoteEntity])
async def update_note(note_id: int, payload: NoteUpdateSchema, controller: NoteController = Depends(), username: str = Depends(get_current_username)):
    note = controller.update_note(note_id=note_id, title=payload.title, content=payload.content)
    return ResponseModel(data=note, message="Note updated successfully")


@router.delete("/{note_id}", response_model=ResponseModel[NoteEntity], status_code=status.HTTP_200_OK)
async def delete_note(note_id: int, controller: NoteController = Depends(), username: str = Depends(get_current_username)):
    note = controller.delete_note(note_id)
    return ResponseModel(data=note, message="Note deleted successfully")
    