import random
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select

from src.models.rooms import Rooms, Activity


class RoomsService:
    def __init__(self, session):
        self.session = session
        self.employees = [
            {"first_name": "John", "last_name": "Key"},
            {"first_name": "Andrea", "last_name": "Kolin"},
            {"first_name": "Michael", "last_name": "Smith"},
            {"first_name": "Emily", "last_name": "Johnson"}
        ]

    async def update_temperature(self, rooms):
        for room in rooms:
            # Проверяем, когда было последнее изменение температуры
            current_time = datetime.now()
            time_since_last_change = current_time - room.last_temperature_change

            # Для каждой комнаты свой интервал изменения температуры (от 5 до 15 секунд)
            min_interval = 5 + room.id  # Разные интервалы для разных комнат
            if time_since_last_change < timedelta(seconds=min_interval):
                continue

            room_temperature = room.temperature
            new_temperature = round(random.uniform(15.0, 30.0), 1)
            temperature_change = abs(new_temperature - room_temperature)

            # Обновляем температуру только если изменение не больше 2.5 градусов
            if temperature_change <= 2.5:
                room.temperature = new_temperature
                room.last_temperature_change = current_time

                # Добавляем активность только если изменение больше 2.0 градусов
                if temperature_change > 2.0:
                    new_activity = Activity(
                        date=current_time,
                        room_id=room.id,
                        action=f"Temperature changed from {room_temperature}°C to {new_temperature}°C",
                        first_name=None,
                        last_name=None
                    )
                    self.session.add(new_activity)

        await self.session.commit()

    async def set_open(self, room):
        room.is_open = True
        # Выбираем случайного сотрудника
        employee = random.choice(self.employees)
        new_activity = Activity(
            date=datetime.now(),
            room_id=room.id,
            action="opened",
            first_name=employee["first_name"],
            last_name=employee["last_name"]
        )
        self.session.add(new_activity)
        await self.session.commit()

    async def set_close(self, room):
        await asyncio.sleep(3)
        room.is_open = False
        new_activity = Activity(
            date=datetime.now(),
            room_id=room.id,
            action="closed",
            first_name=None,
            last_name=None
        )
        self.session.add(new_activity)
        await self.session.commit()

    async def get_room_activities(self, room_id):
        query = select(Activity).where(Activity.room_id == room_id).order_by(Activity.date.desc())
        result = await self.session.execute(query)
        return result.scalars().all()