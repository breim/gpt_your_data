from gpt_your_data.config.database import engine, Base
from gpt_your_data.models.episode import Episode

def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
