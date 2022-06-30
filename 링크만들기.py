import random, re
from datetime import datetime
import pandas as pd
import requests
import urllib.request
from 구글시트 import pickleload, SheetLoad

# df = pickleload("포잡")
df, worksheet1 = SheetLoad("내포스팅", "포페북")

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def mypickleLoad(data):
  global subject_df
  subject = data['subject']
  subject_2 = data['subject_2']
  count = data['Content_2'].count("BTN") + data['Content_2'].count("******") + data['Content_2'].count("LINK") + 3
  if subject == "잡":
    subject_df = df.sample(n=count).reset_index(drop=True)
  else:
    if subject_2 == "x":
      print("subject_2 없습니다.")
      subject_df = df.loc[df['subject'] == subject].reset_index(drop=True)
    else:
      subject_2_df = df.loc[df['subject_2'] == subject_2].reset_index(drop=True)
      subject_1_df = df.loc[df['subject'] == subject].reset_index(drop=True)
      subject_df = pd.concat([subject_2_df, subject_1_df], ignore_index=True) #데이터프레임 합치기
      subject_df = subject_df.head(count)
    if len(subject_df) < count:
      total_df = df.sample(n=count-len(subject_df))
      subject_df = pd.concat([subject_df, total_df], ignore_index=True)
  return subject_df

def 관련버튼추가(data):
  content = data['Content_2']
  if "BTN" in content:
    subject_df = mypickleLoad(data)
    btncount = content.count("BTN")
    a = random.sample(range(len(subject_df)), btncount)
    if 'blog_style' not in data or data['blog_style'] == 'blogger':
      for i in range(len(a)):
        BTNtitle = subject_df.loc[a[i], 'keyword']
        BTNLink = subject_df.loc[a[i], 'link']
        btn_color = ["#0080ff", "#df262a", "#fa823e","#4CAF50"]
        btn_radius = ["10px","15px","20px","30px"]
        ran_btn_color = random.choice(btn_color)
        ran_btn_radius = random.choice(btn_radius)
        content = content.replace("BTN",  f'''
<p><br></p>
<div style="text-align:center;">
  <a href="{BTNLink}" target="_self" style="background-color:{ran_btn_color};color:#fff;border-radius:{ran_btn_radius};padding:15px 20px;font-size:21px;text-decoration:none;"><b>▼ {BTNtitle}</b></a>
</div>
<p><br></p>''',1)
      print("관련버튼 추가성공")
    elif data['blog_style'] == "naver":
      for i in range(len(a)):
        link = subject_df.loc[a[i], 'link']
        content = content.replace("BTN",link,1)
  else:
    print("BTN 없음")
  return content

def 관련링크추가(data):
  content = data['Content_2']
  if "******" in content:
    print("콘텐츠내 ****** 있음")
    linkCount = content.count("******")
    try:
      subject_df = mypickleLoad(data)
      a = random.sample(range(1, len(subject_df)), linkCount)
      if 'blog_style' not in data or data['blog_style'] == 'blogger':
        for i in range(len(a)):
          title = subject_df.loc[a[i], 'title_2']
          link = subject_df.loc[a[i], 'link']
          keyword = subject_df.loc[a[i], 'keyword']
          imgurl = subject_df.loc[a[i], 'imgurl']
          tokens = daumBlog(title)
          ran_Num = random.randrange(0, len(tokens['documents'])) 
          mycontent = cleanhtml(tokens['documents'][ran_Num]['contents'])
          summary = f'''{mycontent[0:88]}...'''
          content = content.replace("******", f'''
  <div class="vlp-link-container" id="grid" style="margin:10px auto;width:95%;display:grid;border:1px solid; border-color: #BDBDBD; border-radius:0.2em;cursor:pointer;" onclick="location.href="{link}";">
    <div class="vlp-link-image" style="max-height:300px; overflow:hidden;">
      <a href="{link}"><img alt="{keyword}" class="linkimage" style="width:100%;height:100%;" src="{imgurl}"></a>
    </div>
    <div class="vlp-link-text-container">
      <div class="vlp-link-title">{title}</div>
      <div class="vlp-link-summary" style="color:#909090; font-size:14px;">{summary}</div>
      <div style="color:#1e73be;font-size:16px;">...Read more</div>
    </div>
  </div>''', 1)
      elif data['blog_style'] == "naver" or data['blog_style'] == "tistory":
        for i in range(len(a)):
          link = subject_df.loc[a[i], 'link']
          content = content.replace("******", link,1) 
      else:
        print("관련링크 추가성공")
    except:
      content = content.replace("******", "",1) 
  else:
    print("****** 없음")
  return content

