import datetime
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from project.utils import connect_db

meta_data, session, connection = connect_db()

if not meta_data.tables['archive_table'] == meta_data.tables['archive_table']:
    archive_table = Table(
        'archive_table', meta_data,
        Column('index', Integer),
        Column('Data', String),
        Column('Otwarcie', Float),
        Column('Najwyzszy', Float),
        Column('Najnizszy', Float),
        Column('Zamkniecie', Float),
        Column('Wolumen', Float),
    )
    meta_data.create_all()

if not meta_data.tables['log'] == meta_data.tables['log']:
    log = Table(
        'log', meta_data,
        Column('id', Integer, primary_key=True),
        Column('timestamp', String),
        Column('message', String),
    )
    meta_data.create_all()


def test_select():
    wig = meta_data.tables['wig']
    stmt = select(wig.c.Wolumen).where(wig.c.Wolumen > 200_000_00)
    for wig in session.scalars(stmt):
        print(wig)


# test_select()

def insert_data_to_db(Data: str, otwarcie, najwyzszy, najnizszy, zamkniecie, wolumen):
    wig = meta_data.tables['wig']
    log_table = meta_data.tables['log']
    record = session.query(wig).count()

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


# insert_data_to_db('2022-12-31', 1797.53, 1797.86, 1786.56, 1792.7, 6736363)


def update_data_to_db(index, wolumen):
    wig = meta_data.tables['wig']
    log_table = meta_data.tables['log']
    update_data = wig.update().where(wig.c.index == index).values(Wolumen=wolumen)

    new_log = log_table.insert().values(
        timestamp=datetime.datetime.now(),
        message=f'update row in wig table {index} {wolumen}'
    )
    session.execute(new_log)
    session.execute(update_data)
    session.commit()


# update_data_to_db(15, 15000)


def delete_data_to_db(index):
    wig = meta_data.tables['wig']
    archive = meta_data.tables['archive_table']
    log_table = meta_data.tables['log']

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

# delete_data_to_db(7483)
