import 본문크롤링, 전부바꾸기, 이미지삽입
import random
from datetime import datetime
import os
from db저장 import fb_db_update

def worp_blog_list():
  blog_list = ["https://blackdoggy.xyz/page/"]
  blog_link_list = 본문크롤링.wordpress_rss(blog_list, 1, 2)
  return blog_link_list

def createFolder(title, content):
  directory = f'.\\output'
  nowtime_record = datetime.today().strftime("%Y-%m-%d")
  try:
    if not os.path.exists(directory):
      os.makedirs(directory)
  except OSError:
    print('Error: Creating directory. ' + directory)
  with open(directory+f"\\{title}_{nowtime_record}.html", 'w', encoding="UTF8") as f:
    f.write(content)
  print(">>", title, "html 만들기 완료")

def img_upload(data):
    print("[system] STEP 4 : 이미지 업로드")
    data = 이미지삽입.imageDown(data, 0)
    data = 이미지삽입.fireb_upload(data)
    return data

def wordpress_posting(data):
  from 쓰기워프 import wordpressPost
  myAccount = {'site':"https://yoontaegoo.com/", 'id': "medipin09",'password': "Jinhong12!@"}
  data = wordpressPost(data, myAccount, "draft", "")

def fb_upload(data):
  mydata = {"subject" : data['subject'], "subject_2" : data['subject_2'], "title_2": data['title_2'], "originallink": data['originallink'], "keyword": data['keyword'], "Content_2": data['Content_2'], "imgurl":data['imgurl'], "status":data['status']}
  fb_db_update("myblog",data['keyword'], img_upload(data))

def facebook_main():
  blog_link_list =  ["https://blackdoggy.xyz/archives/88153"]
  data = {'originallink': blog_link_list[0], "subject":"페북", 'blogstyle': "wordpress"}
  data = 본문크롤링.myContent_2(data)
  data = 전부바꾸기.myConverter(data)
  # print(data)
  createFolder(data['title_1'], data['Content_2'])
  return data

if __name__ == '__main__':
  # blog_link_list = worp_blog_list()
  # print(blog_link_list)

  data = facebook_main()
  # print(data)


# blog_link_list = 본문크롤링.tistory_rss(blog_list, 3)
# data = {'originallink': blog_link_list[0], "subject":"페북", 'blogstyle': "tistory"}


