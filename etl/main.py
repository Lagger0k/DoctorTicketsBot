from sqlalchemy import create_engine

from database.schema.tables import Base

engine = create_engine('sqlite://', echo=True)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
