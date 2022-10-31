from src.models import create_engine,sessionmaker
import sqlalchemy.ext.declarative as declarative
from pymysql.constants.CLIENT import MULTI_STATEMENTS
from sqlalchemy.orm import scoped_session
# from dotenv.
 
SQLALCHEMY_DATABASE_URL = "mysql://skillhub_fastapi:fastapipassword@localhost/skillhub_fastapi_backend"

engine  = create_engine(SQLALCHEMY_DATABASE_URL,connect_args={"client_flag":MULTI_STATEMENTS})

SessionLocal = sessionmaker(autocommit=False, autoflush=True,bind=engine)
Base = declarative.declarative_base()
SessionNow = scoped_session(SessionLocal)
