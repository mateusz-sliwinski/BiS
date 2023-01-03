import pandas as pd
from utils import create_engine
from date import day
from date import month
from date import year
from validate_data import type_validate
from validate_data import check_nan_values
from validate_data import validate_download
from const import URL
from const import URL_DATABASE

validate_download(URL, year, month, day)

dbEngine = create_engine(URL_DATABASE)
connection = dbEngine.connect()

df = pd.read_csv(f'data/wig20_d-{year}-{month}-{day}.csv')
df = type_validate(df)
df = check_nan_values(df)

if not connection.dialect.has_table(connection, f'data/wig20_d-{year}-{month}-{day}.csv'):
    df.to_sql(f'data/wig20_d-{year}-{month}-{day}.csv', connection)

