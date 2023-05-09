from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from prizepicks_scraper import env_variables

if env_variables.ENV == "LOCAL":
    engine = create_engine("sqlite+pysqlite:///nba_stats.db")
else:
    # this will only work if you are on a pythonanywhere machine
    url_object = URL.create(
        "mysql+pymysql",
        username=env_variables.PROD_USER,
        password=env_variables.PROD_PASSWORD,
        host=env_variables.PROD_HOST,
        database=env_variables.PROD_DB,
    )
    print(f"Connecting to db: {url_object}")
    engine = create_engine(url_object)

Session = sessionmaker(bind=engine)
session = Session()
