import datetime
import uuid
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from prizepicks_scraper.db import engine
Base = declarative_base()


class PrizePicksProjection(Base):
    """
    Prize Pick Bet
    """
    __tablename__ = "prizepicks_projections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    line = Column(Integer)
    bet_type = Column(String)
    img = Column(String)
    timestamp = Column(Date, default=datetime.datetime.now().date())

    def as_dict(self):
        return {
            "name": self.name,
            "line": self.line,
            "bet_type": self.bet_type,
            "timestamp": self.timestamp
        }


Base.metadata.create_all(engine)
