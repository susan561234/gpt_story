# import mysql.connector
# import configparser
# import os
# import datetime

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# config = configparser.ConfigParser()
# config.read(os.path.join(BASE_DIR ,'config.ini'))
# conn = mysql.connector.connect(
#     host=config.get('mysql', 'host'),  # 連線主機名稱  
#     user=config.get('mysql', 'user'),  # 登入帳號
#     password=config.get('mysql', 'passwd'),
#     database=config.get('mysql', 'database'),
#     port=3306)  
# cursor = conn.cursor()
# storyName="name"
# query = 'INSERT INTO linebot.upload_fig (time, file_path) VALUES (%s, %s)'
# value = (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), storyName)
# cursor.execute(query, value)
# conn.commit()
# conn.close()
import pymongo
import datetime
import pandas as pd
class DB:
  def __init__(self):
    self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    self.mydb = self.myclient["test"]
  def DB_start(self,ip,user_id,start_time,datatime):
    # dblst = myclient.list_database_names()
    mycol = self.mydb["start"]
    data = {"ip": ip,"user_id":user_id,"start_time":start_time,"datatime":datatime}
    inserted_document = mycol.insert_one(data)
  def DB_over(self,ip,start_time,over_time,datatime,style,storyname,completestory,imgurl):
    mycol = self.mydb["story"]
    data = {"ip": ip,"start_time":start_time,"over_time":over_time,"datatime":datatime,"storytype":style ,"stotyname":storyname,"completestory":completestory,"photo":imgurl}
    inserted_document = mycol.insert_one(data)
  def DB_find_style(self,data_time):#list    
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    count1_list = []
    count2_list = []
    count3_list = []
    count4_list = []
    # dblst = myclient.list_database_names()
    mycol = self.mydb["story"]
    for data_time_one in data_time :
      query = {"datatime":data_time_one}
      results = mycol.find(query)
      for result in results:
        d  = result['storytype']      
        if d=="科幻":
          count1 += 1
        elif d=="魔法":
          count2 += 1
        else:
          count3 += 1
        count4 += 1
        
      count1_list.append(count1)
      count2_list.append(count2)
      count3_list.append(count3)
      count4_list.append(count4)
      count1 = 0
      count2 = 0
      count3 = 0
      count4 = 0
    return count1_list,count2_list,count3_list,count4_list
  def DB_find_people(self,data_time):#list
    count_people_start = 0
    count_people_start_list = []
    mycol = self.mydb["start"]
    results = mycol.find()
    for data_time_one in data_time :
      query = {"datatime":data_time_one}
      results = mycol.find(query)
      for result in results:
        count_people_start += 1
      count_people_start_list.append(count_people_start)
      count_people_start = 0
    return count_people_start_list
      

      

      
# if __name__ == "__main__":
#   print(DB_find_style(pd.date_range(start='2023-05-18', periods=30))))