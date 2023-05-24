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
        openai.api_key = self.api_key
            # 當我要求你設計場景時,請設計出故事發生的場景，例如，如果故事風格是魔法,你可以談論魔法學校或魔法森林；如果是科幻,你可以談論外太空或科技等等,但必須好好地描述場景
            # 如果除了主角外還有其他角色,你必須在一開始就設計出所有角色的資訊,如果是怪獸,你必須在其他角色描述怪獸外觀,名稱,性格等等。
            # 場景:
            # 其他角色描述:
            # [名稱:]
            # [外觀:]
            # [性格:]
    def generate_story_beginning(self, prompt_user):
        x = {"role":"user","content":f"""{prompt_user}兒童故事
            我想讓你扮演講故事的角色。您將想出引人入勝、富有想像力和吸引觀眾的有趣故事。
            它可以是童話故事、教育故事或任何其他類型的故事，有可能吸引人們的注意力和想像力。
            """,
            "role":"user","content":f"""
            我的第一個要求是“我需要一個關於兒童故事的{prompt_user}故事“。
            請設計出主角名稱、外觀、性格、場景、故事名稱、故事開頭、3個故事選項
            特別要求主角外觀部分請給我頭髮特徵,故事開頭字數必須在60個字以上80個字以下,選項的字數必須在20個字以上45個字以下
            請依照下列格式做出回應,請用繁體中文回答,標點符號請用半形
            主角描述:
            [名稱:]
            [外觀:]
            [性格:]
            故事名稱:   
            故事開頭:
            選項:
            1.
            2.
            3.
            """}
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=1000,
            messages=[x]
        )
        ai_msg = response.choices[0].message.content.replace('\n', '')
        self.messages.append(x)
        self.messages.append({"role": "assistant", "content": ai_msg})

        return ai_msg

    def generate_story_item(self, option, option_count):

        x = {"role":"user","content":""""我會做選擇
                                    請繼續設計接下來故事內容和3個選項,
                                    故事開頭字數必須在60個字以上80以下,選項字數必須在20個字以上45字以下
                                    依照下列格式回應             
                                    故事內容:            
                                    選項:
                                    1.
                                    2.
                                    3.           
                        """}
        if x not in self.messages:
            self.messages.append(x)
            self.messages.append({"role": "user", "content": option})
            

        if option_count == 3:
            x = {"role":"user","content":""""請妳在這次回答給故事一個完美的結束內容,
                                            故事內容控制在50個字以上80個字以內
                                            依照下列格式回應                 
                                            故事內容:
                                                    
                                            <故事結束!>
                                            
                        """}
            self.messages.append(x)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=1000,
            messages=self.messages
        )
        ai_msg = response.choices[0].message.content.replace('\n', '')
        self.messages.append({"role": "assistant", "content": ai_msg})
        option_count += 1

        return ai_msg, option_count

    def translate(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0.5,
            messages=[
                {"role": "user", "content": f"請幫我翻譯\"{prompt}\"從中文翻譯成英文,並且自動找出最適合放進stable diffusion的生圖咒語"}
            ]
        )
        ai_msg = response.choices[0].message.content.replace('\n', '')
        return ai_msg

# def generatestorybeginning(prompt_user): 
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     config = configparser.ConfigParser()
#     config.read(os.path.join(BASE_DIR ,'config.ini'))
#     openai.api_key = config.get('chat_gpt_story', 'api_key')
#     global messages
#     messages = []
#     x = {"role":"user","content":f"""{prompt_user}兒童故事
#             我想讓你扮演講故事的角色。您將想出引人入勝、富有想像力和吸引觀眾的有趣故事。
#             它可以是童話故事、教育故事或任何其他類型的故事，有可能吸引人們的注意力和想像力。
#             根據目標受眾，您可以為您的講故事會議選擇特定的主題或主題，例如，如果是兒童，您可以談論動物；如果是成年人，那麼基於歷史的故事可能會更好地吸引他們等等。
#             當我要求你設計主角時,請設計出主角外觀以及性格。你設計出的故事內容,必須與角色個性呼應
#             """,
#         "role":"user","content":f"""
#             我的第一個要求是“我需要一個關於兒童故事的{prompt_user}故事“。
#             請設計出主角名稱、外觀、性格、故事名稱、故事開頭、3個故事選項
#             特別要求主角外觀部分請給我頭髮特徵,故事開頭字數必須在80至100字,選項字數必須在40至50字

#             請依照下列格式做出回應

#             主角描述:
#             [名稱:]
#             [外觀:]
#             [性格:]
#             故事名稱:
            
#             故事開頭:
            
#             選項:
#             1.
#             2.
#             3.
#             """}
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         temperature=0.8,
#         max_tokens=1000,
#         messages=[
#                  x
#                 ]
#         )
#     ai_msg = response.choices[0].message.content.replace('\n','')
#     messages.append(x)
#     messages.append({"role":"assistant","content":ai_msg})
#     return ai_msg,messages
# def generatestoryitem(option,option_count,message):
#     x = {"role":"user","content":""""我會做選擇
#                                     請繼續設計接下來故事內容和3個選項,
#                                     故事開頭字數必須在80至100字,選項字數必須在40至50字

#                                     依照下列格式回應
                                    
#                                     故事內容:
                                    
#                                     選項:
#                                     1.
#                                     2.
#                                     3.           
#                         """}
#     if x not in message: 
#         message.append(x)
#         message.append({"role":"user","content":option})
#     if option_count == 3:
#         message.append({"role":"user","content":""""我會做選擇,請妳在這次回答給故事一個完美的結束內容,
#                                                     故事內容控制在100個字以上150個字以內

#                                                     依照下列格式回應
                                                    
#                                                     故事內容:
                                                    
#                                                     <故事結束!>
                                            
#                         """})
#     for _ in range(5):  # 給你5次機會><
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             temperature=0.8,
#             max_tokens=1000,
#             #stream=True,
#             messages=message
#             )
#         ai_msg = response.choices[0].message.content.replace('\n','')
#         if "故事內容:" not in ai_msg:
#             continue
#         else:
#             message.append({"role":"assistant","content":ai_msg})
#             option_count+=1
#             return ai_msg,option_count,message
# def translate(prompt):
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     config = configparser.ConfigParser()
#     config.read(os.path.join(BASE_DIR ,'config.ini'))
#     openai.api_key = config.get('chat_gpt_story', 'api_key')
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         max_tokens=500,
#         temperature=0.5,
#         messages=[
#             {"role":"user","content":f"請幫我翻譯\"{prompt}\"從中文翻譯成英文,並且自動找出最適合放進stable diffusion的生圖咒語"}
#                              ]
#         )
#     ai_msg = response.choices[0].message.content.replace('\n','')
#     return ai_msg

# =============================================================================
# url = 'https://database01-eaae6-default-rtdb.firebaseio.com'
# fdb = firebase.FirebaseApplication(url, None)   # 初始化 Firebase Realtimr database
# chatgpt = fdb.get('/','chatgpt')
# if chatgpt == None:
#     messages = []        # 如果沒有資料，預設訊息為空串列
# else:
#     messages = chatgpt   
# =============================================================================
