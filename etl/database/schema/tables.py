from datetime import date
from typing import List
from typing import Optional
from uuid import uuid4
from uuid import UUID

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr

from database.schema.mixins import TaskMixin
from database.schema.mixins import LastModifiedMixin


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class User(Base):
    """
    Пользователь сервиса.
    """

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    doctor_tasks: Mapped[Optional[List['DoctorTask']]] = relationship(
        back_populates='user'
    )
    speciality_tasks: Mapped[Optional[List['SpecialityTask']]] = relationship(
        back_populates='user'
    )


class Speciality(Base, LastModifiedMixin):
    """
    Специальность врача.
    """

    title: Mapped[str] = mapped_column(
        String(100), nullable=True, comment='Специальность'
    )
    code: Mapped[int] = mapped_column(nullable=True, comment='Код специальности')
    doctors: Mapped[List['Doctor']] = relationship(back_populates='speciality')

    tasks: Mapped[Optional[List['SpecialityTask']]] = relationship(
        back_populates='speciality'
    )


class Doctor(Base, LastModifiedMixin):
    """
    Врач, ведущий приём.
    """

    first_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='Имя')
    last_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment='Фамилия'
    )
    middle_name: Mapped[str] = mapped_column(
        String(100), nullable=True, comment='Отчество'
    )
    department: Mapped[int] = mapped_column(nullable=True, comment='Департамент')
    hospital: Mapped[int] = mapped_column(nullable=True, comment='Учреждение')

    schedule_days: Mapped[List['ScheduleDay']] = relationship(back_populates='doctor')

    speciality_id: Mapped[Optional[str]] = mapped_column(ForeignKey('speciality.id'))
    speciality: Mapped[Optional['Speciality']] = relationship(back_populates='doctors')

    tasks: Mapped[Optional[List['DoctorTask']]] = relationship(back_populates='doctor')


class ScheduleDay(Base, LastModifiedMixin):
    """
    Приёмный день.
    """

    __tablename__ = 'schedule_day'
    day: Mapped[date] = mapped_column(nullable=False, comment='День приёма')
    is_working_day: Mapped[bool] = mapped_column(default=False, comment='Ведется приём')

    doctor_id = mapped_column(ForeignKey('doctor.id'))
    doctor: Mapped['Doctor'] = relationship(back_populates='schedule_days')

    tickets: Mapped[Optional[List['Ticket']]] = relationship(
        back_populates='schedule_day'
    )


class Ticket(Base, LastModifiedMixin):
    """
    Талон на приём к врачу.
    """

    time: Mapped[str] = Column(String(32), nullable=False, comment='Время приёма')
    type: Mapped[int] = mapped_column(nullable=False, comment='Тип талона')
    code: Mapped[int] = mapped_column(nullable=False, comment='Код талона')
    is_free: Mapped[bool] = mapped_column(default=False, comment='Талон свободен')

    schedule_day_id: Mapped[Optional[str]] = mapped_column(
        ForeignKey('schedule_day.id')
    )
    schedule_day: Mapped[Optional['ScheduleDay']] = relationship(
        back_populates='tickets'
    )


class DoctorTask(Base, LastModifiedMixin, TaskMixin):
    """
    Задача на поиск талонов по врачу, на конкретный день, для пользователя.
    """

    __tablename__ = 'doctor_task'

    doctor_id: Mapped[Optional[str]] = mapped_column(ForeignKey('doctor.id'))
    doctor: Mapped[Optional['Doctor']] = relationship(back_populates='tasks')

    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey('user.id'))
    user: Mapped[Optional['User']] = relationship(back_populates='doctor_tasks')


class SpecialityTask(Base, LastModifiedMixin, TaskMixin):
    """
    Задача на поиск талонов по специальности врача, на конкретный день, для пользователя.
    """

    __tablename__ = 'speciality_task'

    speciality_id: Mapped[Optional[str]] = mapped_column(ForeignKey('speciality.id'))
    speciality: Mapped[Optional['Speciality']] = relationship(back_populates='tasks')

    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey('user.id'))
    user: Mapped[Optional['User']] = relationship(back_populates='speciality_tasks')
