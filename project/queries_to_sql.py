from sqlalchemy import select
from sqlalchemy import insert
from sqlalchemy import func
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


def test_select():
    wig = meta_data.tables['wig']
    stmt = select(wig.c.Wolumen).where(wig.c.Wolumen > 200_000_00)
    for wig in session.scalars(stmt):
        print(wig)


# test_select()

def insert_data_to_db():
    wig = meta_data.tables['wig']
    record = session.query(wig).count()

    add_data = wig.insert().values(
        index=record,
        Data='2022-12-30',
        Otwarcie=1797.53,
        Najwyzszy=1797.86,
        Najnizszy=1786.56,
        Zamkniecie=1792.7,
        Wolumen=6736363
    )

    session.execute(add_data)
    session.commit()


# insert_data_to_db()


def update_data_to_db():
    wig = meta_data.tables['wig']
    update_data = wig.update().where(wig.c.index == 7480).values(Wolumen=1)

    session.execute(update_data)
    session.commit()


# update_data_to_db()

def delete_data_to_db():
    wig = meta_data.tables['wig']
    archive_table = meta_data.tables['archive_table']

    record = select(wig.c.index, wig.c.Data, wig.c.Otwarcie, wig.c.Najwyzszy, wig.c.Najnizszy, wig.c.Zamkniecie,
                    wig.c.Wolumen).where(wig.c.index == 7483)
    xd = archive_table.insert().from_select(
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
    session.execute(xd)

    delete_data = wig.delete().where(wig.c.index == 7483)
    session.execute(delete_data)
    session.commit()


delete_data_to_db()
