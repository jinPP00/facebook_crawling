from __future__ import print_function  #파이썬 2, 3에서 모두 쓸 수 있게 만드는 함수
from oauth2client import client
from googleapiclient import sample_tools
import sys		#명령행에서 인수 전달하기 - sys.argv

# subject로 랜덤블 선택
def 블로그랜덤선택(df, subject):
	if len(df.loc[df['subject'] == subject].reset_index(drop=True)) > 0:
		subject_df = df.loc[df['subject'] == subject].reset_index(drop=True)
	else:
		subject_df = df
	df = subject_df.sample(n=1).reset_index(drop=True)
	myAccount = {'style':df.loc[0,'style'], 'site': df.loc[0,'site'], 'id': df.loc[0,'id'],'password': df.loc[0,'password']}
	print("블계정", myAccount)
	return myAccount

def main(argv, data, myAccount, pubstatus):
	id = int(myAccount['id']) 
	title = data['title_2']
	content = data['Content_2']
	if pubstatus == "publish":
		pubstatus = False
	else: 
		pubstatus = True
	service, flags = sample_tools.init(
			# argv, 'blogger', 'v3', __doc__, __file__,   # __file__ 현재 수행중인 코드를 담고 있는 파일의 위치한 Path
			argv, 'blogger', 'v3', __doc__,"./data/client_secrets.json",
			scope='https://www.googleapis.com/auth/blogger')
	print(title)
	try:
		print(">> 구글블로그 포스팅 시도")
		users = service.users()
		thisuser = users.get(userId='self').execute()
		blogs = service.blogs()
		thisusersblogs = blogs.listByUser(userId='self').execute()
		for blog in thisusersblogs['items']:
				pass
		posts = service.posts()
		# print(thisusersblogs['items'])
		# for i in range(len(thisusersblogs['items'])):
		#     print(i,thisusersblogs['items'][i]['id'], thisusersblogs['items'][i]['url'])
		# blog = thisusersblogs['items'][blognum]
		# if blog['id'] == blog_Id:
		body = {
				"kind": "blogger#post",
				"id": id,
				"title": title,
				"content": content,
				}
		request = posts.insert(blogId=myAccount['id'], body=body, isDraft=pubstatus)  #isDraft True 임시보관
		response = request.execute()
		# print(response)
		data['link'] = response["url"]
		bloglink = "https://www.blogger.com/blog/posts/" + str(myAccount['id'])
		print("구블 포스팅 완료", data['link'])
		print(bloglink)
	except client.AccessTokenRefreshError:
			print ('error')
	return data

if __name__ == '__main__':
	data = {'title':"테스트", 'title_2':"테스트",'keyword':"테스트 123", 'Content_2':"테스트입니다", "subject":"잡","subject_2":"x" }
	pubstatus = "draft"
	myAccount = {'id': 7160628493176839344, 'password': ''}
	# myAccount = gbAccount(myAccount)
	data = main(sys.argv, data, myAccount, pubstatus)