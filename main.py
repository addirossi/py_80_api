import os
import time
from pprint import pprint

import pandas as pd
import requests
from dotenv import load_dotenv


load_dotenv()


class VkApiHandler:

    base_url = 'https://api.vk.com/method/'

    def __init__(self, access_token, version='5.131'):
        self.params = {
            'access_token': access_token,
            'v': version
        }

    def get_user_data(self, user_ids):
        method_name = f'{self.base_url}users.get'
        params = {'user_ids': user_ids}.update(self.params)
        response = requests.get(method_name, params=params)
        data = response.json()
        return data

    def get_user_data_extended(self, user_ids, fields):
        method_name = f'{self.base_url}users.get'
        params = {'user_ids': user_ids, 'fields': fields, **self.params}
        response = requests.get(method_name, params=params)
        data = response.json()
        return data

    def search_groups(self, q, sort, count):
        url = self.base_url + 'groups.search'
        params = {'q': q, 'sort': sort, 'count': count, **self.params}
        response = requests.get(url, params=params)
        data = response.json()
        return data['response']

    def search_news(self, q):
        url = self.base_url + 'newsfeed.search'
        params = {'q': q, 'count': 2, **self.params}
        # news_frame = pd.DataFrame()
        news = []
        while True:
            time.sleep(0.34)
            response = requests.get(url, params=params)
            data = response.json()
            # news_frame = pd.concat([news_frame, pd.DataFrame(data['response']['items'])])
            news.extend(data['response']['items'])
            if 'next_from' in data['response']:
                params.update({'start_from': data['response']['next_from']})
            else:
                break
            # return news_frame
            print(len(news))
            # return news


if __name__ == '__main__':
    # with open('token.txt', 'r') as token_file:
    #     token = token_file.readline()

    vk_token = os.getenv('VK_API_TOKEN')
    version = os.getenv('VERSION')

    vk = VkApiHandler(vk_token, version)

    # data = vk.get_user_data(token, '1')
    # user_data = vk.get_user_data_extended('1,2,3', 'bdate,city,followers_count')
    # groups = vk.search_groups('авто', 6, 10)
    # assert len(groups['items']) == 10
    # pd.DataFrame(groups['items'])
    news = vk.search_news('авто')
    pprint(news, indent=4)
