# -*- coding: utf-8 -*-
import random, re, requests
from bs4 import BeautifulSoup
import feedparser, ssl 
import fb_control

data = {}
header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def tistory_rss(blog_list, rss_count):
  if hasattr (ssl, '_create_unverified_context') :
    ssl._create_default_https_context = ssl._create_unverified_context
  blog_link_list = []
  for i in range(len(blog_list)):
    feed = feedparser.parse(blog_list[i] + "rss")
    for idx, entry in enumerate(feed.entries, start=1) :
      print(idx,"번째", entry['id'], "크롤링")
      blog_link_list.append(entry['id'])
      if idx == rss_count: 
          break
  return blog_link_list

# 워프페이지 url 주소 추출
def wordpress_rss(blog_list, first, last):
  blog_link_list = []
  for i in range(len(blog_list)):
    try:
      for j in range(first, last+1):
        page_url = blog_list[i] + str(j)
        r = requests.get(page_url, headers=header)
        bs = BeautifulSoup(r.text, "lxml")
        title_count = bs.select('h2 > a')
        for k in title_count:
          blog_link_list.append(k['href'])
    except:
      print("크롤링 실패")
  return blog_link_list

def tagdict_add(data, content_2):
  data['imgdict'] = re.findall("<img[^>]*data-src=[\"']?([^>\"']+)[\"']?[^>]*>",content_2)
  content_2 = re.sub("<img[^>]*data-src=[\"']?([^>\"']+)[\"']?[^>]*>",'@@@@@@', content_2, 0, re.I|re.S)
  if not data['imgdict']:
    data['imgdict'] = re.findall("<img[^>]*src=[\"']?([^>\"']+)[\"']?[^>]*>",content_2)
    content_2 = re.sub("<img[^>]*src=[\"']?([^>\"']+)[\"']?[^>]*>",'@@@@@@', content_2, 0, re.I|re.S)
  return data, content_2

def insert_mylink(content_2):
  if len(content_2) > 7:
    randNum = random.sample(range(1,len(content_2)),8)
    # adRandomstyle  = random.randrange(1, 4)
    # content_2.insert(randNum[0], f'$$$$$$')
    # content_2.insert(randNum[1], f'$$$$$$')
    # content_2.insert(randNum[2], f'$$$$$$')
    # content_2.insert(randNum[4], f'PRN')
    content_2.insert(randNum[5], f'ADSENSE1')
    content_2.insert(randNum[6], f'ADSENSE2')
    content_2.insert(randNum[7], f'ADSENSE3')
    content_2.insert(randNum[1], f'ADSENSE2')
    content_2.insert(randNum[2], f'ADSENSE3')
    content_2.insert(randNum[3], f'ADSENSE1')
  else:
    randNum = random.sample(range(1,len(content_2)),3)
    # content_2.insert(randNum[0], f'******')
    # content_2.insert(randNum[1], f'BTN')
    # content_2.insert(randNum[2], f'BTN')
    content_2.insert(randNum[1], f'ADSENSE1')
    content_2.insert(randNum[2], f'ADSENSE2')
  content_2.insert(0,'ADSENSE1')
  # content_2.insert(len(content_2), f'&&&&&&')
  # content_2.insert(len(content_2), f'&&&&&&')
  return content_2

