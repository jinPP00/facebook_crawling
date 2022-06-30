
import os
from fb_control import firebase_credit, fb_db_update
import 본문크롤링, 링크만들기, 이미지삽입
import time

def createFolder(title, content):
  directory = f'.\\output'
  try:
    if not os.path.exists(directory):
      os.makedirs(directory)
  except OSError:
    print('Error: Creating directory. ' + directory)
  with open(directory+f"\\{title}.html", 'w', encoding="UTF8") as f:
    f.write(content)
  print(">>", title, "html 만들기 완료")

def myConverter(data): 
  for i in range(len(data['imgdict'])):
    data['Content_2'] = data['Content_2'].replace('@@@@@@', f'''\n<div style="text-align:center;"><figure><img src="{data['imgdict'][i]}" style="max-height:500px;max-width:650px;"></figure></div>''', 1)
  data['Content_2'] = 링크만들기.관련페북링크(data)
  data['Content_2'] = 링크만들기.관련페북큰링크(data)
  data['Content_2'] = 링크만들기.이전글링크(data)
  # data['Content_2'] = 링크만들기.yoyo(data)
  # data['Content_2'] = 링크만들기.관련링크추가(data)
  # data['Content_2'] = 링크만들기.관련버튼추가(data)
  # data['Content_2'] = 링크만들기.관련큰링크(data)
  
  data['Content_2'] = data['Content_2'].replace("ADSENSE1", '''\n<div id="ad1"></div>''').replace("ADSENSE2", '''\n<div id="ad2"></div>''').replace("ADSENSE3", '''\n<div id="ad3"></div>''')
  data['Content_2'] = f'''<div class="main-content">{data['Content_2']}</div>'''
  return data

def img_upload(data):
  # data = 이미지삽입.imageDown(data, len(data['imgdict']))
  data = 이미지삽입.imageDown(data, 0)
  data = 이미지삽입.fireb_upload(data)
  return data

def wordpress_posting(data):
  from 쓰기워프 import wordpressPost
  myAccount = {'site':"https://yoontaegoo.com/", 'id': "medipin09",'password': "Jinhong12!@"}
  data = wordpressPost(data, myAccount, "draft", "")

def facebook_main(blog_list):
  blog_link_list =  ["https://blackdoggy.xyz/archives/88153"]
  user, db, storage = firebase_credit("./libdata/auth3.json")
  # blog_link_list = 본문크롤링.wordpress_rss(blog_list, 1, 2)
  for i in range(len(blog_link_list)):
    data = {'originallink': blog_link_list[i], "subject":"페북", 'blogstyle': "wordpress"}
    data = 본문크롤링.myContent_2(db, data)
    if 'comment' in data:
      print(data['comment'])
    else:
      data = myConverter(data) 
      data = img_upload(data)
      del data['Content_1']
      del data['title_1']
      del data['imgdict']
      del data['download_imgpath']
      del data['blogstyle']
      del data['subject_2']
      fb_db_update(db, "myblog",data['title_2'], data)
      print(">> FB 업로드 완료")
      createFolder(data['title_2'], data['Content_2'])
      print(data['title_2'], " 완료")
      time.sleep(5)
  return data

if __name__ == '__main__':
  blog_list = ["https://blackdoggy.xyz/page/"]
  data = facebook_main(blog_list)
  
  
