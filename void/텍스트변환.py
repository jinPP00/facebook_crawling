# -*- coding: utf-8 -*-
import re, random
from api활용 import daumBlog
import urllib.parse as par
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import requests, json
from datetime import datetime
from bs4 import BeautifulSoup

def cleanText(readData):
  # hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')  # 한글만, 숫자까지 제거됨
  hangul = re.compile('[-=+,#/\?:^.@*\"※~ㆍ!』‘<>|\(\)\[\]`\'…》\”\“\’·]')
  result = hangul.sub(' ', readData)
  return result

# 실시간 검색어 추출
def nate_sil_keyword():
    now = datetime.now().strftime('%Y%m%d%H%M')
    r = requests.get('https://www.nate.com/js/data/jsonLiveKeywordDataV1.js?v=' + now).content
    keyword_list = json.loads(r.decode('euc-kr'))
    result = []
    for k in keyword_list:
        result.append(k[1])
    return result
 
def zum_sil_keyword():
    r = requests.get("https://issue.zum.com/")
    soup = BeautifulSoup(r.text, 'lxml')
    ul = soup.find("ul", {"id":"issueKeywordList"})
    num = ul.findAll("span", {"class":"num"})
    keyword_list = ul.findAll("span", {"class":"word"})
    result = []
    for k in keyword_list:
        result.append(k.text)
    return result

def silkeyword_sum():
    result1 = nate_sil_keyword()
    result2 = zum_sil_keyword()
    keyword_list = list(set(result1+result2)) 
    return keyword_list

# 구글 연관검색어 추출
def myrelKeyword(keyword):
  encoded = par.quote(keyword)
  url = "https://suggestqueries.google.com/complete/search?output=toolbar&q={}".format(encoded)
  response = urlopen(url).read()
  # print(response)
  xtree = ET.fromstring(response)
  relKeyword = []
  for i in range(len(xtree)):
    word = xtree[i][0].attrib['data']
    relKeyword.append(word)
  return relKeyword

def relkeywordAdd(keyword, content):
  text1 = ["오늘은", "금일은", "이번시간에는", "금일에는", "요번시간에는"]
  text3 = ["관련 내용을 알려드릴려고 합니다.", "관련 정보를 알려드릴려고 합니다.", "관련된 내용을 알려드릴까 해요.", "대한 내용을 포스팅하려고 해요.", "관한 정보를 포스팅하려고 해요.", "관련된 정보들을 알려드릴까 합니다.", "관련된 정보들을 설명 드리려고 해요.", "관한 내용들을 안내 드리려고 해요.", "관한 정보들을 쏙쏙 안내 드리려고 합니다."]
  TEXT1 = random.choice(text1)
  TEXT2 = ""
  TEXT3 = random.choice(text3)
  relKeyword = myrelKeyword(keyword)
  if not relKeyword or len(relKeyword)==1:
    TEXT2 = f'''{keyword}'''
  elif len(relKeyword)== 2:
    for i in range(len(relKeyword)):
      TEXT2 +=  f'''{relKeyword[i]}, '''
    TEXT2 = TEXT2[:-2]
  else:
    print("연관키워드",relKeyword)
    a = random.sample(range(1, len(relKeyword)), 2)
    for i in range(len(a)):
      TEXT2 +=  f'''{relKeyword[a[i]]}, '''
    TEXT2 = TEXT2[:-2]
  content = f'''<div><p>{TEXT1} {TEXT2} {TEXT3} </p></div>{content}'''
  return content

def TitleRR(title):
  title = cleanText(title)
  try:
    keyword = f'''{title.split(' ')[0]} {title.split(' ')[1]} {title.split(' ')[2]}'''
  except:
    keyword = f'''{title.split(' ')[0]} {title.split(' ')[1]}'''
  tokens = daumBlog(keyword)
  RanNum = random.randrange(0, len(tokens['documents']))
  # search_title = tokens['documents'][RanNum]['title'].replace("<b>","").replace("</b>","")
  search_title = cleanText(tokens['documents'][RanNum]['title']).replace("b","").replace("&gt;","").replace("&lt;","")
  word_list = title.split()
  word2_list = search_title.split()
  word2_list[0],word2_list[1] = word_list[0],word_list[1]
  word2_list[-1],word2_list[-2] = word_list[-1],word_list[-2]
  replace_title = ' '.join(word2_list)
  print(replace_title)
  return replace_title

