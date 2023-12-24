from sqlalchemy import Column, Integer, String

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    description = Column(String(4096))
