from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import airline, Base, equipment

engine = create_engine("sqlite:///airline.db")

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

airline1 = airline(name="America Airlines")

session.add(airline1)
session.commit()

equipment1 = equipment(name="Boeing 707",airlinerelation=airline1 )
session.add(equipment1)
session.commit()
