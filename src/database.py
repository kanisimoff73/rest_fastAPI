from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

check_sequence_query = text("SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = 'task_sid_seq';")

with engine.connect() as connection:
    result = connection.execute(check_sequence_query)
    sequence_exists = bool(result.fetchone())

if not sequence_exists:
    create_sequence_query = text("CREATE SEQUENCE task_sid_seq;")
    with engine.connect() as connection:
        connection.execute(create_sequence_query)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
