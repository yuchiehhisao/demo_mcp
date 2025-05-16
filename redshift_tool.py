import time
import logging
import pandas as pd
import sqlalchemy
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from dotenv import load_dotenv

load_dotenv()


class ReshiftHandler:
    def __init__(self):
        self.host = 'taycan-redshift-cluster.cxoftjoutn2e.ap-northeast-1.redshift.amazonaws.com'
        self.database = getenv("REDSHIFT_DB")
        self.port = 5439
        self.user = getenv("REDSHIFT_USER")
        self.password = getenv("REDSHIFT_PASSWORD")
        # self.engine = create_engine(
        #     f"redshift+redshift_connector://{self.user}:{self.password}@taycan-redshift-cluster.cxoftjoutn2e.ap-northeast-1.redshift.amazonaws.com:5439/{self.database}"
        # )
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

        self.logger = logging.getLogger(__name__)

    def do_sql(self, sql):
        try:
            with self.engine.connect() as conn:
                return conn.execute(sql)
        except Exception as e:
            print(e)


    def read_from_redshift(self, sql_string):
        return pd.read_sql(sql_string, con=self.engine.connect())