def 관련페북링크(data):
  subject_df = pickleload("포페북")
  content = data['Content_2']
  if "&&&&&&" in content:
    print("콘텐츠내 &&&&&& 있음")
    linkCount = content.count("&&&&&&")
    a = random.sample(range(len(subject_df)), linkCount)
    pubdate = datetime.now()
    if 'blog_style' not in data or data['blog_style'] == 'blogger':
      for i in range(linkCount):
        title = subject_df.loc[a[i], 'title_2']
        link = subject_df.loc[a[i], 'link']
        imgurl = subject_df.loc[a[i], 'imgurl']
        content = content.replace("&&&&&&", f'''
<div class="vlp-link-container" id="grid" style="border: 1px solid; padding: 2px; border-color: #BDBDBD; border-radius: 0.2em; display: grid; margin:0 auto; cursor: pointer;" onclick="location.href='{link}';"> 
  <div class="vlp-link-image" style="max-height:300px; overflow:hidden;">
    <a href="{link}"><img class="linkimage" style="height:100%;width:100%;" src="{imgurl}"></a>
  </div>
  <div class="vlp-link-text-container">
    <div class="vlp-link-title"><b>{title}</b></div>
    <div class="news_date" style="color:green; font-size:13px;">{pubdate}</div>
    <div class="news_author" style="color:blue;font-size:13px;">투데이이슈</div>
  </div>
</div>
''', 1)
    else:
      for i in range(len(a)):
        link = subject_df.loc[a[i], 'link']
        content = content.replace("&&&&&&", f'\n{link}',1) 
    print("관련페북 추가성공")
  else:
    print("&&&&&& 없음")
  return content

def 관련페북큰링크(data):
  subject_df = pickleload("포페북")
  content = data['Content_2']
  if "$$$$$$" in content:
    print("콘텐츠내 $$$ 있음")
    pubdate = datetime.now()
    linkCount = content.count("$$$$$$")
    a = random.sample(range(0, len(subject_df)), linkCount)
    if 'blog_style' not in data or data['blog_style'] == 'blogger' or data['blog_style'] == 'tistory':
      for i in range(linkCount):
        title = subject_df.loc[a[i], 'title_2']
        link = subject_df.loc[a[i], 'link']
        imgurl = subject_df.loc[a[i], 'imgurl']
        content = content.replace("$$$$$$",f'''
<div class="news-box" style="margin:0 auto; min-height:430px;border:0.5px solid #BDBDBD; border-radius:0.2em;cursor:pointer; max-width:430px; display:grid;" onclick="location.href='{link}'">
  <div class="news-image-container" style="height:300px;overflow:hidden;">
    <a href="{link}"><img alt="저금리 소상공인대출 신청" class="news_image" style="width:100%;height:100%;" src="{imgurl}"></a>
  </div>
  <div class="news-text-container" style="padding:8px;">
    <div class="news_title" style="font-weight:bold; font-size:19px;">{title}</div>
    <div class="news_date" style="color:green; font-size:13px;">{pubdate}</div>
    <div class="news_author" style="color:blue;font-size:13px;">투데이이슈</div></div>
</div>''', 1)
    elif data['blog_style'] == "naver":
      for i in range(len(a)):
        link = subject_df.loc[a[i], 'link']
        content = content.replace("$$$$$$", link,1) 
    print("관련페북큰링크 추가성공")
  else:
    print("$$$$$$ 없음")
  return content

