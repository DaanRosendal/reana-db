"""Workflow sharing.

Revision ID: 6289daf693a1
Revises: 377cfbfccf75
Create Date: 2023-10-17 09:04:41.437326

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = "6289daf693a1"
down_revision = "377cfbfccf75"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "role",
        sa.Column("id_", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint("id_"),
        sa.UniqueConstraint("name"),
        schema="__reana",
    )
    op.create_table(
        "user_workflow",
        sa.Column(
            "workflow_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False
        ),
        sa.Column("user_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column("role_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("valid_until", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["__reana.role.id_"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["__reana.user_.id_"],
        ),
        sa.ForeignKeyConstraint(
            ["workflow_id"],
            ["__reana.workflow.id_"],
        ),
        sa.PrimaryKeyConstraint("workflow_id", "user_id"),
        schema="__reana",
    )
    op.create_unique_constraint(
        "uq_interactive_session_id", "interactive_session", ["id_"], schema="__reana"
    )


def downgrade():
    op.drop_constraint(
        "uq_interactive_session_id",
        "interactive_session",
        schema="__reana",
        type_="unique",
    )
    op.drop_table("user_workflow", schema="__reana")
    op.drop_table("role", schema="__reana")
