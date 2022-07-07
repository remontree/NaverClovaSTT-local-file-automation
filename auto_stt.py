import clova
import os
from tqdm import tqdm
import requests
import json

class Stt:
    def __init__(self,address,FileType,save,invoke_url,secret):
        self.success = 0
        self.address = address
        self.filetype = ['.mp3','.wav','.m4a']
        self.filetype = self.filetype[FileType-1]
        self.save = save
        self.invoke_url = invoke_url
        self.secret = secret
        self.doc_list,self.doc_name = self.get_document(address)

        self.get_document(self.address)
        self.run_stt()

    def get_document(self, address):
        doc = []
        name = []
        file = os.listdir(address)
        for i in file:
            if self.filetype in i:
                doc.append(address + "\\" + i)
                name.append(i[:-4])
        return doc,name

    def run_stt(self):
        os.mkdir(self.save+"\\stt result")
        for i in tqdm(range(len(self.doc_list))):
            try:
                res = clova.ClovaSpeechClient(self.invoke_url,self.secret).req_upload(file=self.doc_list[i], completion='sync')
                data = json.loads(res.text)
                with open(self.save+"\\stt result\\"+self.doc_name[i]+".txt", 'w', encoding='UTF-8-sig') as file:
                    file.write(data['text'])
                    self.success += 1
            except:
                print("api를 호출하는데 문제가 생겼습니다.")
                break
        print("변환에 성공한 파일: "+str(self.success))

if __name__ == '__main__':
    address = input("음성파일이 저장되어 있는 폴더의 주소를 입력하세요:")
    save = input("파일을 저장할 주소를 선택하세요:")
    invoke_url = input("invoke_url:")
    secret = input("secret key:")
    FileType = int(input("""파일 확장자를 선택하세요
[1].mp3
[2].wav
[3].m4a
press the number:"""))
    print("프로그램 실행 중....")
    Stt(address,FileType,save,invoke_url,secret)
    print("프로그램 종료")
    os.system("pause")