def 관련큰링크(data):
  content = data['Content_2']
  if "LINK" in content:
    print("LINK 있음")
    linkCount = content.count("LINK")
    try:
      keyword = data['keyword']
      encText = urllib.parse.quote(keyword)
      req = requests.get(f'https://s.kimanote.com/news/?query={encText}')
      mylinktokens = req.json()
      if 'blog_style' not in data or data['blog_style'] == 'blogger' or data['blog_style'] == 'tistory':
        try:
          for i in range(linkCount):
            title = mylinktokens[i]['title']
            if len(mylinktokens[i]['desc']) > 90:
              desc = f'''{mylinktokens[i]['desc'][0:90]}...'''
            else:
              desc = mylinktokens[i]['desc']
            link = mylinktokens[i]['link']
            img = mylinktokens[i]['img']
            author = mylinktokens[i]['author']
            print(mylinktokens)
            content = content.replace("LINK",f'''
<div class="wrap" style="margin:10px auto; width:380px;">
  <div class="news-box" style="border:1px solid #333; cursor:pointer;" onclick="location.href='{link}'">
    <div class="news-image" style="height:300px; overflow:hidden;">
      <a href="{link}">
        <img src='{img}' alt="{keyword}" style="width:100%; height:100%;"></a>
    </div>
    <div class="content" style=padding:5px; ">
      <div class="title" style="font-weight:bold; padding:10px; font-size:16px;">{title}</div>
      <div class="desc" style="padding:10px; color:#909090;font-size:13px;">{desc}</div>
      <div class="author" style="padding:10px; color:blue;font-size:14px;">{author}</div>
    </div>
  </div>
</div>''', 1)
        except:
          content = content.replace("LINK","")
      elif data['blog_style'] == "naver":
          for i in range(linkCount):
            link = mylinktokens[i]['link']
            content = content.replace("LINK", link,1) 
      print("관련뉴스 추가성공")
    except:
      content = content.replace("LINK","")
  else:
    print("컨텐츠내 LINK 없음.")
    pass
  return content

def 이전글링크(data):
  content = data['Content_2']
  if "PRN" in content:
    subject_df = mypickleLoad(data)
    print(subject_df)
    linkCount = content.count("PRN")
    mytext = ["같이 보면 좋은 글  ▼", "추가로 함께보면 좋은 글  ▼", "많이 본 글보기 ▼", "함께 읽으면 좋은 글들", "유용한 정보 모음  ▼", "유용한 정보글 모음", "▼ 사람들이 많이 읽은 글들 ▼", "▼ 많은 본 글 모아보기", "읽어보면 유용한 정보 모음", "함께 읽으면 좋은 글 보기", "사람들이 많이본 글 다시보기", "사람들이 많이본 글  ▼", "추가로 확인할 정보", "다양한 정보 글모음"]
    mytext = random.choice(mytext)
    linkadd = f'''
<h4><b>{mytext}</b></h4>
<ul style="padding-left:5px;">'''
    # print(subject_df)
    a = random.sample(range(0,len(subject_df)), 4)
    for i in range(len(a)):
      title = subject_df.loc[a[i], 'title_2']
      link = subject_df.loc[a[i], 'link']
      linkadd += f'''
  <li style="margin-left:20px;">
    <span style="color:#006dd7;"><a style="color:#006dd7;" href="{link}" rel="noopener"><b>{title}</b></a></span>
  </li>'''
    linkadd +="</ul>"
    for i in range(linkCount):
      content = content.replace("PRN", linkadd)
    print("이전글링크 추가성공")
  else:
    print("컨텐츠내 PRN 없음")
    pass
  return content

