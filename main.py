from dotenv import load_dotenv
import os
import requests
from mailSender import send_email


def prepare_articles_to_send(data_list) -> str:
    context = 'List of articles:\n'
    for article in data_list:
        context += (article['title'] if article['title'] is not None else "") + '\n'
        context += article['description'] + '\n'
        context += f"<a href={article['url']}>link</a>" + 2*'\n'

    return context


load_dotenv()

api_key = os.getenv('NEWS_API_KEY')
# url = "https://finance.yahoo.com"
url = f"https://newsapi.org/v2/everything?q=apple&" \
      f"from=2023-06-27&to=2023-06-27&" \
      f"pageSize=20&language=en&" \
      f"sortBy=popularity&apiKey={api_key}"

requests = requests.get(url)
content = requests.json()

body = prepare_articles_to_send(content["articles"])
send_email('leo.leo@my.mail', 'leo.leo@my.mail', body)