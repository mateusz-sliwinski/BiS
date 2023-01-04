from sqlalchemy import select, insert, func

from project.utils import connect_db

meta_data, session = connect_db()


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
        index=record - 1,
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
