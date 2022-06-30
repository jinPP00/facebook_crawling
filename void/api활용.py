import requests
import json
import urllib.request

#네이버 짧은주소
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

method = "GET"
header = {'authorization': 'KakaoAK 0acfc1d91380d01b92ef2dc6c3a0f688'}

def daumsearch(keyword):
  url = "https://dapi.kakao.com/v2/search/web"
  params = {'query' : keyword}
  response = requests.request(method=method, url=url, headers=header, params=params )
  ### response = requests.get(url, headers=header, params=params) 
  tokens = response.json()
  # print(response)
  return tokens

def daumBlog(keyword):
  url = "https://dapi.kakao.com/v2/search/blog"
  params = {'query' : keyword, 'size':50}
  # 'page'= 2
  response = requests.request(method=method, url=url, headers=header, params=params )
  ### response = requests.get(url, headers=header, params=params) 
  tokens = response.json()
  # print(response)
  return tokens

def daumimgSearch(keyword):
  url = "https://dapi.kakao.com/v2/search/image"
  params = {'query' : keyword}
  response = requests.request(method=method, url=url, headers=header, params=params )
  tokens = response.json()
  return tokens

def daumYoutube(keyword):
  url = "https://dapi.kakao.com/v2/search/vclip"
  params = {'query' : keyword}
  response = requests.request(method=method, url=url, headers=header, params=params )
  tokens = response.json()
  return tokens

if __name__ == '__main__':
  # keyword = "부산 광안리"
  # tokens = daumBlog(keyword)
  # print(tokens)
  # print(tokens)

  shortUrl('https://firebasestorage.googleapis.com/v0/b/my-project-1635737583462.appspot.com/o/images%2F%EA%B3%B5%EB%8F%99%EC%9D%B8%EC%A6%9D%EC%84%9C%20%EB%B0%9C%EA%B8%89%EB%B0%9B%EB%8A%94%20%EB%B2%95%2F%EA%B3%B5%EB%8F%99%EC%9D%B8%EC%A6%9D%EC%84%9C%20%EB%B0%9C%EA%B8%89%EB%B0%9B%EB%8A%94%20%EB%B2%9500?alt=media&token=afb3f945-10c1-4758-bd46-27a427ffdaf6')