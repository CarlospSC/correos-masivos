from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///tracking-alexia.db")
Session = sessionmaker(bind=engine)
session = Session()


class SentEmail(Base):
    __tablename__ = "sent_emails"
    id: Mapped[int] = mapped_column(primary_key=True)
    segment: Mapped[str] = mapped_column()
    rut: Mapped[Optional[str]] = mapped_column(nullable=True)
    recipient_email: Mapped[Optional[str]] = mapped_column(nullable=True)
    recipient_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    company: Mapped[Optional[str]] = mapped_column(nullable=True)
    to: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column()
    message_id: Mapped[Optional[str]] = mapped_column(nullable=True)
    error: Mapped[Optional[str]] = mapped_column(nullable=True)
    bounce_error: Mapped[Optional[str]] = mapped_column(nullable=True)
    update_error: Mapped[Optional[str]] = mapped_column(nullable=True)
    sent_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    received_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    opened_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
