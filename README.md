
# GPT-Your-Data

The purpose of this project is to demonstrate how to work with your existing database by implementing a semantic search using the FAISS vector database. GPT-Your-Data utilizes FastAPI, SQLAlchemy, FAISS, and OpenAI's GPT model to create and manage a database of Pokémon episodes, incorporating a vector-based semantic search functionality.

[Video](./assets/video.mp4)

## Key Features

- **Vector Search with FAISS**: Use the FAISS service to index and search Pokémon episodes based on vector representations of episode descriptions.
- **GPT Integration**: Generate contextual responses to queries using the GPT model, integrating semantic search results from FAISS.
- **Web Scraping**: Automatically extract content from Pokémon episodes from online sources and store it in the database.
- **REST API with FastAPI**: Expose endpoints to create new episodes, search episodes by semantic similarity, and integrate with GPT to generate answers to questions based on episode content.

## Project Structure


## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/breim/gpt-your-data.git
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
## Install the data transformers
```bash
pip install -U sentence-transformers
```

## Database Setup

The project uses SQLite by default. The `session.py` file configures the database connection. To initialize the database:

```bash
python -m gpt_your_data.db.init_db
```

This will create the necessary tables in your SQLite database.

## Running the Application

To start the FastAPI application, use:

```bash
poetry run start
```

The application will be available at `http://localhost:8001`.

## Using the API

### Create an Episode

- **Endpoint**: `POST /episodes/`
- **Parameters**: 
  - `name`: The name or identifier of the episode.
  - `description`: A detailed description of the episode.

### Search Episodes by Semantic Similarity

- **Endpoint**: `GET /search/`
- **Parameters**: 
  - `query`: A text query to search for similar episodes.

## Web Scraping

The project includes a web scraping script to extract Pokémon episode content:

```bash
python -m gpt_your_data.scripts.scrape_episodes
```

This script will fetch and store the content of the episodes in the database.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
