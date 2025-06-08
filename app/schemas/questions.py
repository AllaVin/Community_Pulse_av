from pydantic import BaseModel, Field
from typing import Union, List

class QuestionOut(BaseModel):
    id: int
    text: str = Field(..., description="Text of the question")
    category_id: int

class MessageResponse(BaseModel):
    message: Union[str, List[QuestionOut]]
