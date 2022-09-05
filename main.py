import argparse
import requests

from urllib.parse import urlparse
from environs import Env

parser = argparse.ArgumentParser()
parser.add_argument("url")


env = Env()
env.read_env()


def shorten_link(token, url):
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        json={'long_url': url},
        headers={'Authorization': f'Bearer {token}'}
    )
    response.raise_for_status()

    return response.json()['link']


def count_clicks(token, url):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}/{parsed_url.path}'
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary',
        headers={'Authorization': f'Bearer {token}'},
        params={'units': -1}
    )
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(token, url):
    parsed_url = urlparse(url)
    bitlink = f'{parsed_url.netloc}/{parsed_url.path}'
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}',
        headers={'Authorization': f'Bearer {token}'}
    )

    return response.ok


def main():
    url = parser.parse_args().url
    token = env.str('BITLY_TOKEN')
    if is_bitlink(token, url):
        print(f"Количество переходов по ссылке bitly: {count_clicks(token, url)}")
    else:
        print(f"Битлинк: {shorten_link(token, url)}")


if __name__ == '__main__':
    main()
