from sqlalchemy import create_engine
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite:///tracking-alexia.db")
Session = sessionmaker(bind=engine)
session = Session()


class SentEmail(Base):
    __tablename__ = "sent_emails"
    id: Mapped[int] = mapped_column(primary_key=True)
    rut: Mapped[str] = mapped_column()
    to: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column()
    message_id: Mapped[str | None] = mapped_column(nullable=True)
    error: Mapped[str | None] = mapped_column(nullable=True)
    bounce_error: Mapped[str | None] = mapped_column(nullable=True)
    update_error: Mapped[str | None] = mapped_column(nullable=True)
    sent_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    received_at: Mapped[datetime | None] = mapped_column(nullable=True)
    opened_at: Mapped[datetime | None] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
