import json

from pydantic import BaseModel, model_validator
from typing import List
from fastapi import HTTPException, status

from app.utils.totimestamp import time_str_to_seconds

# class FileUpload(BaseModel):
#     path: str
    
# class FileCreate(BaseModel):
#     name: str
#     path: str
#     size: int
    
class UploadLocal(BaseModel):
    fps: float = 1.5
    save_pattern: str = f'frame_%05d.jpg'
    zipped: bool = True
    timecodes: List | None = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        if value['timecodes'] is None:
            return value
        timcodes = []
        for timecode in value['timecodes']:
            try:
                start, end = timecode.split("-")
                start = time_str_to_seconds(start)
                end = time_str_to_seconds(end)
                if start > end:
                    raise ValueError
                timcodes.append((start, end))
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid format timecodes. Example: 4:54-5:54, 21:54-34:34")
        value["timecodes"] = timcodes
        return value
    
class UploadLink(UploadLocal):
    link: str
            
    