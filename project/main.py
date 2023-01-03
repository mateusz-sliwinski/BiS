import os
import pandas as pd
from const import URL_DATABASE
from utils import create_engine
from utils import run_predict
import warnings
warnings.filterwarnings('ignore')
os.system('python database.py')

dbEngine = create_engine(URL_DATABASE)
connection = dbEngine.connect()

print(dbEngine.table_names())

df = pd.read_sql_table(input(), connection)

run_predict(True, df)
