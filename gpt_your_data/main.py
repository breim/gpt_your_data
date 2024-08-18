import uvicorn
from fastapi import FastAPI, Body, HTTPException
from gpt_your_data.models.episode import Episode
from gpt_your_data.repositories.episode_repository import EpisodeRepository
from gpt_your_data.services.chat_gpt_service import ChatGPTService

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/episodes/")
def create(name: str = Body(...), description: str = Body(...)):
    episode_repo = EpisodeRepository()

    created_episode= episode_repo.add_episode(name=name, description=description)
    return created_episode

@app.get("/search/")
def search(query: str):
    episode_repo = EpisodeRepository()
    chatgpt_service = ChatGPTService()
    query_vector = episode_repo.extract_vector(episode_description=query)
    distances, indexes = episode_repo.search_episode_by_vector(query_vector, top_k=3)
    
    results = []
    for i, idx in enumerate(indexes[0]):
        if distances[0][i] <= 40:
            convert_idx = int(idx) + 1 # It's good put the relative faiss_id in a field table on your database.
            pokemon = episode_repo.db.query(Episode).get(convert_idx) # read above.
            
            if pokemon:
                result = {
                    "pokemon": pokemon,
                    "distance": float(distances[0][i])
                }
                results.append(result)

    if not results:
        raise HTTPException(status_code=404, detail="No Pokemon found matching the query")

    return chatgpt_service.generate_response(prompt=query, semantic_result=results)

def start():
    uvicorn.run("gpt_your_data.main:app", host="0.0.0.0", port=8001, reload=True)
