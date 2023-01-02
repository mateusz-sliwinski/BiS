import sqlalchemy
from pandas import DataFrame


def create_engine(name: str) -> sqlalchemy.create_engine:
    engine = sqlalchemy.create_engine(name)
    return engine


def select_data(df: DataFrame, connection: sqlalchemy.create_engine, year: int, month: int, day: int, second_year: int,
                second_month: int, second_day: int,
                save_to_db: bool) -> None:
    if save_to_db:
        if not connection.dialect.has_table(
                connection,
                f'data/wig20_d-{year}-{month}-{day}-do{second_year}-{second_month}-{second_day}.csv'):
            selected = df[
                (df['Data'] > f'{year}-{month}-{day}') & (df['Data'] < f'{second_year}-{second_month}-{second_day}')
                ]

            selected.to_sql(
                f'data/wig20-od-{year}-{month}-{day}-do{second_year}-{second_month}-{second_day}.csv',
                connection
            )
        else:
            print('istnieje tabela o takiej nazwie')

    else:
        print(df[(df['Data'] > f'{year}-{month}-{day}') & (df['Data'] < f'{second_year}-{second_month}-{second_day}')])
