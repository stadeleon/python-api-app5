from dotenv import load_dotenv
import os
import requests
from mailSender import send_email
from pathlib import Path


def prepare_articles_to_send(data_list) -> str:
    context = 'List of articles:\n'
    for article in data_list:
        context += (article['title'] if article['title'] is not None else "") + '\n'
        context += article['description'] + '\n'
        context += f"<a href={article['url']}>link</a>" + 2*'\n'
        download_image(article['urlToImage'])
    return context


def download_image(image_url: str):
    if not image_url:
        return

    image_url = str(image_url.split('?', 1)[0])
    name = Path(image_url).name

    if 'jpeg' in name or ('.jpg' and '.png') not in name:
        name = str(name.split('.', 1)[0]) + '.jpg'

    image_content = requests.get(image_url)
    with open(f"images/{name}", 'wb') as file:
        file.write(image_content.content)


load_dotenv()

api_key = os.getenv('NEWS_API_KEY')
url = f"https://newsapi.org/v2/everything?q=apple&" \
      f"from=2023-06-27&to=2023-06-27&" \
      f"pageSize=20&language=en&" \
      f"sortBy=popularity&apiKey={api_key}"

response = requests.get(url)
if response.status_code == 200:
    content = response.json()
    body = prepare_articles_to_send(content["articles"])
    send_email('leo.leo@my.mail', 'leo.leo@my.mail', body)


