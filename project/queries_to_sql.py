import datetime
import json
import re

import pandas as pd
import sqlalchemy
from matplotlib import pyplot as plt
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError

from project.const import URL_DATABASE
from utils import connect_db, create_engine
from utils import create_tables

meta_data, session, connection = connect_db()
create_tables(connection, meta_data)

dbEngine = create_engine(URL_DATABASE)
connection = dbEngine.connect()


class TypeException(SQLAlchemyError):
    def __init__(self, message):
        self.message = message


def test_select():
    wig = meta_data.tables['wig']
    stmt = select(wig.c.Wolumen).where(wig.c.Wolumen > 200_000_00)
    for wig in session.scalars(stmt):
        print(wig)


# test_select()

def insert_data_to_db(
        Data: str, otwarcie: float, najwyzszy: float, najnizszy: float, zamkniecie: float,
        wolumen: float) -> None:
    wig = meta_data.tables['wig']
    log_table = meta_data.tables['log']
    record = session.query(wig).count()

    regex = re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")

    match = re.match(regex, Data)

    if match:
        add_data = wig.insert().values(
            index=record,
            Data=Data,
            Otwarcie=otwarcie,
            Najwyzszy=najwyzszy,
            Najnizszy=najnizszy,
            Zamkniecie=zamkniecie,
            Wolumen=wolumen
        )

        new_log = log_table.insert().values(
            timestamp=datetime.datetime.now(),
            message=f'add row to wig table {record} {Data} {otwarcie} {najwyzszy} {najnizszy} {zamkniecie} {wolumen}'
        )

        session.execute(new_log)
        session.execute(add_data)
        session.commit()

    else:
        new_log = log_table.insert().values(
            timestamp=datetime.datetime.now(),
            message=f'Invalid date'
        )
        session.execute(new_log)
        session.commit()

        return print("Invalid date, try again")


# insert_data_to_db('2022-12-31', 1797.53, 1797.86, 1786.56, 1792.7, 6736363)


def update_data_to_db(index: int, wolumen: float) -> None:
    wig = meta_data.tables['wig']
    log_table = meta_data.tables['log']

    if index > session.query(wig).count():
        new_log = log_table.insert().values(
            timestamp=datetime.datetime.now(),
            message=f'Error with update {index} {wolumen}'
        )
        session.execute(new_log)
        session.commit()
        raise NoResultFound

    else:
        update_data = wig.update().where(wig.c.index == index).values(Wolumen=wolumen)
        new_log = log_table.insert().values(
            timestamp=datetime.datetime.now(),
            message=f'update row in wig table {index} {wolumen}'
        )
        session.execute(new_log)
        session.execute(update_data)
        session.commit()


# update_data_to_db(1123123312, 15000)


def delete_data_to_db(index: int) -> None:
    wig = meta_data.tables['wig']
    archive = meta_data.tables['archive_table']
    log_table = meta_data.tables['log']

    if index > session.query(wig).count():
        new_log = log_table.insert().values(
            timestamp=datetime.datetime.now(),
            message=f'Error with select and delete {index}'
        )
        session.execute(new_log)
        session.commit()
        raise NoResultFound
    else:
        record = select(
            wig.c.index, wig.c.Data, wig.c.Otwarcie, wig.c.Najwyzszy, wig.c.Najnizszy, wig.c.Zamkniecie,
            wig.c.Wolumen
        ).where(
            wig.c.index == index
        )

        archive_to_table = archive.insert().from_select(
            [
                'index',
                'Data',
                'Otwarcie',
                'Najwyzszy',
                'Najnizszy',
                'Zamkniecie',
                'Wolumen',
            ],
            record
        )

        new_log = log_table.insert().values(timestamp=datetime.datetime.now(), message=f'add row to archive {index}')
        session.execute(new_log)
        session.execute(archive_to_table)

        new_log = log_table.insert().values(timestamp=datetime.datetime.now(), message=f'delete row about {index}')
        session.execute(new_log)
        delete_data = wig.delete().where(wig.c.index == index)
        session.execute(delete_data)
        session.commit()


# delete_data_to_db(3000)


def show_quarter():
    df = pd.read_sql_table('wig', connection)
    del df['index']
    df['Data'] = pd.to_datetime(df['Data'])
    df['quarter'] = df['Data'].dt.to_period('Q')

    df_quarter_add = df.groupby(['quarter']).agg({'Wolumen': 'sum'}).reset_index()
    df_quarter_add['quarter'] = df_quarter_add['quarter'].astype(str)

    df_quarter_add.to_sql(f'quarter', connection, if_exists='replace', index=False)

    df_quarter = df.groupby(['quarter']).agg({'Wolumen': 'sum'})
    df_quarter.plot()
    plt.show()


def show_year():
    df = pd.read_sql_table('wig', connection)
    del df['index']
    df['Data'] = pd.to_datetime(df['Data'])
    year = df['Data'].dt.year
    df['year'] = year.astype(int)

    df_year = df.groupby(['year']).agg({'Wolumen': 'sum'})
    df_year_add = df.groupby(['year']).agg({'Wolumen': 'sum'}).reset_index()
    df_year_add.to_sql(f'year', connection, if_exists='replace', index=False)

    df_year.plot()
    plt.show()


def show_month():
    df = pd.read_sql_table('wig', connection)
    del df['index']
    df['Data'] = pd.to_datetime(df['Data'])
    month = df['Data'].dt.month
    df['month'] = month.astype(int)
    df_month = df.groupby(['month']).agg({'Wolumen': 'sum'})
    df_month_add = df.groupby(['month']).agg({'Wolumen': 'sum'}).reset_index()
    df_month_add.to_sql(f'month', connection, if_exists='replace', index=False)

    df_month.plot()
    plt.show()


show_year()
show_quarter()
show_month()
