# -*- coding: utf-8 -*-
import 링크만들기
import 이미지삽입
from 본문크롤링 import cleanhtml
import re
import random

def h_id_make(data):
	Content_2 = data['Content_2']
	cnt = 0
	if "<h2>" in Content_2:
		for i in range(Content_2.count("<h2>")):
			Content_2 = Content_2.replace("<h2>",f'''<h2 id="list{cnt+1}">''',1)
			cnt +=1
	if "<h3>" in Content_2:
		for i in range(Content_2.count("<h3>")):
			Content_2 = Content_2.replace("<h3>",f'''<h3 id="list{cnt+1}">''',1)
			cnt +=1
	else:
		pass
	data['Content_2'] = Content_2
	return data
	
# 최종 수정후 목차 생성
def make_index(data):
	if "목차" not in data['Content_2'] and data['blog_style'] != "naver":
		content = data['Content_2']
		data = h_id_make(data)
		if "<h3" in content or  "<h2" in content:
			myindex = f'''<div id="myindex" style="padding:10px 5px 0px 15px;border: 1px solid #333;margin-bottom: 15px;background-color: #FFFBFA;">
<p style="font-size:23px;text-align:left; margin-top:0px; margin-bottom:10px;"><b>목차</b></p>
<ul class="mylist" style="list-style-type: circle;padding-bottom: 10px;margin-left: 30px;">'''
			h3tag = re.findall("<h3.*?>.*?.h3>",content)
			h2tag = re.findall("<h2.*?>.*?.h2>",content)
			myhtag = h2tag + h3tag 
			for i in range(len(myhtag)):
				myindex += f'''
	<li style="text-align:left;" data-ke-size="size16">
		<a style="color:#4b70fd;" href="#list{i+1}"><b>{cleanhtml(myhtag[i])}</b></a>
	</li>'''
			myindex += f'''\n</ul>
</div>'''
			content = myindex + content
		else:
			pass
		data['Content_2'] = content
	else:
		print("목차가 있습니다.")
	return data

def h_style(data):
	if "<h2" in data['Content_2']:
		print(data['Content_2'].count("<h2"))
		print("h2 스타일변경")
		ran_h2_style = random.choice(["#58ACFA","#70819A","#58ACFA"])
		print(ran_h2_style)
		h2_style = f'''<h2 style="min-height:50px;color:#ffffff;text-align:left;border-style:dashed;border-radius:25px 5px 25px 5px;border-color:{ran_h2_style};background-color:{ran_h2_style};padding:10px 0px 0px 10px;font-family:'Nanum Gothic';font-size:24px;"'''
		data['Content_2'] = data['Content_2'].replace("<h2",h2_style)
	if "<h3" in data['Content_2']:
		print("h3 스타일변경")
		h3_style = ['''\
<h3 style="min-height:50px;text-align:left;box-sizing:border-box;border-right-width:0px;margin: 5px 10px 20px 0px;letter-spacing: 1px;line-height: 1.5;border-top-width:0px;padding:10px 5px 5px 5px;font-family:'Nanum Gothic';font-size:22px;border-bottom:#FA8258 2px solid;border-left:#FA8258 15px solid;"''', '''<h3 style="min-height:50px;color:#ffffff;text-align:left;border-style:dashed;border-radius:25px 5px 25px 5px;border-color:#F78181;font-family:'Nanum Gothic';padding:10px 0px 0px 10px;margin-bottom:8px;font-size:22px;background-color:#F78181;"''']
		ran_h3_style = random.choice(h3_style)
		data['Content_2'] = data['Content_2'].replace("<h3", ran_h3_style)
	if "<h4>" in data['Content_2']:
		h4_style = ['''<h4 style="text-align:left;border-style:solid;border-width: 0 0 0 5px;padding:8px;word-break: break-all;border-color:#F78181;background-color:#fbfbfb; margin-left:5px;font-size:20px;">''','''<h4 style="font-size:20px;padding:13px; background-color: #fff7f4; color:#7D1C24;">''']
		ran_h4_style = random.choice(h4_style)
		data['Content_2'] = data['Content_2'].replace("<h4>", ran_h4_style)
	if "<h5>" in data['Content_2']:
		data['Content_2'] = data['Content_2'].replace("<h5>",'''<h5 style="border-style:solid;border-width:1px 0px 1px 0px;padding:10px;word-break:break-all;border-color:#df301a;background-color:#FFFBFA;margin-left:20px;margin-right:20px;margin-bottom:20px;text-align:center;">''')
	return data

def myConverter(data):
	# data['Content_2'] = 링크만들기.관련페북링크(data)
	# data['Content_2'] = 링크만들기.관련페북큰링크(data)
	data['Content_2'] = 링크만들기.yoyo(data)
	data['Content_2'] = data['Content_2'].replace("YTB","").replace("$$$$$$","")
	if data['subject'] == "페북":
		data['Content_2'] = data['Content_2'].replace("******","LINK",3)

	data = 이미지삽입.originalImage(data, "ori")
	data = 이미지삽입.urlconverter(data['modified_img'], data)
	data['Content_2'] = 링크만들기.관련링크추가(data)
	data['Content_2'] = 링크만들기.관련버튼추가(data)
	data['Content_2'] = 링크만들기.관련큰링크(data)
	data['Content_2'] = 링크만들기.이전글링크(data)
	# data = make_index(data)
	# data = h_style(data)
	data['Content_2'] = data['Content_2'].replace("ADSENSE1", '''\n<div id="ad1"></div>''').replace("ADSENSE2", '''\n<div id="ad2"></div></div>''').replace("ADSENSE3", '''\n<div id="ad3"></div>''')
	return data

if __name__ == '__main__':
	data = {}
	# data['Content_2']= '''<h3> 안녕하세요 </h3> <h3> 반갑습니다 </h3> <h3> 안녕하세하이이요 </h3>'''
	# data['Content_2'] = make_index(data['Content_2'])
	# print(data)

	# with open('mycontents.html', 'w', encoding="UTF8") as f:
	# 	f.write(data['Content_2'])


		# if '<style>' not in data['Content_2']:
	# 	print("style_css 추가")
	# data['Content_2'] = f'''{style_css()}{data['Content_2']}'''