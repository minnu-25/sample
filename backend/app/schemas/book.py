from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, model_validator


class ReadingStatus(str, Enum):
    BACKLOG = "Backlog"
    CURRENTLY_READING = "Currently Reading"
    COMPLETED = "Completed"


class CreateBookRequest(BaseModel):
    title: str = Field(min_length=1, max_length=200, strip_whitespace=True)
    author: str = Field(min_length=1, max_length=150, strip_whitespace=True)
    genre: Optional[str] = Field(default=None, max_length=100, strip_whitespace=True)
    isbn: Optional[str] = Field(default=None, max_length=20, strip_whitespace=True)
    cover_url: Optional[AnyHttpUrl] = None
    status: ReadingStatus = ReadingStatus.BACKLOG
    pages_read: int = Field(default=0, ge=0)
    total_pages: Optional[int] = Field(default=None, gt=0)
    personal_rating: Optional[float] = Field(default=None, ge=0, le=4)

    @model_validator(mode="after")
    def validate_progress(self):
        if self.total_pages is not None and self.pages_read > self.total_pages:
            raise ValueError("pages_read cannot exceed total_pages")
        if self.cover_url is not None and len(str(self.cover_url)) > 2048:
            raise ValueError("cover_url must be at most 2048 characters")
        return self


class UpdateBookRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200, strip_whitespace=True)
    author: Optional[str] = Field(default=None, min_length=1, max_length=150, strip_whitespace=True)
    genre: Optional[str] = Field(default=None, max_length=100, strip_whitespace=True)
    isbn: Optional[str] = Field(default=None, max_length=20, strip_whitespace=True)
    cover_url: Optional[AnyHttpUrl] = None
    status: Optional[ReadingStatus] = None
    pages_read: Optional[int] = Field(default=None, ge=0)
    total_pages: Optional[int] = Field(default=None, gt=0)
    personal_rating: Optional[float] = Field(default=None, ge=0, le=4)

    @model_validator(mode="after")
    def validate_patch_fields(self):
        required_non_null = {"title", "author", "status", "pages_read"}
        null_fields = required_non_null.intersection(
            field for field in self.model_fields_set if getattr(self, field) is None
        )
        if null_fields:
            raise ValueError(f"Fields cannot be null: {', '.join(sorted(null_fields))}")
        if self.cover_url is not None and len(str(self.cover_url)) > 2048:
            raise ValueError("cover_url must be at most 2048 characters")
        return self


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    author: str
    genre: Optional[str]
    isbn: Optional[str]
    cover_url: Optional[str]
    status: ReadingStatus
    pages_read: int
    total_pages: Optional[int]
    personal_rating: Optional[float]


class BookListResponse(BaseModel):
    message: str
    total: int
    books: list[BookResponse]


class DeleteBookResponse(BaseModel):
    message: str
