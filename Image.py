# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 17:30:20 2023

@author: Tibame_EX14
"""


import BingImageCreator
import configparser
import os
import requests
import concurrent.futures
from typing import List

def Image(prompt):
    import openai
    config = configparser.ConfigParser()
    config.read('config.ini')
    openai.api_key = config.get('chat_gpt_story', 'api_key') 
    response = openai.Image.create(
        prompt=prompt,
        model="image-alpha-001",
        size="512x512",
        response_format="url"
    )   
    return response["data"][0]["url"]
def Image1(prompt):
    import chaptgptget
    config = configparser.ConfigParser()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    config.read(os.path.join(BASE_DIR ,'config.ini'))
    translated = chaptgptget.translate(prompt)   
    print(translated)
    x = BingImageCreator.ImageGen(config.get('chat_gpt_image', 'micosoft_key'))
    try:
        return x.get_images(translated + "watercolor painting")# pop art digital art watercolor painting
    except Exception as e:
        print(f"Error: {e}")
        # return a default image URL or an error message
        return "default_image_url_here"




def post_request(data: dict, url: str) -> str:
    response = requests.post(url, data=data)
    return response.text
def stable_diffusion_photo(main_character: str,storycontext: str,button1: str,button2: str,button3: str) -> list:
    url = 'http://35.226.104.60:5000/'
    data1 = {}
    data2 = {}
    data3 = {}
    data4 = {}
    data1["prompt"] = main_character+storycontext
    data2["prompt"] = main_character+storycontext+button1
    data3["prompt"] = main_character+storycontext+button2
    data4["prompt"] = main_character+storycontext+button3
    
    responses = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(post_request, data1, url)
        future2 = executor.submit(post_request, data2, url)
        future3 = executor.submit(post_request, data3, url)
        future4 = executor.submit(post_request, data4, url)

    responses = [future1.result(), future2.result(), future3.result(), future4.result()]

    return responses
