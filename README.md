
# GPT-Your-Data

**GPT-Your-Data** is a project that uses FastAPI and SQLAlchemy to create and manage a database of episodes, in addition to integrating a vector search service using FAISS. The project is managed with Poetry, which facilitates dependency installation and virtual environment management.

## Project Structure

```plaintext
gpt-your-data/
├── gpt_your_data/
│   ├── models/
│   │   ├── episode.py             # Episode model definition
│   ├── repositories/
│   │   ├── episode_repository.py  # Repository for managing episodes
│   ├── services/
│   │   ├── faiss_service.py       # FAISS service for vector search
│   ├── db/
│   │   ├── base.py                # SQLAlchemy Base definition
│   │   ├── session.py             # Database configuration and sessionmaker
│   │   ├── init_db.py             # Script to create tables in the database
│   ├── main.py                    # FastAPI application entry point
├── pyproject.toml                 # Poetry configuration
└── README.md                      # Project documentation
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/gpt-your-data.git
   cd gpt-your-data
   ```

2. **Install dependencies using Poetry:**

   Make sure you have Poetry installed on your machine.

   ```bash
   poetry install
   ```

3. **Activate Poetry's virtual environment:**

   ```bash
   poetry shell
   ```

## Database Setup

The project uses SQLite by default. The `session.py` file contains the database configuration:

```python
# gpt_your_data/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## Creating Tables

To create the tables in the database, run the following command:

```bash
poetry run create-tables
```

This command runs the `init_db.py` script, which creates all the tables defined in the SQLAlchemy models.

## Using the Episode Repository

The `EpisodeRepository` manages the persistence and retrieval logic for episodes, as well as integrating with FAISS for vector searches. It is configured to automatically initialize the database session if one is not passed.

Usage example:

```python
from gpt_your_data.repositories.episode_repository import EpisodeRepository

def main():
    episode_repo = EpisodeRepository()
    episode_number = 1
    episode_text = "Episode description"

    episode_repo.add_episode(name=str(episode_number), description=episode_text)
    print("Episode added successfully!")

if __name__ == "__main__":
    main()
```

## Running the FastAPI Server

To start the FastAPI server, simply run:

```bash
poetry run start-webserver
```

The server will be available at `http://127.0.0.1:8000`.

## Episode Model Structure

The `Episode` model represents an episode with a name and description. It is defined in `episode.py`:

```python
# gpt_your_data/models/episode.py

from sqlalchemy import Column, Integer, String, Text
from gpt_your_data.db.base import Base

class Episode(Base):
    __tablename__ = 'episodes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
```

## FAISS Integration

The project uses FAISS for efficient vector searches. The FAISS service is managed by the `FaissService` class, which can be found in `faiss_service.py`. The `EpisodeRepository` uses this service to index episode descriptions and perform vector searches.

## Contributing

Feel free to submit PRs and report issues. This project is a work in progress, and any contributions are welcome!

## License

This project is licensed under the MIT License.
