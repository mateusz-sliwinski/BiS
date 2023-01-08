import urllib.request
from pandas import DataFrame
import pandas as pd


def validate_download(url: urllib.request, year: int, month: int, day: int) -> urllib.request:
    try:
        url = urllib.request.urlretrieve(url, f'data/wig20_d-{year}-{month}-{day}.csv')
    except FileExistsError:
        raise FileExistsError("This url probably doesn't exist")
    return url


def type_validate(df: DataFrame) -> DataFrame:
    try:
        pd.to_datetime(df['Data'], format='%Y-%m-%d', errors='raise')
    except ValueError:
        raise ValueError('Incorrect data format, should be YYYY-MM-DD')

    try:
        df['Otwarcie'] == df['Otwarcie'].astype(float)
    except ValueError:
        raise ValueError('Incorrect Otwarcie format, should be float')

    try:
        df['Najwyzszy'] == df['Najwyzszy'].astype(float)
    except ValueError:
        raise ValueError('Incorrect Najwyzszy format, should be float')

    try:
        df['Najnizszy'] == df['Najnizszy'].astype(float)
    except ValueError:
        raise ValueError('Incorrect Najnizszy format, should be float')

    try:
        df['Zamkniecie'] == df['Zamkniecie'].astype(float)
    except ValueError:
        raise ValueError('Incorrect Zamkniecie format, should be float')

    try:
        df['Wolumen'] == df['Wolumen'].astype(float)
    except ValueError:
        raise ValueError('Incorrect Wolumen format, should be float')

    return df


def check_nan_values(df: DataFrame) -> DataFrame:
    if not df.isnull().values.any():
        return df
    else:
        raise ValueError('Dataset have NaN values')
