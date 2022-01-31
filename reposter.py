import requests,time
from configparser import ConfigParser

def configsetup():
    config = ConfigParser()
    config.read('config.ini')
    token = (config['main']['token'])
    readchannel = (config['main']['readchannel'])
    postchannel = (config['main']['postchannel'])
    timesleep = (config['main']['timesleep'])
    api = (config['main']['api'])
    header = {
        'authorization' : token
    }
    return readchannel, postchannel, api, header, config, timesleep

def checkandpost(readchannel, postchannel, api, header, config, timesleep):
    while True:
        #grab all chat from readchannel
        messages = requests.get(api + '/channels/' + readchannel + '/messages',headers=header)
        #convert to json
        messagejson = messages.json()
        #grab the chatid of the lattest chat
        latestchatid = messagejson[0]['id']
        #grab value of currentchatid
        curentchatid = (config['main']['currentchatid'])
        #if value empty set to latestchat value
        if not curentchatid:
            config.set('main', 'currentchatid', latestchatid)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        if latestchatid != curentchatid:
            config.set('main', 'currentchatid', latestchatid)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            latestchatcontent = messagejson[0]['content']
            payload = {
                "content": latestchatcontent
            }
            requests.post(api + '/channels/' + postchannel + '/messages',headers=header, data=payload)
        time.sleep(timesleep)
        

if __name__ == '__main__':
    readchannel, postchannel, api, header, config, timesleep = configsetup()
    checkandpost(readchannel, postchannel, api, header, config, timesleep)