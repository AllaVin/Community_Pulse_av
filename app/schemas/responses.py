from pydantic import BaseModel, Field

class ResponseCreate(BaseModel):
    question_id: int = Field(...,description="ID of the question the response belongs to")
    text: str = Field(..., description="Text of the response", max_length=140)

class ResponseDelete(BaseModel):
    response_id: int = Field(...,description="ID of the response")
    text: str = Field(..., description="Text of the deleted response", max_length=140)

