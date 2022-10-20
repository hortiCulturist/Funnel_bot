import pandas as pd
import sqlite3
import config


def excel():
    con = sqlite3.connect(config.path_to_db)
    df = pd.read_sql('SELECT * FROM data', con)
    df.to_excel(config.path_to_result, index=False)
