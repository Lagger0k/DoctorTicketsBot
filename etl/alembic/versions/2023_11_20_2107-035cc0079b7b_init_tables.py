"""init tables

Revision ID: 035cc0079b7b
Revises: 
Create Date: 2023-11-20 21:07:08.626291

"""
from typing import Sequence
from typing import Union

from alembic import op
import sqlalchemy as sa

revision: str = '035cc0079b7b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('speciality',
                    sa.Column('title', sa.String(length=100), nullable=True, comment='Специальность'),
                    sa.Column('code', sa.Integer(), nullable=True, comment='Код специальности'),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('last_modified', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user',
                    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('telegram_id')
                    )
    op.create_table('doctor',
                    sa.Column('first_name', sa.String(length=100), nullable=False, comment='Имя'),
                    sa.Column('last_name', sa.String(length=100), nullable=False, comment='Фамилия'),
                    sa.Column('middle_name', sa.String(length=100), nullable=True, comment='Отчество'),
                    sa.Column('department', sa.Integer(), nullable=True, comment='Департамент'),
                    sa.Column('hospital', sa.Integer(), nullable=True, comment='Учреждение'),
                    sa.Column('speciality_id', sa.Uuid(), nullable=True),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('last_modified', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['speciality_id'], ['speciality.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('speciality_task',
                    sa.Column('speciality_id', sa.Uuid(), nullable=True),
                    sa.Column('user_id', sa.Uuid(), nullable=True),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('last_modified', sa.DateTime(), nullable=False),
                    sa.Column('day', sa.Date(), nullable=False, comment='День приёма'),
                    sa.Column('completed', sa.Boolean(), nullable=False, comment='Поиск завершен'),
                    sa.Column('cancelled', sa.Boolean(), nullable=False, comment='Поиск отменён'),
                    sa.ForeignKeyConstraint(['speciality_id'], ['speciality.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('doctor_task',
                    sa.Column('doctor_id', sa.Uuid(), nullable=True),
                    sa.Column('user_id', sa.Uuid(), nullable=True),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('last_modified', sa.DateTime(), nullable=False),
                    sa.Column('day', sa.Date(), nullable=False, comment='День приёма'),
                    sa.Column('completed', sa.Boolean(), nullable=False, comment='Поиск завершен'),
                    sa.Column('cancelled', sa.Boolean(), nullable=False, comment='Поиск отменён'),
                    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('schedule_day',
                    sa.Column('day', sa.Date(), nullable=False, comment='День приёма'),
                    sa.Column('is_working_day', sa.Boolean(), nullable=False, comment='Ведется приём'),
                    sa.Column('doctor_id', sa.Uuid(), nullable=True),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('last_modified', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['doctor_id'], ['doctor.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('ticket',
                    sa.Column('time', sa.String(length=32), nullable=False, comment='Время приёма'),
                    sa.Column('type', sa.Integer(), nullable=False, comment='Тип талона'),
                    sa.Column('code', sa.Integer(), nullable=False, comment='Код талона'),
                    sa.Column('is_free', sa.Boolean(), nullable=False, comment='Талон свободен'),
                    sa.Column('schedule_day_id', sa.Uuid(), nullable=True),
                    sa.Column('id', sa.Uuid(), nullable=False),
                    sa.Column('last_modified', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['schedule_day_id'], ['schedule_day.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('ticket')
    op.drop_table('schedule_day')
    op.drop_table('doctor_task')
    op.drop_table('speciality_task')
    op.drop_table('doctor')
    op.drop_table('user')
    op.drop_table('speciality')
