from pymongo import MongoClient
from datetime import datetime
from config import DATABASE_URL

client = MongoClient(DATABASE_URL)
db = client.Shutterfest
leaderboard = db["leaderboard"]
users = db['users']


def leaderboard_sort():
    results = leaderboard.find()
    leader_list = []
    not_started = []

    for result in results:
        if result['level'] == '-':
            not_started.append((result['points'], result["level"],
                                datetime.strptime(result["last_solved"][:len(result["last_solved"]) - 10],
                                                  '%d/%m/%Y %H:%M:%S'), result["username"], result['_id']))
        else:
            leader_list.append((result['points'], result["level"],
                                datetime.strptime(result["last_solved"][:len(result["last_solved"]) - 10],
                                                  '%d/%m/%Y %H:%M:%S'), result["username"], result['_id']))
    leader_list.sort()
    leader_list.sort(key=lambda x: x[0], reverse=True)  # reverse=True
    #    leader_list = reversed(leader_list)
    leader_list = tuple(leader_list)

    leader_main = []

    for element in leader_list:
        leader_main.append({'points': element[0], 'username': element[3], '_id': element[4], 'level': element[1], 'name': users.find_one({'_id': element[4]})})
    for element in not_started:
        leader_main.append({'points': element[0], 'username': element[3], '_id': element[4], 'level': element[1], 'name': users.find_one({'_id': element[4]})})
    return leader_main
