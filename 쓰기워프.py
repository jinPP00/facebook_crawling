# -*- coding: utf-8 -*-
# from socket import AI_PASSIVE
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts
from wordpress_xmlrpc.compat import xmlrpc_client

# 이미지 워프에 업로드
def attach_post(data, myAccount):
  print(data['Content_2'])
  upload_imgurl = []
  img_path = data['download_imgpath']
  myblog = Client(f'''{myAccount['site']}xmlrpc.php''', myAccount['id'], myAccount['password'])
  if img_path is not None:
    for i in range(len(img_path)):
      filepath = img_path[i]
      wo_data = {
        'name': filepath,
        'type': 'image/jpeg',  # mimetype
      }
      with open(filepath, 'rb') as img:
        wo_data['bits'] = xmlrpc_client.Binary(img.read())
      response = myblog.call(media.UploadFile(wo_data))
      upload_imgurl.append(response['url'])
      if i == 0:
        attachment_id = response['id']
      data['Content_2'] = data['Content_2'].replace("######", f'''<div align="center"><figure><img src="{upload_imgurl[i]}" alt="{data['keyword']}"></figure></div>''', 1)
    print("워프이미지업로드 성공", upload_imgurl)
  else:
    print("이미지 없습니다.")
    pass
  print(data['Content_2'])
  return upload_imgurl, attachment_id

def wordpressPost(data, myAccount, pubstatus, thumb):
  keyword = data['keyword']
  content = data['Content_2']
  title = data['title_2']
  myblog = Client(f"{myAccount['site']}xmlrpc.php", myAccount['id'], myAccount['password'])
  post = WordPressPost()
  if thumb is not None:
    post.thumbnail = thumb
  else:
    pass
  post.title = title
  post.slug = keyword
  post.content = content
  post.post_status = pubstatus  
  post_id = myblog.call(posts.NewPost(post))  
  posted_link = f'''{myAccount['site']}?p={post_id}'''
  data['link'] = posted_link
  print("워프쓰기완료", data['link'])
  return data

if __name__ == '__main__':
  myAccount = {'site':"https://krablog.com/" , 'id': "medipin09",'password': "Jinhong12!@"}
  img_path = ["C:/python/images/1vx54XaPNIHT.jpg"]
  data = {'title':"테스트", 'title_2':"테스트",'keyword':"테스트 123", 'Content_2':"테스트입니다 ###### ######", "subject":"잡","subject_2":"x" ,'download_imgpath': ['C:\\python\workspace\\블로그글쓰기\\data\\test.png']}
  
  wo_img_url, attachment_id = attach_post(data, myAccount)
  print(wo_img_url, attachment_id)

  # pubstatus = "draft"
  # posted_link = wordpressPost(data, myAccount, pubstatus, attachment_id)  # attachment_id 는 썸네일지정
  # print(posted_link)



  
