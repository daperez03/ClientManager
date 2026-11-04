from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.
    This class provides the necessary metadata and configuration for SQLAlchemy
    to map Python classes to database tables.
    """
    pass

class Client(Base):
    """
    Represents a client in the system.
    """
    __tablename__ = "Clients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)