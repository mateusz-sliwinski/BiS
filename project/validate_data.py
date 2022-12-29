import urllib.request

from pandas import DataFrame


def validate_download(url):
    try:
        url = urllib.request.urlretrieve(url, 'data/wig20_d.csv')
    except FileExistsError:
        print("this url probably doesn't exist")

    return url


def validate(df: DataFrame) -> DataFrame:
    pass
