from datetime import datetime
from datetime import date

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy.sql import func


class LastModifiedMixin:
    last_modified: Mapped[datetime] = mapped_column(onupdate=func.utc_timestamp())


class TaskMixin:
    day: Mapped[date] = mapped_column(nullable=False, comment='День приёма')
    completed: Mapped[bool] = mapped_column(default=False, comment='Поиск завершен')
    cancelled: Mapped[bool] = mapped_column(default=False, comment='Поиск отменён')
