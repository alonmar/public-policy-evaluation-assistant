import os
from datetime import datetime
from sqlalchemy_utils import create_database, database_exists
from typing import Optional
from zoneinfo import ZoneInfo
from sqlmodel import (
    TIMESTAMP,
    Column,
    Field,
    Session,
    SQLModel,
    create_engine,
    text,
)


TZ_INFO = os.getenv("TZ", "America/Mexico_City")
tz = ZoneInfo(TZ_INFO)


class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(default=None)
    question: str = Field(default=None)
    answer: str = Field(default=None)
    created_datetime: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )


class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(default=None)
    feedback: str = Field(default=None)
    created_datetime: Optional[datetime] = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )


# SQLITE_URL = "postgresql://postgres:example@localhost:5432/test"
SQLITE_URL = "sqlite:///./test.db"


def init_db():
    if not database_exists(SQLITE_URL):
        create_database(SQLITE_URL)

    engine = create_engine(SQLITE_URL)

    SQLModel.metadata.create_all(engine)


def save_conversation(conversation_id, question, answer):
    with Session(SQLITE_URL) as session:
        conversation = Conversation(
            conversation_id=conversation_id, question=question, answer=answer
        )
        session.add(conversation)
        session.commit()


def save_feedback(conversation_id, feedback):
    with Session(SQLITE_URL) as session:
        feedback = Feedback(conversation_id=conversation_id, feedback=feedback)
        session.add(feedback)
        session.commit()
