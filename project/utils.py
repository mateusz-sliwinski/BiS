import pickle
import pandas as pd
import sqlalchemy
from matplotlib import pyplot as plt
from pandas import DataFrame
from boar.running import run_notebook


def create_engine(name: str) -> sqlalchemy.create_engine:
    engine = sqlalchemy.create_engine(name)
    return engine


def select_data(df: DataFrame, connection: sqlalchemy.create_engine, year: int, month: int, day: int, second_year: int,
                second_month: int, second_day: int,
                save_to_db: bool) -> None:
    if save_to_db:
        if not connection.dialect.has_table(
                connection,
                f'data/wig20_od-{year}-{month}-{day}-do{second_year}-{second_month}-{second_day}.csv'):
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


def df_plot_history(x, y, title="", xlabel='Date', ylabel='Value', dpi=100):
    plt.figure(figsize=(16, 5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()


def convert_data_set(df: DataFrame) -> DataFrame:
    df['Data'] = pd.to_datetime(df['Data'])
    df = df.tail(3)
    add_split_date(df)
    dane = df[['year', 'month', 'day', 'Otwarcie', 'Najwyzszy', 'Najnizszy', 'Wolumen', 'Zamkniecie']]
    return dane


def predict_tomorrow(dane: DataFrame) -> None:
    loaded_model = pickle.load(open('Reg', 'rb'))
    result = loaded_model.predict(dane.values)
    last_element = result[-1]
    print(f'{last_element}')


def run_predict(notebook_run: bool, df: DataFrame) -> None:
    if notebook_run:
        run_notebook('regression.ipynb')

    df_last_three_record = convert_data_set(df)
    predict_tomorrow(df_last_three_record)


def add_split_date(df: DataFrame) -> DataFrame:
    df['Data'] = pd.to_datetime(df['Data'])
    year = df['Data'].dt.year
    month = df['Data'].dt.month
    day = df['Data'].dt.day
    df['year'] = year.astype(int)
    df['month'] = month.astype(int)
    df['day'] = day.astype(int)
    return df
