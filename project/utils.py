import sqlalchemy


def create_engine(name: str) -> sqlalchemy.create_engine:
    engine = sqlalchemy.create_engine(name)
    return engine
