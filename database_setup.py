from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class airline(Base):
    __tablename__ = 'airline'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Returns object for json format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class equipment(Base):
    __tablename__ = 'equipment'
    """ equipment is referring to which aircraft the respective airline is using"""
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    airline_id = Column(Integer, ForeignKey('airline.id'))
    airlinerelation = relationship(airline)

    @property
    def serialize(self):
        """Return object for json format"""
        return {
            'name': self.name,
            'id': self.id,
            
        }
engine = create_engine('sqlite:///airline.db')

Base.metadata.create_all(engine)