def yoyo(data):
  content = data['Content_2']
  if "YTB" in content:
    keyword = data['keyword']
    print("YTB 있음")
    ytbcount = content.count("YTB")
    mytext = ["관련 있는 영상 보기  ▼", "함께보면 좋은 영상 보기  ▼", "많이 본 동영상보기 ▼", "함께 읽으면 좋은 영상", "관련된 유용한 영상정보 보기  ▼", "▼ 사람들이 많이 본 영상 ▼", "▼ 많은 본 영상 보기" , "같이 보면 좋은 영상","관련 영상 다시보기", "사람들이 많이본 동영상  ▼", "추가로 확인하면 좋을 영상", "관련 있는 영상 확인" ]
    mytext = random.choice(mytext)
    keyword = cleanhtml(keyword)
    ytbtokens = daumYoutube(keyword)
    ytb_list = []
    for i in range(len(ytbtokens['documents'])):
      if "http://www.youtube.com" in ytbtokens['documents'][i]['url']:
        ytb_list.append(ytbtokens['documents'][i])
        pass
    # print("유튜브리스트",ytb_list)
    if not ytb_list:
      print("검색결과 유튜브링크가 없습니다.")
      content = content.replace("YTB", "")
      pass
    else:
      a = random.sample(range(0, len(ytb_list)), ytbcount)
      for i in a:
        ytb_title = ytb_list[i]['title']
        ytb_url = f'''https://www.youtube.com/embed/{ytb_list[i]['url'].split('?v=')[-1]}'''
      ytb_content = f'''
<h4><b>{mytext}</b></h4><p data-ke-size="size16">{ytb_title}</p>
<div style="text-align:center;">
  <iframe src="{ytb_url}" width="400px" height="300px"></iframe>
</div>'''
      content = content.replace("YTB", f'{ytb_content}',1)
  else:
    print("컨텐츠내 YTB 없음")
    content = content.replace("YTB", "")
  return content 


def createFolder(title, content):
  directory = f'.\\output'
  with open(directory+f"\\{title}.html", 'w', encoding="UTF8") as f:
    f.write(content)
  print(">>", title, "html 만들기 완료")

if __name__ == '__main__':
  data = {"keyword": "test", "Content_2": "$$$$$$ LINK "}
  data['Content_2'] = 관련페북큰링크(data)
  data['Content_2'] = 관련버튼추가(data)
  data['Content_2'] =관련링크추가(data)
  # data['Content_2'] = 관련페북큰링크(data)  

  print(data)

  title, content = "test", data['Content_2']
  createFolder(title, content)





  #큰링크 만들기
# def 큰링크추가(Content_2, keyword):
#   linkCount = Content_2.count("LINK")
#   try:
#     for i in range(linkCount):
#       mylinktokens = naverNews(keyword)
#       print(mylinktokens)
#       summary = f'''{mylinktokens['description'][0:100]}...'''
#       Content_2 = Content_2.replace("LINK",f'''\
# <div class="wrap" style="margin:10px auto; max-width: 480px;">\
# <div class="news-box" style="border:1px solid #333; margin:10px auto;cursor: pointer;" onclick="location.href='{mylinktokens['link']}'">\
# <div class="news-image" style="width:100%;height:100%">\
# <a href="{mylinktokens['link']}"><img src='{mylinktokens['imgurl']}' onerror="this.src='{imgsrc}'" class="news-myimage" style='width:100%; height:100%;' alt="{keyword}"></a></div>\
# <div class="news-contentbox">
# <div class="news-title" style="font-weight:bold;">{mylinktokens['title']}</div>\
# <div class="news-desc" style="color:#666;">{summary}</div>\
# <div class="news-date" style="color:green; ">{mylinktokens['pubdate']}</div>\
# <div class="news-author" style="color:blue; ">{mylinktokens['author']}</div>\
# </div></div></div>''', 1)
#     print("관련뉴스 추가성공")
#   except:
#     Content_2 = Content_2.replace("LINK", "")
#     print("관련뉴스 추가실패")
#   return Content_2
