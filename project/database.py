import pandas as pd
import sqlalchemy

from validate_data import validate


def create_engine(name: str) -> sqlalchemy.create_engine:
    engine = sqlalchemy.create_engine(name)
    return engine


url_database = 'postgresql+psycopg2://postgres:admin@localhost/postgres'

dbEngine = create_engine(url_database)

connection = dbEngine.connect()

df = pd.read_csv('data/wig20_d.csv')

validate(df)

if not connection.dialect.has_table(connection, 'wig'):
    df.to_sql('wig', dbEngine)

print(df)
