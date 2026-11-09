from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.book import Book
from app.models.user import User
from app.schemas.book import (
    BookListResponse,
    BookResponse,
    CreateBookRequest,
    DeleteBookResponse,
    UpdateBookRequest,
)
from app.utils.logger import logger

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    payload: CreateBookRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    book = Book(
        title=payload.title,
        author=payload.author,
        genre=payload.genre,
        isbn=payload.isbn,
        cover_url=str(payload.cover_url) if payload.cover_url is not None else None,
        status=payload.status.value,
        pages_read=payload.pages_read,
        total_pages=payload.total_pages,
        personal_rating=payload.personal_rating,
        user_id=current_user.id,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    logger.info(f"Book created with ID {book.id} for user {current_user.email}")
    return book


@router.get("", response_model=BookListResponse, status_code=status.HTTP_200_OK)
def list_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Book).where(Book.user_id == current_user.id).order_by(Book.title)
    books = db.execute(statement).scalars().all()
    return BookListResponse(
        message="Books retrieved successfully",
        total=len(books),
        books=books,
    )


@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def get_book(
    book_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Book).where(Book.id == book_id, Book.user_id == current_user.id)
    book = db.execute(statement).scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
def update_book(
    book_id: UUID,
    payload: UpdateBookRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Book).where(Book.id == book_id, Book.user_id == current_user.id)
    book = db.execute(statement).scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="At least one field must be provided",
        )

    pages_read = updates.get("pages_read", book.pages_read)
    total_pages = updates.get("total_pages", book.total_pages)
    if total_pages is not None and pages_read > total_pages:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="pages_read cannot exceed total_pages",
        )

    for field, value in updates.items():
        if field == "cover_url":
            value = str(value) if value is not None else None
        elif field == "status" and value is not None:
            value = value.value
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    logger.info(f"Book {book.id} updated for user {current_user.email}")
    return book


@router.delete(
    "/{book_id}", response_model=DeleteBookResponse, status_code=status.HTTP_200_OK
)
def delete_book(
    book_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    statement = select(Book).where(Book.id == book_id, Book.user_id == current_user.id)
    book = db.execute(statement).scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()
    logger.info(f"Book {book_id} deleted for user {current_user.email}")
    return DeleteBookResponse(message="Book deleted successfully")