def ContentRR(text):
    Text = text.replace("보입니다","보이는데요").replace("될까요?","되는지 알아볼까요?").replace("같습니다","같아요").replace("하겠습니다","할게요").replace("예상이에요","예상됩니다").replace("예정인데요","예정입니다").replace("최근","요즘").replace("뉴스","기사").replace("생기면서","나오면서").replace("많습니다","많은데요").replace("간단하게","간단히").replace("대하여","관하여").replace("정확히","확실히").replace("액수","금액").replace("생각합니다","생각이 듭니다").replace("가져보도록","가지도록").replace("내가","저가").replace("의견입니다","의견인데요").replace("보아야 합니다","보셔야 해요").replace("있습니다","있어요").replace("있었는데요","있었습니다").replace("해보았는데요","해보았습니다").replace("계속해서","지속해서").replace("좀 더","조금 더").replace("확대되면","커지게 되면").replace("한정","국한").replace("좋겠습니다","좋겠는데요").replace("됩니다","되는데요").replace("안녕하세요.","반갑습니다").replace("좋겠습니다.","좋겠네요").replace("졌는데요.","졌습니다.").replace("읽어보세요","읽어보시기 바랍니다").replace("이랍니다","입니다").replace("인데요","입니다").replace("주세요","주면 됩니다").replace("나와있습니다","나와있어요").replace("있을 것입니다","있습니다").replace("알려드릴게요.", "알려드리려고 해요.").replace("집니다","지는데요").replace("하는데요","합니다").replace("좋아요","좋습니다").replace("했습니다","했는데요").replace("안녕하세요","반갑습니다").replace("읽어보세요","읽어보시기 바랍니다").replace("높습니다","높은데요").replace("보세요","보시기 바랍니다").replace("우선","먼저").replace("되죠","됩니다").replace("알아봤는데요","알아봤습니다").replace("알려드릴게요","알려드리려고 해요").replace("겁니다","거에요").replace("있네요","있데는요").replace("되죠","되는데요").replace("되는데요","됩니다").replace("오늘은","이번시간에는").replace("바랍니다","바래요").replace("드립니다","드려요").replace("진행합니다","진행됩니다").replace("간편하게","간단히").replace("좋네요.","좋은데요.").replace("바라요","바랍니다").replace("함.","합니다.").replace("입니다.","인데요.").replace("하는 자","하는 분").replace("않음","않습니다").replace("모음","모아보기").replace("텐데요","수 있는데요").replace("다양한데","많은데").replace("또는","혹은").replace("인데요","입니다").replace("화양연화","제이팍").replace("되었습니다","됐습니다").replace("거주하시는","살고계시는").replace(" 곳","장소").replace("하세요","하시기 바랍니다").replace("내용","정보").replace("혹시","혹여나").replace("궁금한 점","의문점").replace("있으시면","있다면").replace("전달해드린","전해드린").replace("오늘","금일").replace("사용","이용").replace("즉시","바로").replace("관한","관련된").replace("!",".").replace("알려드리려고","전해드리려고").replace("대해서","관련해서").replace("알려드렸는데요.","알려드렸습니다.").replace("어플","앱").replace("이다.","입니다.").replace("많다","많습니다").replace("진다.","집니다.").replace("한다.","합니다.").replace("있다.","있습니다.").replace("않는다","않습니다").replace("된다.","됩니다.").replace("듣는다.","듣습니다.").replace("확인","체크").replace("앱","어플").replace("홈페이지","사이트").replace("해요.","합니다.").replace("있어요.","있습니다.").replace("할게요.","하겠습니다.").replace("이에요.","입니다.").replace("에요.","입니다.").replace("줘요.","줍니다.").replace("되어요.","될 수있습니다.").replace("았다.","았습니다.").replace("이다.","입니다.").replace("겠다.","겠습니다.").replace("했다.","했습니다.")
    return Text 

if __name__ == '__main__':
  # data ={}
  # data['Content_2'] = "345"
  # data['keyword'] = "Leave a Comment"
  # data = relkeywordAdd(data)
  # print(data)

  title_1 = "[6시 내고향]60초를 잡아라"
  keyword = "서민갑부 361회 울산"
  replace_title = TitleRR(title_1,keyword)


# def english_division(word):
#   reg = re.compile(r'[a-zA-Z]')
#   if reg.match(word):
#     print(word)
#     pass
#   else:
#       return word




# 키워드로 다음블로그 url 추출
# def tisurl_list(keyword):
#     method = "GET"
#     header = {'authorization': 'KakaoAK 0acfc1d91380d01b92ef2dc6c3a0f688'}
#     url = "https://dapi.kakao.com/v2/search/blog"
#     params = {'query' : keyword, 'size':30}
#     # 'page'= 2
#     response = requests.request(method=method, url=url, headers=header, params=params )
#     tokens = response.json()
#     bloglist = []
#     for i in range(len(tokens['documents'])):
#         if "tistory.com" in tokens['documents'][i]['url']:
#             bloglist.append(tokens['documents'][i]['url'])
#         else:
#             pass
#     print(bloglist)
#     bloglink = random.choice(bloglist)
#     return bloglink

# if __name__ == "__main__":
#     keyword_list = silkeyword_sum()
#     print(keyword_list)
#     mykeyword = random.choice(keyword_list)
#     bloglink = tisurl_list(mykeyword)