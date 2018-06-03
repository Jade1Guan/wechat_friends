#coding = utf-8
# author: Jade

import json

import itchat
import requests

sex_dict = {}
sex_dict['0'] = "other"
sex_dict['1'] = "male"
sex_dict['2'] = "female"

# 下载好友头像


def download_images(friends_list):
    image_dir = "./images/"
    num = 1
    for friend in friends_list:
        iamge_name = str(num) + '.jpg'
        num += 1
        img = itchat.get_head_img(userName=friend["UserName"])
        with open(image_dir + iamge_name, 'wb') as file:
            file.write(img)


def save_data(friends_list):
    out_file_name = "./data/friends.json"
    with open(out_file_name, 'w') as json_file:
        json_file.write(json.dumps(friends_list, ensure_ascii=False))


if __name__ == '__main__':
    itchat.auto_login()

    friends = itchat.get_friends(update=True)[0:]
    friends_list = []

    for friend in friends:
        item = {}
        item['NickName'] = friend['NickName']
        item['HeadImgUrl'] = friend['HeadImgUrl']
        item['sex'] = sex_dict[str(friend['Sex'])]
        item['Province'] = friend['Province']
        item['Signature'] = friend['Signature']
        item['UserName'] = friend['UserName']

        friends_list.append(item)

    save_data(friends_list)
    download_images(friends_list)

    itchat.run()
