from pydantic import BaseModel


class RoomSensor(BaseModel):
    id: int
    status_door: bool
    temperature: float

