import 쓰기구블, sys, 쓰기워프
import 구글시트
import fb_control

def blog_random_select(subject):
  myblog_df, worksheet = 구글시트.SheetLoad("내포스팅", "내계정")
  print(myblog_df)
  myAccount = 쓰기구블.블로그랜덤선택(myblog_df, subject)
  print(myAccount['site'], "랜덤선택")
  return myAccount

def blog_posting(data, myAccount, pubstatus):
  if myAccount['style'] == "g":
    data = 쓰기구블.main(sys.argv, data, myAccount, pubstatus) 
  elif myAccount['style'] == "w":
    print(">> 워프포스팅", myAccount['site'])
    # data['imgurl'], attachment_id = 쓰기워프.attach_post(data, myAccount)
    data = 쓰기워프.wordpressPost(data, myAccount, pubstatus, "")
  return data

def gsheet_write(data, pubstatus):
  if pubstatus!="draft":
    myFile, myWorksheet = "내포스팅","포페북"
    구글시트.sheetWrite(myFile, myWorksheet, "페북", "x", data['keyword'], data['title_2'], data['originallink'], data['link'], data['imgurl'][0])

def txt_write(keyword):
    with open('./블로그쓰기완.txt', 'a', encoding="UTF-8") as f:
        f.write(f'''{keyword}\n''')
    print(">> txt 쓰기완료")

def main():
  user, db, storage = fb_control.firebase_credit("./libdata/auth3.json")
  fb_data = fb_control.fb_complex_db_load(db,"myblog", "status", "작업중")
  if not fb_data.val():
    print("값이 없습니다.")
  else:
    for user in fb_data.each():
      mytitle = user.key()
      data = user.val()
    print(mytitle)
    myAccount = blog_random_select("페북")
    pubstatus="draft"
    data = blog_posting(data, myAccount, pubstatus)
    fb_control.fb_db_delete(db, "myblog",mytitle)
    gsheet_write(data, pubstatus)
    # txt_write(data['link'])

if __name__ == '__main__':
  main()