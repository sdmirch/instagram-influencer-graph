# coding=utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json
import requests
from pymongo import MongoClient
import numpy as np
from collections import defaultdict
import pickle
import networkx as nx

from webscrape_util.scrape_util import (load_json,
                                        write_json,
                                        selenium_instagram_login,
                                        setup_mongo_client)


client, collection = setup_mongo_client('instascrape', 'influencer_likes')


# Making dictionary of top posts for top influencers


hashtags_likes_dict = load_json('../data/hashtags_likes_dict.json')
top = nx.read_gml('/home/emil/Desktop/instagram-influencer-graph/graph_util/file.gml')

# словарь всех influencer ов
influencers_top = {}
for k, v in hashtags_likes_dict.iteritems():
    if k in top.nodes():
        influencers_top[k] = v
    print influencers_top

# Словарь из списка самых пролайканных постов и количества лайков
influencers_top_post = {}
for k, v in influencers_top.iteritems():
    influencers_top_post[k] = {'max_likes': 0, 'post': None}
    for i in range(len(v['likes'])):
        if v['likes'][i] > influencers_top_post[k]['max_likes']:
            influencers_top_post[k]['max_likes'] = v['likes'][i]
            influencers_top_post[k]['post'] = v['posts'][i] # ищет самый пролайканный пост
        print influencers_top_post

# Список постов с наибольшим количество лайков
top = influencers_top_post.keys()


driver = webdriver.Firefox()
# Likes on posts. Who liked this posts(edges)
url_likes = "https://www.instagram.com/graphql/query/?query_id=17864450716183058&variables=%7B%22shortcode%22%3A%22{}%22%2C%22first%22%3A{}%7D"
selenium_instagram_login(driver, '../instagram_credentials.json')


for i in range(len(top)):
    driver.get(url_likes.format(influencers_top_post[top[i]]['post'], str(influencers_top_post[top[i]]['max_likes'])))
    time.sleep(np.random.uniform(3, 5))

    driver.find_element_by_id('rawdata-tab').click()
    data = driver.find_element_by_css_selector('pre.data')
    my_json = json.loads(data.text)
    likes = my_json['data']['shortcode_media']['edge_liked_by']['edges']
    # мы вставляем в базу данных самый пролайканный пост и человека, который это лайкнул
    collection.insert_one({'id': top[i], 'likes': likes})
    # Post id
    print top[i]

    time.sleep(np.random.uniform(5, 8))



cursor = collection.find({})
for x in cursor:
    user_id = x['id']
    # Они переопределили likes и теперь это будет просто список id пользователей
    likes = []
    for liker in x['likes']:
        likes.append(liker['node']['id'])
    if influencers_top_post.get(user_id, False):
        # Добавляет список пользователей, пролайкавших пост
        influencers_top_post[user_id]['likes'] = likes

## Add total followers

G = nx.read_gml('/home/emil/Desktop/instagram-influencer-graph/graph_util/file.gml')


for influencer in influencers_top_post:
    influencers_top_post[influencer]['num_follow'] = len(G.in_edges(influencer))


write_json(influencers_top_post, '../data/interaction_dict.json')


# Checking the data


for k, v in influencers_top_post.iteritems():
    if 'likes' in v.keys():
        print k, v['max_likes'], len(v['likes'])



