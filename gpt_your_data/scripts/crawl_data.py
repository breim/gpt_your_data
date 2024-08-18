import requests
import time
from bs4 import BeautifulSoup

from gpt_your_data.config.database import SessionLocal
from gpt_your_data.repositories.episode_repository import EpisodeRepository

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

def extract_episode_text(episode_number):
    url = f"https://bulbapedia.bulbagarden.net/w/api.php?action=parse&page=EP{episode_number:03d}&format=json"
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        if 'parse' in json_data and 'text' in json_data['parse']:
            html_content = json_data['parse']['text']['*']

            return clean_html(html_content)
        else:
            print(f"Error: {episode_number:03d}")
            return None
    else:
        print(f"Error {url}: Status {response.status_code}")
        return None


def main():
    episode_repo = EpisodeRepository()

    for episode_number in range(1, 276):
        episode_text = extract_episode_text(episode_number)

        if episode_text:
            print(f"EP{episode_number:03d} extraído com sucesso.")
            episode_repo.add_episode(name=str(episode_number), description=episode_text)

        time.sleep(1)

    print("Crawler completed :)")

if __name__ == "__main__":
    main()
