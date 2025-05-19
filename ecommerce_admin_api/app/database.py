from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from ecommerce_admin_api.app.config import settings

# construct db url - standard stuff
db_url = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# create engine with some decent defaults
engine = create_engine(db_url)

# session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for all models
Base = declarative_base()


# db session getter
def get_db():
    # get a new session
    db = SessionLocal()
    try:
        yield db  # for FastAPI dependency injection
    except:
        # rollback if something goes wrong
        db.rollback()
        raise
    finally:
        # always close the session
        db.close()