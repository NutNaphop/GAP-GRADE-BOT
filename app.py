import module.webcraw as wc 
import module.database as db 
import module.flex as flex 
import module.textChecker as tc
from flask import Flask, request, abort , jsonify
import requests
import json
import os 

from dotenv import dotenv_values
config = dotenv_values(".env")
Channel_access_token = config['API_KEY']


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        payload = request.get_json()
        # print(payload)
        events = payload['events']
        for event in events:
            event_type = event['type']
            Reply_token = event['replyToken']
            if event_type == 'message':
                message = event['message']['text']
                userID = event['source']['userId']
                userName = getUserID(userID , Channel_access_token)
                print(message)
                if tc.detect_gap(message) and len(message) == 3:
                    # print(Reply_token)
                    # print(Reply_message)
                    Reply_message = f"สวัสดีคุณ {userName[0]['displayName']} วันนี้มีอะไรให้ Gap ช่วยหรือเปล่าครับ 😊😊"
                    # print(userName)
                    ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                    msg = flex.sendQuickReply(userID)
                    replyFlexMessage(msg , Channel_access_token)
                    return request.json, 200
                elif "สอนสมัครสมาชิก" in message : 
                    Reply_message = 'หากต้องการลงชื่อในระบบต้องพิมดังนี้ "สมัคร b6xxxxxxxxx password" ใช้บัญชีนนทรีนะ 🤔🤔'
                    ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                    return request.json, 200
                
                elif "สมัคร" in message : 
                    userData = message.split()
                    if len(userData) != 3 : 
                        Reply_message = "ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง ❌❌"
                        ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                        return request.json , 200
                    else : 
                        print(userID , userData[1] , userData[2])
                        if db.findDup(userID , userData[1]) :
                            Reply_message = "ไม่สำเร็จ มีข้อมูลนี้อยู่ในระบบแล้ว ❌❌"
                            ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                            return request.json , 200
                        else :
                            db.insertData(userID , userData[1] , userData[2])
                            Reply_message = "สำเร็จ!!!! ลงทะเบียนเรียบร้อยแล้ว ✅✅"
                            ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                            return request.json, 200
                    
                elif "ผลการเรียน" in message : 
                    data = db.findID(userID)
                    if data == -1 :
                        Reply_message = 'กรุณาลงทะเบียนก่อน โดยพิมพ์ "สมัคร b6xxxxxxxxx password" ในช่องข้อความ ใช้บัญชีนนทรีนะ 🤔🤔'
                        ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                        return request.json , 200
                    subData =  wc.login(data[1] , data[2])
                    if subData == -1 : 
                        Reply_message = "ไม่สามารถเข้าถึงข้อมูลได้ เว็บอาจจะล่ม หรือ รหัสผ่านผิด แนะนำติดต่อ Admin"
                        ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                        return request.json , 404
                    else :
                        msg = flex.sendMessage(userID, subData)
                        replyFlexMessage(msg , Channel_access_token)
                        return request.json , 200
                elif "ติดต่อ" in message :
                    Reply_message = "ติดต่อเราได้ที่ อีเมล : nutnaphop24@gmail.com 📫📫" 
                    ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                    return request.json , 200
                elif "เกี่ยวกับ" in message :
                    Reply_message = '''สวัสดีครับผม GAP สร้างขึ้นมาเพื่อช่วยในการดูเกรดของนิสิตทุกคนเลย!!! (ˉ▽￣～) ผมถูกสร้างขึ้นเพราะคนๆหนึ่ง เริ่มไม่ชอบที่จะเปิดเว็บมอเวลาดูเกรด เพราะกว่าจะล็อคอินนู้นนนี่นั้นมันก็ช้า ดังนั้น ก็สร้างมันขึ้นมาเลยละกัน จะได้ประหยัดเวลาขึ้นหน่อย ใช่ไหมละ ┗|｀O′|┛ !!! 
บอทตัวนี้ทำขึ้นมาโดย นิสิตวิทย์คอมท่านหนึ่ง 💻'''
                    ReplyMessage(Reply_token, Reply_message, Channel_access_token)
                    return request.json , 200
                elif request.method == 'GET':
                    return 'GET port 80 : Getting Started', 200
                else:
                    Reply_message = 'Gap ไม่รู้จะตอบอะไรดี คนเขียนไม่ได้ตั้งไว้ 😥😥 ถ้ามีอะไรให้ Gap ช่วย ให้พิมพ์ GAP หรือ gap นะครับ ขอบคุณครับ'
                    ReplyMessage(Reply_token , Reply_message , Channel_access_token)
                    abort(400)
            elif event_type == 'source' : 
                    userID = event['source']['userId']
                    print(userID)
                    getUserID(userID , Channel_access_token)
        return request.json , 200
    elif request.method == 'GET':
        return 'GET port 80 Start', 200
    else : 
        abort(400)
@app.route('/webhook', methods=['GET'])
def hello():
    return 'Get port 80', 200

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Acees_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    data = {
        "replyToken": Reply_token,
        "messages": [{
            "type": "text",
            "text": TextMessage
        }]
    }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    return r.json(), r.status_code

def getUserID(Profile_ID , Line_Access_Token) : 
    LINE_API = f'https://api.line.me/v2/bot/profile/{Profile_ID}'
    Authorization = 'Bearer {}'.format(Line_Access_Token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }

    r = requests.get(LINE_API , headers=headers)
    print(r.json())
    return r.json() , 200 

def replyFlexMessage(message , Line_Access_token) : 
    LINE_API = f'https://api.line.me/v2/bot/message/push'
    Authorization = 'Bearer {}'.format(Line_Access_token)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': Authorization
    }
    data = json.dumps(message)
    r = requests.post(LINE_API , headers=headers , data=data)
    print('Sending')
    return r.json(), 200

@app.route('/register' , methods=['POST']) 
def getRegister() :
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=80)
