import os
from dotenv import load_dotenv
from urllib import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

db_username = str(os.getenv('DATABASE_USERNAME'))
db_password = str(os.getenv('DATABASE_PASSWORD'))
db_host = str(os.getenv('DATABASE_HOST'))
db_port = str(os.getenv('DATABASE_PORT'))
db_name = str(os.getenv('DATABASE_NAME'))

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_username}:{parse.quote(db_password)}@{db_host}:{db_port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=20, max_overflow=0)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

async def get_db():
    # engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=20, max_overflow=0)
    # session_factory = sessionmaker(bind=engine)
    # session = scoped_session(session_factory)
    db = session()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()

    session.remove()