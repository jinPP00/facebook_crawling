# -*- coding: utf-8 -*-
from string import ascii_uppercase, ascii_lowercase, digits
import base64
import os, random, json, requests
import urllib.parse as par
import urllib.request as req
from urllib.request import urlopen
from api활용 import daumimgSearch
from bs4 import BeautifulSoup
from db저장 import fb_storage_update
from PIL import Image
from api활용 import shortUrl

outpath = "C:/python/images/jinweb/"
if not os.path.exists(outpath):
  os.mkdir(outpath)

def rand_generator(length=12):
  chars = ascii_uppercase + ascii_lowercase + digits
  return ''.join(random.sample(chars, length))

def Yimage(data):
    encoded = par.quote(data['keyword'])
    url = "https://images.search.yahoo.com/search/images;_ylt=Awr9CKtWOPFgQDcAFABXNyoA;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZANDMjAxMl8xBHNlYwNwaXZz?p={}&fr2=piv-web&fr=yfp-t".format(encoded)
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    img = soup.select("li > a > img")
    data['yimage'] = []
    cnt = 0
    for i in img:
        img_url = i.attrs['data-src']
        data['yimage'].append(img_url)
        cnt +=1
        if cnt == 10:
            break
    print(data['yimage'],"yimage 이미지 크롤링 완료")
    return data

def DImage(data):
  # imgtokens = daumimgSearch(data['keyword'])
  imgtokens = daumimgSearch(data['keyword'])
  dimage_list = []
  for i in range(len(imgtokens['documents'])):
    # if "postfiles" in imgtokens['documents'][i]['image_url'] or "news" in imgtokens['documents'][i]['collection'] or "news" in imgtokens['documents'][i]['image_url'] or "https://blogfiles.pstatic.net" in imgtokens['documents'][i]['image_url'] or "cafeattach" in imgtokens['documents'][i]['image_url'] or "dispatch" in imgtokens['documents'][i]['image_url'] or "pstatic" in imgtokens['documents'][i]['image_url'] or "http://" in imgtokens['documents'][i]['image_url']:
    #   pass
    # else:
    dimage_list.append(imgtokens['documents'][i]['image_url'])
  # print(len(dimage_list),"개 dimage 크롤링완")
  return dimage_list

# @@@@@@를 원본이미지링크로 변환
def originalImage(data, thumb):
  if '@@@@@@' in data['Content_2']:
    if len(data['imgdict']) > 0:
      if thumb == "ori":
        print("오리지널 이미지")
        data['modified_img'] = data['imgdict'].copy()
      elif thumb == "f_dimg":
        print("다음이미지")
        # data['modified_img'] = []
        data['modified_img'] = data['imgdict'].copy()
        dimage_list = DImage(data)
        data['modified_img'][0] = random.choice(dimage_list)
      elif thumb == "ori+dimg":  
        # print(data['imgdict'])
        data['modified_img'] = data['imgdict'].copy() + random.sample(DImage(data), k=3)
        random.shuffle(data['modified_img'])
      elif thumb == "ori+yimg":  
        data['modified_img'] = data['imgdict'].copy() + random.sample(DImage(data), k=3)
        random.shuffle(data['modified_img'])
  elif "<img" in data['Content_2']:
    print("img가 있습니다.")
    pass
  else:
    print("이미지가 없습니다. 이미지 추가")
    data['Content_2'] = f'''@@@@@@ {data['Content_2']}''' 
    data['modified_img'] = [random.choice(DImage(data))]
  return data


# imgsrc = 'https://dimg.donga.com/ugc/CDB/SHINDONGA/Article/5f/9a/4c/f6/5f9a4cf615cfd2738de6.jpg'
# @@@@@@를 다른이미지링크로 변환
def urlconverter(img_path, data):
  # print("&&&&&&&&&&&&",data['imgdict'])
  count = data['Content_2'].count("@@@@@@")
  data['img_frame'] = []
  if img_path is not None:
    # print("img_frame이 없지 않다면")
    for i in range(count):
      data['img_frame'].append(f'''\n<div style="text-align:center;"><figure><img src="{data['modified_img'][i]}" style="max-height:500px;max-width:650px;"></figure></div>''')
      data['Content_2'] = data['Content_2'].replace('@@@@@@',data['img_frame'][i],1)
  else:
    pass
  return data

# <img src="https://t1.daumcdn.net/cafeattach/1IHuH/baa1c3b39d0695789f6a9ffc7b67c1e31a1e7641" oneerror="this.src='https://dimg.donga.com/ugc/CDB/SHINDONGA/Article/5f/9a/4c/f6/5f9a4cf615cfd2738de6.jpg'">

