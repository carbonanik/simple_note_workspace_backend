from sqlmodel import Field, SQLModel

class NoteBase(SQLModel):
    title: str
    content: str

class Note(NoteBase, table=True):
    id: int = Field(default=None, primary_key=True)
    
class CreateNote(NoteBase):
    title: str
    content: str