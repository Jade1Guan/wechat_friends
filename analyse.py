#coding = utf-8
#author: jade

import json
from pyecharts import Bar
from pyecharts import Grid
from pyecharts import WordCloud
from pyecharts import Pie
from pyecharts import Map
from collections import Counter
import jieba.analyse
import PIL.Image as Image
import os
import math

def get_pie(item_name, item_name_list, item_num_list):
    totle = item_num_list[0] + item_num_list[1] + item_num_list[2]
    subtitle = "共有%d个好友" %totle

    pie = Pie(item_name, page_title = item_name, title_text_size = 30, title_pos = 'center',\
        subtitle = subtitle, subtitle_text_size = 25, width = 800, height = 800)
    
    pie.add("", item_name_list, item_num_list, is_label_show = True, center = [50, 45], radius = [0, 50],\
        legend_pos = 'left', legend_orient = 'vertical', label_text_size = 20)

    out_file_name = './analyse/' + item_name + '.html' 
    pie.render(out_file_name)

def word_cloud(item_name,item_name_list,item_num_list,word_size_range):
    
    wordcloud = WordCloud(width=1400,height= 900)
    
    wordcloud.add("", item_name_list, item_num_list,word_size_range=word_size_range,shape='pentagon')
    out_file_name = './analyse/'+item_name+'.html'
    wordcloud.render(out_file_name)

def get_item_list(first_item_name, dict_list):
    item_name_list = []
    item_num_list = []
    i = 0
    for item in dict_list:
        i += 1
        if i >= 15:
            break
        
        for name,num in item.items():
            if name != first_item_name:
                item_name_list.append(name)
                item_num_list.append(num)

        return item_name_list, item_num_list

def dict2list(_dict):
    name_list = []
    num_list = []

    for key, value in _dict.items():
        name_list.append(key)
        num_list.append(value)

    return name_list,num_list

def counter2list(_counter):
    name_list = []
    num_list = []

    for item in _counter:
        name_list.append(item[0])
        num_list.append(item[1])

    return name_list,
    
def get_tag(text, cnt):
    print('正在分析句子：', text)
    tag_list = jieba.analyse.extract_tags(text)
    for tag in tag_list:
        cnt[tag] += 1


if __name__ == '__main__':
    
    in_file_name = './data/friends.json'
    with open(in_file_name) as f:
        friends = json.load(f)


    #待统计参数
    sex_counter = Counter()  #性别
    Province_conter = Counter()  #省份
    NickName_list = []  #昵称
    Signature_counter = Counter()  #个性签名关键词

    for friend in friends:
        #统计性别
        sex_counter[friend['sex']] += 1
        #省份
        if friend ['Province'] != "":
            Province_conter[friend['Province']] += 1
        #昵称
        NickName_list.append(friend['NickName'])
        #个性签名关键词提取提取
        get_tag(friend['Signature'], Signature_counter)


    #性别
    name_list, num_list = dict2list(sex_counter)
    get_pie('性别统计', name_list, num_list)

    #省份前15
    # name_list, num_list = counter2list(Province_conter.most_common(15))
    # get_bar('地区统计', name_list, num_list)

    #地图

    #昵称

    #微信好友签名关键词
    name_list = counter2list(Signature_counter.most_common(200))
    num_list = counter2list(Signature_counter.most_common(200)) 
    word_cloud('微信好友签名关键词', name_list, num_list,[20,100])

    #头像合成

