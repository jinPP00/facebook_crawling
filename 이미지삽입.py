import json, os
import urllib.request as req
import urllib.request 
from string import ascii_uppercase, ascii_lowercase, digits
from PIL import Image
import random
from fb_control import fb_storage_update

outpath = "C:/python/images/facebook/"
if not os.path.exists(outpath):
  os.mkdir(outpath)

def shortUrl(url):
  client_id = "l9XuLKg5kJrQljLZRYVv" # 네이버 개발자센터에서 발급받은 CLIENT ID
  client_secret = "34cboxYhES" # 네이버 개발자센터에서 발급받은 CLIENT SECRET
  encText = urllib.parse.quote(url) # 단축 시킬 URL 주소
  data = "url=" + encText
  url = "https://openapi.naver.com/v1/util/shorturl"
  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id",client_id)
  request.add_header("X-Naver-Client-Secret",client_secret)
  response = urllib.request.urlopen(request, data=data.encode("utf-8"))
  rescode = response.getcode()
  if(rescode==200):
      response_body = response.read()
      response = response_body.decode('utf-8')
      responseJson = json.loads(response)
      naverShorturl = responseJson.get("result").get("url")
      # print("단축URL: ", naverShorturl)
  else: print("Error Code:" + rescode)
  print(naverShorturl)
  return naverShorturl

def rand_generator(length=12):
  chars = ascii_uppercase + ascii_lowercase + digits
  return ''.join(random.sample(chars, length))

def imageDown(data, imgCount):
  img_path = data['imgdict']
  download_imgpath = []
  if img_path is not None:
    for i in range(len(img_path)):
      downImgPath = outpath + rand_generator() +".jpg"
      req.urlretrieve(img_path[i], downImgPath)
      download_imgpath.append(downImgPath)
      print(">> 이미지 다운로드 완료", download_imgpath[i])
      data['Content_2'] = data['Content_2'].replace(data['imgdict'][i],download_imgpath[i],1)
      if i == imgCount:
        break
  else:
    print("다운로드할 이미지 없음")
    pass
  data['download_imgpath'] = download_imgpath
  image_process(data)
  print(">> img 리사이즈 완료")
  return data

def fireb_upload(data):
  upload_imgurl = []
  foldname = data['title_2']
  img_path = data['download_imgpath']
  if img_path is not None:
    for i in range(len(img_path)):
      filename = data['title_2']+"0"+str(i)
      upload_imgurl.append(fb_storage_update(foldname,filename,img_path[i]))
      short_url = shortUrl(upload_imgurl[i])
      data['Content_2'] = data['Content_2'].replace(data['download_imgpath'][i], short_url, 1)
      print(">> 이미지 fb업로드 완료")
    data['Content_2'] = f'''<img src="{short_url}" style="display:none;"/>''' + data['Content_2']
  else:
    print("업로드할 이미지 없음")
    upload_imgurl.append(" ")
    pass
  data['imgurl'] = short_url
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