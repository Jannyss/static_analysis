import re
import requests

from vk_api.audio import VkAudio
from vk_api.vk_api import VkApi


LOGIN = ''
PASSWORD = ''



class VkAPI:

    def __init__(self):
        self.access_token = ''
        self.domain = "https://api.vk.com/method"
        self.version = "5.141"

        self.vk = VkApi(login=LOGIN, password=PASSWORD)
        self.vk.auth()
        self.vk_api = self.vk.get_api()

        # self.vk_audio = VkAudio(self.vk)

    def get_user_account(self, username):
        query_params = {
            'domain': self.domain,
            'access_token': self.access_token,
            'user_ids': username,
            'fields': 'photo_200,about,followers_count,counters,screen_name',
            'v': self.version
        }

        r = requests.get("{domain}/users.get?access_token={access_token}&user_ids={user_ids}&fields={fields}&v={v}"
                         .format(**query_params))
        response = r.json()['response'][0]
        return {"user_id": response["id"],
                "username": response["screen_name"],
                "name": response["first_name"] + " " + response["last_name"],
                "profile_pic_url": response["photo_200"],
                "followers": response["followers_count"]
                }
    
    def get_user_info(self, user_id):
        return self.vk_api.users.get(user_ids=f'{user_id}', fields='city,country,bdate')

    def get_user_friends(self,
                         user_id=None,
                         fields=('bdate', 'city', 'contacts', 'country', 'nickname', 'sex', 'status')):
        friends = self.vk_api.friends.get(user_id=user_id, fields=list(fields))
        if friends:
            return friends['items']

    def is_friendship_between(self, user_id_first, user_id_second):
        friends_first_user = self.get_user_friends(user_id=user_id_first)
        if friends_first_user:
            return user_id_second in friends_first_user
        else:
            return

    def get_music_list(self, user_id=None, username=None):
        if not user_id:
            user_id = self._get_user_id_by_username(username)
        tracks = self.vk_audio.get(owner_id=user_id)
        return tracks

    def _get_user_id_by_username(self, username):
        query_params = {
            'domain': self.domain,
            'access_token': self.access_token,
            'user_ids': username,
            'v': self.version
        }
        r = requests.get(
            "{domain}/users.get?access_token={access_token}&user_ids={user_ids}&v={v}".format(
                **query_params))
        response = r.json()['response'][0]
        return response['id']

    def _get_mentions(self, post_text):
        mentions = []
        positions = []
        if post_text:
            re.escape('[]|')
            mention_id = re.compile(r'\[(\w*)\|')
            mention_name = re.compile(r'\|([a-zA-Zа-яА-Я ]*)\]')
            account_ids = mention_id.findall(post_text)
            account_names = mention_name.findall(post_text)
            if account_ids:
                new_post_text = post_text.replace('[', '').replace(']', '').replace('|', '')
                for account_id in account_ids:
                    new_post_text = new_post_text.replace(account_id, '')
                for account_name in account_names:
                    m = re.search(account_name, new_post_text)
                    positions.append(m.span())
                for account, pos in zip(account_ids, positions):
                    mentions.append({'name': account,
                                     'pos_start': pos[0],
                                     'pos_end': pos[1]-1})
            return mentions
        else:
            return []

    def get_user_posts(self, user_id):
        return self.vk_api.wall.get(owner_id=user_id)

    def get_user_post(self, username, posts_number=1):
        user_id = self._get_user_id_by_username(username)
        posts_list = []
        query_params = {
            'domain': self.domain,
            'access_token': self.access_token,
            'owner_id': user_id,
            # 'count': posts_number,
            'v': self.version
        }
        r = requests.get("{domain}/wall.get?access_token={access_token}&owner_id={owner_id}&count={count}&v={v}".format(**query_params))
        response = r.json()['response']
        for post in response["items"]:
            attachments = []
            if "attachments" in post:
                for attach in post["attachments"]:
                    if attach["type"] == 'photo':
                        attachments.append(attach["photo"]["sizes"][3]["url"])
            mentions = self._get_mentions(post['text'])
            if mentions:
                post_text = post["text"].replace('[', '').replace(']', '').replace('|', '')
                for mention in mentions:
                    post_text = post_text.replace(mention['name'], '')
                    mention["name"] = mention["name"].replace("id", "")
            else:
                post_text = post["text"]
            posts_list.append({'link': "https://vk.com/" + username + "?w=wall" + str(post["from_id"]) + "_" + str(post["id"]),
                               'likes': post["likes"]["count"],
                               'comments': post["comments"]["count"],
                               'shares': post["reposts"]["count"],
                               'views': post["views"]["count"],
                               'text': post_text,
                               'attachment_link': attachments,
                               'datetime': post["date"],
                               'mentions': mentions})
        return posts_list

# v = VkAPI()

