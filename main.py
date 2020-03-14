import requests
import pprint
import time
import json

URL = "https://api.vk.com/method/friends.get"
URL_2 = "https://api.vk.com/method/groups.get"
TOKEN = "73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1"


class User:

    def __init__(self, id):
        self.id = id
        self.link = 'https://vk.com/id' + str(self.id)

    def __str__(self):
        return self.link
    
    def get_friends(self, user_id):
        self.user_id = user_id

        response = requests.get(
            URL, 
            params = { "access_token": TOKEN,
            "v": "5.52",
            "user_id": user_id,
            "fields": ["first_name", "last_name"]
            } 
        )
        
        friends_list = list()
        info = response.json()["response"]
        items = info["items"]

        for detail in items:
            friends_list.append(detail)
        # pprint.pprint(friends_list)
        return friends_list

    def get_groups(self, user_id):
        self.user_id = user_id

        groups_list = list()
        groups_set = set()
        group_dict = dict()

        try: 
            response = requests.get(
            URL_2, 
            params = { "access_token": TOKEN,
            "v": "5.52",
            "user_id": user_id,
            "extended": "1",
            "fields": ["members_count"]
            }
        )
            
            group_info = response.json()["response"]
            group_items = group_info["items"]

            for detail in group_items:
                # print(detail)
                group_name = detail["name"]
                group_id = detail["id"]
                members_count = detail["members_count"]

                group_dict = {"gid": group_id, "name": group_name, "members_count": members_count}
                groups_list.append(group_dict)
                groups_set.add(detail["id"])
            
        except KeyError:
            print('________')
        return groups_list, groups_set

if __name__ == "__main__":
   
    user = User(68070737)
    user_friends_list = user.get_friends(68070737)
    user_groups_list, user_groups_set = user.get_groups(68070737)

    total_groups_set = set()
    total_groups_list = list()

    for friend in user_friends_list:
        group_by_id = user.get_groups(friend['id'])
        total_groups_set.update(group_by_id[1])
        total_groups_list.append(group_by_id[0])
        print('________')
        time.sleep(0.3)
  
    different_groups = user_groups_set.difference(total_groups_set)

    final_list = list()

    for group in user_groups_list:
        if group["gid"] in different_groups:
            final_list.append(group)
    print(final_list)

    with open("groups.json", "w", encoding='utf-8') as f:
        data = final_list
        f.write(json.dumps(data, ensure_ascii=False))