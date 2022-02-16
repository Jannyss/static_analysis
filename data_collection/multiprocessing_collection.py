import multiprocessing as mp
import pandas as pd
from topic_modelling.data_collection.get_friends import collect_friends_of_users


def run(users, processes_num=mp.cpu_count()):
    users_batch_size = len(users) // processes_num
    users_batches = []
    j = users_batch_size
    for k in range(processes_num):
        i = users_batch_size * k
        users_batches.append(users[i:j])
        j = users_batch_size * (k + 2)

    pool = mp.Pool(processes_num)
    a = [pool.apply(collect_friends_of_users,
               args=(users_batches[i], f'../data/friends/friends_{i+2}', f'../data/friends/friends_errors_{i+2}')) for i in range(processes_num)]
    pool.close()


users_df = pd.read_csv('../data/users_activities_groups.csv')
users_list = list(users_df['user_id'].values)[600:]
run(users_list)
