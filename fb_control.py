import pyrebase
import json
import random

def firebase_credit(auth_path):
  global user, db, storage
  with open(auth_path) as f:
      config = json.load(f)
  firebase = pyrebase.initialize_app(config)
  auth = firebase.auth()
  user = auth.sign_in_with_email_and_password("elkoaw38@naver.com", "jinhong12!@")
  db = firebase.database()	# 파이어베이스 db 사용
  storage = firebase.storage() 
  return user, db, storage

#fb스토리지 업데이트(path 지정(fb_path) 따로 하면 안됨.)
def fb_storage_update(foldname,filename,imgpath):
    user, db, storage = firebase_credit("./libdata/auth3.json")
    storage.child("images").child(foldname).child(filename).put(imgpath)
    fb_imgurl = storage.child("images").child(foldname).child(filename).get_url(user['idToken'])
    # fb_imgurl = storage.child("images").child(foldname).child(filename).get_url(fb_upload['downloadTokens'])
    return fb_imgurl

#fb 업데이트
def fb_db_update(db, foldname,filename,update_data):
	db.child(foldname).child(filename).update(update_data)

#fb 추출
def fb_db_load(db, foldname,filename):
  fb_data = db.child(foldname).child(filename).get()		#키워드 데이터 추출
  fb_Data = fb_data.val()
  return fb_Data

def fb_complex_db_load(db, foldname, sortname, sortcont):
  # print(len(db.child(foldname).order_by_child(sortname).equal_to(sortcont).get()),"개")
  fb_data = db.child(foldname).order_by_child(sortname).equal_to(sortcont).limit_to_first(1).get()
  return fb_data

def fb_db_keyload(db, foldname,filename):
  fb_keydata = db.child(foldname).child(filename).shallow().get()		#전체 데이터 키값 추출
  # print(fb_keydata.val()) 
  fb_keyData = fb_keydata.val()
  return fb_keyData

def fb_db_delete(db, foldname,filename):
  db.child(foldname).child(filename).remove()

# FB에서 키워드 추출
def firebase_db(db, foldname, keyword):
  if not keyword:
      keys = db.child(foldname).child().shallow().get().val()   #키값으로 조회
      # print(">> 저장된 상품리스트:", keys)
      keyword = random.choice(list(keys)) 
  else:
      pass
  fb_data = db.child(foldname).child(keyword).get()   #키워드 데이터 추출
  product_all = fb_data.val()
  return keyword, product_all

def fb_complex_db_load(db, foldname, sortname, sortcont):
  fb_data = db.child(foldname).order_by_child(sortname).equal_to(sortcont).get()
  print(">> FB컨텐츠 갯수:",len(fb_data.val()),"개")
  fb_data = db.child(foldname).order_by_child(sortname).equal_to(sortcont).limit_to_first(1).get()
  return fb_data

def fb_all_data():
  fb_data = []
  # users_by_key = db.child("myblog").order_by_key().get()
  users_by_key = db.child("myblog").get()
  for user in users_by_key.each():
    fb_data.append(user.key())
    print(user.key())
  print(fb_data)
  return fb_data

if __name__ == '__main__':
  db, storage, user= firebase_credit()
  # fb_keydata = db.shallow().get()
  # print(fb_keydata.val())
  # fb_keyData = fb_db_keyload('myblog',"")
  # print(fb_keyData)

  # fb_data = fb_complex_db_load("myblog", "status", "작업중")
  # print(fb_data.val())

  fb_data = fb_all_data()


  # mydata = {"title":"567", "Content":"123", "status":"작업중", "link":"www.naver.com", "keyword":"내키워드"}
  # db.child("facebook").child(mydata['status']).child(mydata['title']).update(mydata)
  # db.child("facebook").child(mydata['status']).child(mydata['title']).remove()

  # img_path = "./libdata/test.png"
  # foldname = mydata['keyword']
  # filename = mydata['keyword']+"01"
  # fb_imgurl = fb_storage_update(foldname,filename,img_path)
  # print(fb_imgurl)

