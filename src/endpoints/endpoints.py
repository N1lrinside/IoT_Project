from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from src.schemas.schemas import RoomSensor
from src.core.database import SessionDep, engine, Base
from src.models.rooms import Rooms, Activity
from src.service.rooms import RoomsService

router = APIRouter(prefix="/sensor", tags=["Sensor"])

templates = Jinja2Templates(directory="./src")

@router.get("/room")
async def get_room_sensor(session: SessionDep):
    query = select(Rooms)
    result = await session.execute(query)
    rooms = result.scalars().all()
    return rooms

@router.post("/setup")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@router.post("/load_3_rooms")
async def load_3_rooms(session: SessionDep):
    for _ in range(3):
        new_room = Rooms()
        session.add(new_room)
    await session.commit()
    return True

@router.patch("/update_temperature")
async def update_temperature_in_rooms(session: SessionDep):
    query = select(Rooms)
    result = await session.execute(query)
    rooms = result.scalars().all()
    rooms_service = RoomsService(session)
    await rooms_service.update_temperature(rooms)
    return True

@router.patch("/open_room")
async def open_room(id_room: int, session: SessionDep):
    query = select(Rooms).where(Rooms.id == id_room)
    result = await session.execute(query)
    room = result.scalars().first()
    rooms_service = RoomsService(session)
    await rooms_service.set_open(room)
    return True

@router.patch("/closed_room")
async def closed_room(id_room: int, session: SessionDep):
    query = select(Rooms).where(Rooms.id == id_room)
    result = await session.execute(query)
    room = result.scalars().first()
    rooms_service = RoomsService(session)
    await rooms_service.set_close(room)
    return True

@router.get("/", response_class=HTMLResponse)
async def read_rooms(request: Request, session: SessionDep):
    query = select(Rooms)
    result = await session.execute(query)
    rooms_data = result.scalars().all()

    rooms_service = RoomsService(session)
    activities_by_room = {}
    for room in rooms_data:
        activities = await rooms_service.get_room_activities(room.id)
        activities_by_room[room.id] = activities

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "rooms": rooms_data,
            "activities_by_room": activities_by_room
        }
    )

@router.get("/get_activities/{room_id}")
async def get_activities(room_id: int, session: SessionDep):
    rooms_service = RoomsService(session)
    activities = await rooms_service.get_room_activities(room_id)
    return [{
        "room_id": activity.room_id,
        "action": activity.action,
        "date": activity.date.strftime('%Y-%m-%d %H:%M:%S'),
        "first_name": activity.first_name,
        "last_name": activity.last_name
    } for activity in activities]
