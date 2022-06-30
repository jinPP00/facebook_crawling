# https://docs.gspread.org/en/latest/user-guide.html#opening-a-spreadsheet
# 새로운 스프레드 추가시 spreadsheet@spiritual-storm-330801.iam.gserviceaccount.com 공유.
import gspread
import pickle
import pandas as pd

# now_path = 'C:/python/workspace/블로그글쓰기'
now_path = '.'

# 구글시트 불러오기
def SheetLoad(myFile, myWorksheet):
  gc = gspread.service_account(filename=f'{now_path}/libdata/googlesheet.json')
  sh = gc.open(myFile)
  worksheet = sh.worksheet(myWorksheet)
  df = pd.DataFrame(worksheet.get_all_records())
  return df, worksheet

# 구글시트 작성
def sheetWrite(myFile, myWorksheet, *values):
  df, worksheet = SheetLoad(myFile, myWorksheet)
  writeValue = []
  for i in values:
    writeValue.append(i)
  worksheet.append_row(writeValue)
  print("시트작성", myFile, myWorksheet, writeValue)

#피클 저장
def pickleSave(myFile, myWorksheet, savePickle):
  df, worksheet = SheetLoad(myFile, myWorksheet)
  # df = pd.DataFrame(worksheet.get_all_records())
  with open(f'''{now_path}/data/{savePickle}.pickle''',"wb") as fw:
    pickle.dump(df, fw)
  print("피클 저장 완료", f'''./{savePickle}.pickle''')

#피클 링크 로드
def pickleload(loadPickle):
  with open(f'''{now_path}/data/{loadPickle}.pickle''', 'rb') as f:
    df = pickle.load(f)
  return df

def DeleteRow(worksheet):
  worksheet.delete_row(2)
  print("크롤링 첫행 삭제완료")

if __name__ == '__main__':
  # df, worksheet = SheetLoad("내포스팅", "워프page")
  # df, worksheet = SheetLoad("실시간포스팅", "워프page")
  # print(df)

  # pickleSave("내포스팅","내계정","내계정")
  # pickleSave("내포스팅","포잡","포잡")
  # pickleSave("내포스팅","포페북","포페북")

  df1, worksheet1 = SheetLoad("내포스팅", "내계정")
  df2, worksheet1 = SheetLoad("내포스팅", "포잡")

  print(df1)
  print(df2)