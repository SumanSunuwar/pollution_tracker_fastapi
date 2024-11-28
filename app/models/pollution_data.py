from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
# from app.models import Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PollutionData(Base):
    __tablename__ = "pollution_data"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    air_quality_index: Mapped[int] = mapped_column(nullable=False)
    water_quality_index: Mapped[int] = mapped_column(nullable=False)
    ph_level: Mapped[float] = mapped_column(nullable=False)
    temperature: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(default=func.now())

    def __repr__(self):
        return f"<PollutionData(id={self.id}, air_quality_index={self.air_quality_index}, temperature={self.temperature}, date={self.date})>"
