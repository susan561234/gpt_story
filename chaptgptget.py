# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:03:07 2023

@author: Tibame_EX14
"""
import openai
import configparser
import os

class StoryGenerator:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        config = configparser.ConfigParser()
        config.read(os.path.join(BASE_DIR, 'config.ini'))
        self.api_key = config.get('chat_gpt_story', 'api_key')
        self.messages = []
        self.total_token = []
        openai.api_key = self.api_key
    def generate_story_beginning(self, prompt_user):
        x = {"role":"user","content":f"""{prompt_user}兒童故事我想讓你扮演講故事的角色。您將想出引人入勝、富有想像力和吸引觀眾的有趣故事。它可以是童話故事、教育故事或任何其他類型的故事，有可能吸引人們的注意力和想像力。""",
            "role":"user","content":f"""我的第一個要求是“我需要一個關於兒童故事的{prompt_user}故事“。請設計出主角名稱、外觀、性格、場景、故事名稱、故事開頭、3個故事選項特別要求主角外觀部分請給我頭髮特徵,故事開頭字數必須在60個字以上80個字以下,選項的字數必須在20個字以上45個字以下,請依照下列格式做出回應,請用繁體中文回答,標點符號請用半形,主角描述:[名稱:][外觀:][性格:],故事名稱:,故事開頭:,
            選項:
            1.
            2.
            3."""}
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=600,
            messages=[x]
        )
        ai_msg = response.choices[0].message.content.replace('\n', '')
        self.messages.append(x)
        self.messages.append({"role": "assistant", "content": ai_msg})
        self.total_token.append(response['usage']['total_tokens'])
        print("第一次請求:",self.total_token)
        print(ai_msg)
        return ai_msg

    def generate_story_item(self, option, option_count):
        if 4096-self.total_token[option_count]<800:
            self.messages.pop(0)
        x = {"role":"user","content":""""我會做選擇,請繼續設計接下來故事內容和3個選項,故事開頭字數必須在60個字以上80以下,選項字數必須在20個字以上45字以下,依照下列格式回應,
        故事內容:
        選項:
        1.
        2.
        3."""}
        if x not in self.messages:
            self.messages.append(x)
            self.messages.append({"role": "user", "content": option})
        if option_count == 3:
            x = {"role":"user","content":""""請妳在這次回答給故事一個完美的結束內容,故事內容控制在80個字以上100個字以內,依照下列格式回應,故事內容:,<故事結束!>"""}
            self.messages.append(x)
        for _ in range(3):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                temperature=0.5,
                max_tokens=800,
                messages=self.messages
            )
            ai_msg = response.choices[0].message.content.replace('\n', '')
            if "故事內容" not in ai_msg:
                continue
            else:
                break
        ai_msg = response.choices[0].message.content.replace('\n', '')
        self.messages.append({"role": "assistant", "content": ai_msg})
        self.total_token.append(response['usage']['total_tokens'])
        option_count += 1
        print(f"第{option_count}次請求:",self.total_token)

        print(ai_msg)
        
        
        return ai_msg, option_count