def myContent_1(data):
  if "https://" not in data['originallink']:
    data['originallink'] = data['originallink'].replace("http://","https://")
  if data['blogstyle'] == "tistory" or 'blogstyle' not in data:
    if "tistory.com/m/" in data['originallink']:
      data['originallink'] = data['originallink'].replace("tistory.com/m/","tistory.com/")
    cr_link = data['originallink'].replace("tistory.com/","tistory.com/m/")
    r = requests.get(cr_link, headers=header)
    bs = BeautifulSoup(r.text, "lxml")
    try: 
      data['title_1']= bs.find("h3").text
      print("타이틀 : ", data['title_1'])
    except:  
      data['title_1'] = bs.select_one(".tit_blogview").text
      print("타이틀 : ", data['title_1'])
      pass
    # try:
    #   data['ContDate'] = bs.select_one('span.txt_date').text.strip()
    # except:
    #   data['ContDate'] = ""
    #   pass
    conT = bs.select('div.main-content')
    Content_1 = str(conT[0])
    Content_1 = re.sub('<script.*?>.*?</script>', '', Content_1, 0, re.I|re.S) 
    Content_1 = re.sub('<ins class="adsbygoogle.*?>.*?</ins>', '', Content_1, 0, re.I|re.S)
    Content_1 = re.sub('<div class="og-text.*?>.*?</div>', '', Content_1, 0, re.I|re.S)
    Content_1 = re.sub('<div class="txc-textbox ; font-color: #ffffff.*?.*?</div>', '', Content_1, 0, re.I|re.S)
    Content_1 = Content_1.split('블로그 정보')[0].split('함께보면 좋은 글')[0].split('같이보면 좋은글')[0].split('같이 보면 좋은 글')[0].split('많이 본 글보기')[0].split('저작자표시')[0].split('태그목록')[0].split('같이보면 좋은 정보')[0].split('카테고리 인기글')[0]
    Content_1 = Content_1.replace('목차','').replace('반응형','').replace('&gt;','').replace("<span>","").replace("</span>","").replace("⭐","").replace("✅","").replace("^","").replace("<b>","").replace("</b>","").replace(":)","").replace("\xa0"," ").replace("😉","").replace("더보기","").replace("§","").replace("ㅡ..ㅡ","").replace("📌","").replace("↓","🔻").replace("</strong>","").replace("<strong>","").replace("320x100","").replace("</u>",'').replace("<u>",'').replace("▶",'').replace("300x250","").replace("<em>","").replace("</em>","").replace('세로형 무한','')
    try:
      match = re.search(r'\d{4}.\s\d{1,2}.\s\d{1,2}.\s\d{1,2}:\d{1,2}', str(Content_1))
      Content_1 = Content_1.split(match.group())[1]
    except:
      pass
    try:
      match = re.search(r'\d{4}/\d{1,2}/\d{1,2}\s-\s\[', str(Content_1))
      Content_1 = Content_1.split(match.group())[0]
    except:
      pass
  elif data['blogstyle'] == "wordpress":
    print("워드프레스 크롤링.")
    cr_link = data['originallink']
    r = requests.get(cr_link, headers=header)
    bs = BeautifulSoup(r.text, "lxml")
    try: 
      data['title_1'] = bs.select_one(".entry-title").text.strip()
    except:  
      data['title_1']= bs.find("h1").text.strip()
      pass
    # try: 
    #   data['ContDate'] = bs.select_one("span.published").text.strip()
    #   data['ContDate'] = data['ContDate'].replace("년",". ").replace("월",". ").replace("일","")
    # except:
    #   data['ContDate'] = ""
    conT = bs.select('div.entry-content')
    if not conT:
      conT = bs.select('div.entry')
    if not conT:
      conT = bs.select('.read_body')
      # conT = bs.select('main.content article')
      # conT = bs.select('div.td-ss-main-content')
    content_1 = str(conT[0])
    Content_1 = re.sub('<script.*?>.*?</script>', '', content_1, 0, re.I|re.S)
    Content_1 = re.sub('<.*?id="toc_container".*?">.*?</div>', '', Content_1, 0)  
    Content_1 = re.sub('<div class="code-block.*?>.*?</div>', '', Content_1, 0, re.I|re.S)
    Content_1 = re.sub('<div class="lwptoc_i">.*?</div>', '', Content_1, 0, re.I|re.S)  
    Content_1 = Content_1.split('참고하면 좋은 글')[0]
    Content_1 = re.sub('https://[^>]*.tistory.com/[a-zA-Z0-9_]*', '******', Content_1, 0, re.I|re.S)  # 티스링크 내링크로
    Content_1 = re.sub('http://pf.kakao.com/[a-zA-Z0-9_]{1,16}', '******', Content_1, 0)  # 카카오채널을 내링크로

  data['Content_1'] = Content_1
  print("[1단계] Content_1 크롤링 완료")
  return data

def myContent_2(db, data):
  fb_data = fb_control.fb_complex_db_load(db, "myblog", "originallink", data['originallink'])
  if fb_data.val() and 'reset' not in data:
    print(">>> fb 중복")
    data['comment'] = "fb 중복"
  else:
    print(">>> FB, mongo 중복없음. 크롤링 시도")
    try:
      data = myContent_1(data)
      content_2 = data['Content_1']
      data, content_2 = tagdict_add(data, content_2)
      content_2 = re.split('<[^<>]*>',content_2)
      content_2 = list(map(lambda x: x.strip(), content_2))
      content_2 = list(filter(lambda x: x != '', content_2))
      mycontent_2 = []
      for i in range(len(content_2)):
        if not content_2[i] == "H2" and not content_2[i] == "@@@@@@":
          mycontent_2.append(f'''<p data-ke-size='size18'> {content_2[i]} </p>''')
        else:
          mycontent_2.append(f'''{content_2[i]}''')
      content_2 = insert_mylink(mycontent_2)
      data['Content_2'] = " ".join(content_2)
      data['title_2'] = data['title_1']
      data['status'] = "작업중"
      data['keyword'] = f'''{data['title_1'].split(' ')[0]} {data['title_1'].split(' ')[1]} {data['title_1'].split(' ')[2]}'''
      data['subject_2'] = "x"
      print("[2단계] Content_2 생성 완료")
    except:
      data['comment'] = "크롤링 실패"
      print(">> Content_1 크롤링 실패")
  return data

if __name__ == '__main__':
  data = {'originallink': "https://blackdoggy.xyz/archives/87649", "blogstyle":"wordpress", 'reset':'reset'}
  data = myContent_2(data)
  print(data)