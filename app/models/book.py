import uuid

from sqlalchemy import CheckConstraint, Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
        CheckConstraint(
            "status IN ('Backlog', 'Currently Reading', 'Completed')",
            name="ck_books_status",
        ),
        CheckConstraint("pages_read >= 0", name="ck_books_pages_read_nonnegative"),
        CheckConstraint(
            "total_pages IS NULL OR total_pages > 0",
            name="ck_books_total_pages_positive",
        ),
        CheckConstraint(
            "total_pages IS NULL OR pages_read <= total_pages",
            name="ck_books_progress_within_total",
        ),
        CheckConstraint(
            "personal_rating IS NULL OR (personal_rating >= 0 AND personal_rating <= 4)",
            name="ck_books_rating_range",
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(150), nullable=False)
    genre = Column(String(100), nullable=True)
    isbn = Column(String(20), nullable=True)
    cover_url = Column(String(2048), nullable=True)
    status = Column(String(32), nullable=False, default="Backlog")
    pages_read = Column(Integer, nullable=False, default=0)
    total_pages = Column(Integer, nullable=True)
    personal_rating = Column(Float, nullable=True)