# 이미지 다운로드
def imageDown(data, imgCount):
  img_path = data['modified_img']
  download_imgpath = []
  if img_path is not None:
    for i in range(len(img_path)):
      downImgPath = outpath + rand_generator() +".jpg"
      req.urlretrieve(img_path[i], downImgPath)
      download_imgpath.append(downImgPath)
      print(">> 이미지 다운로드 완료", download_imgpath[i])
      data['Content_2'] = data['Content_2'].replace(data['img_frame'][i],'######',1)
      if i == imgCount:
        break
  else:
    print("다운로드할 이미지 없음")
    pass
  data['download_imgpath'] = download_imgpath
  image_process(data)
  print(">> img 리사이즈 완료")
  return data

# imgbb 이미지 업로드 (style = 0이면 썸네일형태 아니면 원래크기)
def imagebbUpload(data, thumb):
  upload_imgurl = []
  img_path = data['download_imgpath']
  if img_path is not None:
    for i in range(len(img_path)):
      with open(img_path[i], "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
          "key": "5b457e5d5ac77547f0ad030a52c06867",
          "image": base64.b64encode(file.read()),
      }
        res = requests.post(url, data=payload)
        if res.ok:
          json_res = res.text 
          json_res2 = json.loads(json_res)
          TypeofVar = type(json_res2)
          if "dict" in str(TypeofVar): # check the type of var
              data_res = json_res2.get('data') 
              if i == 0 and thumb == "thumb":  
                thumb_res = data_res.get('thumb')
                uploadUrl = thumb_res.get('url')
              else:
                uploadUrl = data_res.get('url')
              upload_imgurl.append(uploadUrl)
          else:
              print("ERROR the var is not dict but {}".format(TypeofVar))
        else:
            print("ERROR {}".format(res.status_code))
      data['Content_2'] = data['Content_2'].replace("######", f'''<div style="text-align:center;"><figure><img src="{upload_imgurl[i]}" style="max-height:500px;max-width:650px;" alt="{data['keyword']}"></figure></div>''', 1)
    print(">> imgbb업로드 성공", upload_imgurl)
    data['Content_2'] = f'''\n<figure><img src="{upload_imgurl[0]}" style="display:none;"/>''' + data['Content_2']
  else:
    print("업로드할 이미지 없음")
    upload_imgurl.append(" ")
    pass
  data['imgurl'] = upload_imgurl
  return data

def fireb_upload(data):
  upload_imgurl = []
  foldname = data['keyword']
  img_path = data['download_imgpath']
  if img_path is not None:
    for i in range(len(img_path)):
      filename = data['keyword']+"0"+str(i)
      upload_imgurl.append(fb_storage_update(foldname,filename,img_path[i]))
      short_url = shortUrl(upload_imgurl[i])
      data['Content_2'] = data['Content_2'].replace("######", f'''\n<div style="text-align:center;"><figure><img src="{short_url}" style="max-height:500px;max-width:650px;" alt="{data['keyword']}"></figure></div>''', 1)
      print(">> 이미지 fb업로드 완료")
      

    data['Content_2'] = f'''<img src="{short_url}" style="display:none;"/>''' + data['Content_2']
  else:
    print("업로드할 이미지 없음")
    upload_imgurl.append(" ")
    pass
  data['imgurl'] = upload_imgurl
  return data

def image_process(data):
  img_path = data['download_imgpath']
  print(img_path)
  for i in range(len(img_path)):
    img = Image.open(img_path[i])
    if img.mode != 'RGB':
      img = img.convert('RGB')
    # if i == 0:
    #   # img = img.resize((300,300))
    #   img.thumbnail((350,350))
    #   print(img_path[i],"썸네일 변경완료")
    img.save(img_path[i], 'JPEG', qualty=95)
    img.close()

if __name__ == '__main__':
  data = {'Content_2': "@@@@@@ @@@@@@", 'keyword':"tiger","imgdict":["https://k.kakaocdn.net/dn/qklp8/btrmyjKt7Ol/OpZ6mn0SqGdr1Gw5EpMakk/img.jpg","https://dojang.io/pluginfile.php/13592/mod_page/content/4/016001.png"], 'subject':"잡",  "modified_img":["https://k.kakaocdn.net/dn/qklp8/btrmyjKt7Ol/OpZ6mn0SqGdr1Gw5EpMakk/img.jpg","https://dojang.io/pluginfile.php/13592/mod_page/content/4/016001.png"]}

  download_imgpath = imageDown(data, imgCount="")
  # upload_imgurl = imagebbUpload(img_path=download_imgpath , thumb="")
  # image_process(data)

  # data = originalImage(data, thumb="ori+dimg")
  # upload_imgurl = fireb_upload(data)
