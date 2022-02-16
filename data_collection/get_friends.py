from connectors.vk import VkAPI


api = VkAPI()


def get_friend_info_as_str(friend_info: dict):
    return ','.join([str(value) for value in friend_info.values()])


def collect_friends_of_users(users: list, filename_friends, filename_errors):
    for user_id in users:
        try:
            friends_list = api.get_user_friends(user_id=user_id)
            if not friends_list:
                continue
            for friend in friends_list:
                with open(filename_friends, 'a', encoding='utf-8') as tracks_file:
                    tracks_file.write(f'{user_id},{get_friend_info_as_str(friend)}\n')
        except Exception as ex:
            with open(filename_errors, 'a', encoding='utf-8') as errors_file:
                errors_file.write(f'{user_id},{ex}\n')
