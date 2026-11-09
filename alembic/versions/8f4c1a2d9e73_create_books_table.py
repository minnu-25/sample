"""create books table

Revision ID: 8f4c1a2d9e73
Revises: 037027d811ea
Create Date: 2026-11-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8f4c1a2d9e73"
down_revision: Union[str, Sequence[str], None] = "037027d811ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("author", sa.String(length=150), nullable=False),
        sa.Column("genre", sa.String(length=100), nullable=True),
        sa.Column("isbn", sa.String(length=20), nullable=True),
        sa.Column("cover_url", sa.String(length=2048), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("pages_read", sa.Integer(), nullable=False),
        sa.Column("total_pages", sa.Integer(), nullable=True),
        sa.Column("personal_rating", sa.Float(), nullable=True),
        sa.CheckConstraint(
            "status IN ('Backlog', 'Currently Reading', 'Completed')",
            name="ck_books_status",
        ),
        sa.CheckConstraint("pages_read >= 0", name="ck_books_pages_read_nonnegative"),
        sa.CheckConstraint(
            "total_pages IS NULL OR total_pages > 0",
            name="ck_books_total_pages_positive",
        ),
        sa.CheckConstraint(
            "total_pages IS NULL OR pages_read <= total_pages",
            name="ck_books_progress_within_total",
        ),
        sa.CheckConstraint(
            "personal_rating IS NULL OR (personal_rating >= 0 AND personal_rating <= 4)",
            name="ck_books_rating_range",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_books_user_id"), "books", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_books_user_id"), table_name="books")
    op.drop_table("books")
