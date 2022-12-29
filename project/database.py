import pandas as pd
import sqlalchemy
from validate_data import type_validate,check_nan_values


def create_engine(name: str) -> sqlalchemy.create_engine:
    engine = sqlalchemy.create_engine(name)
    return engine


url_database = 'postgresql+psycopg2://postgres:admin@localhost/postgres'
dbEngine = create_engine(url_database)
connection = dbEngine.connect()

df = pd.read_csv('data/wig20_d.csv')
df = type_validate(df)
df = check_nan_values(df)
if not connection.dialect.has_table(connection, 'wig'):
    df.to_sql('wig', dbEngine)

print(df)
