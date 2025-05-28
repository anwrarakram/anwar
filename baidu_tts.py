# coding=utf-8
import sys
import json

def text_to_speech(text, out_path):
    IS_PY3 = sys.version_info.major == 3
    if IS_PY3:
        from urllib.request import urlopen, Request
        from urllib.error import URLError
        from urllib.parse import urlencode, quote_plus
    else:
        import urllib2
        from urllib import quote_plus, urlencode
        from urllib2 import urlopen, Request, URLError

    API_KEY = '1Ww9KhEm32rkDBDFw'
    SECRET_KEY = '8IbDDu2Y32F'

    # 语音合成参数
    PER = 4    # 发音人
    SPD = 5    # 语速
    PIT = 5    # 音调
    VOL = 5    # 音量
    AUE = 6    # 音频格式，6=wav

    FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
    FORMAT = FORMATS[AUE]

    CUID = "2"

    TTS_URL = 'ht32o'
    TOKEN_URL = 'http:/32

    class DemoError(Exception):
        pass

    def fetch_token():
        params = {
            'grant_type': 'client_credentials',
            'client_id': API_KEY,
            'client_secret': SECRET_KEY
        }
        post_data = urlencode(params)
        if IS_PY3:
            post_data = post_data.encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req, timeout=5)
            result_str = f.read()
        except URLError as err:
            raise DemoError('token http response http code : ' + str(err.code))
        if IS_PY3:
            result_str = result_str.decode()
        result = json.loads(result_str)
        if ('access_token' in result and 'scope' in result):
            if SCOPE not in result['scope'].split(' '):
                raise DemoError('scope is not correct')
            return result['access_token']
        else:
            raise DemoError('MAYBE API_KEY or SECRET_KEY not correct')

    try:
        token = fetch_token()
    except Exception as e:
        print("获取token失败:", e)
        return False

    tex = quote_plus(text)
    params = {
        'tok': token,
        'tex': tex,
        'per': PER,
        'spd': SPD,
        'pit': PIT,
        'vol': VOL,
        'aue': AUE,
        'cuid': CUID,
        'lan': 'zh',
        'ctp': 1
    }
    data = urlencode(params)
    if IS_PY3:
        data = data.encode('utf-8')
    req = Request(TTS_URL, data)
    try:
        f = urlopen(req)
        result_str = f.read()
        headers = dict((k.lower(), v) for k, v in f.headers.items())
        if 'content-type' not in headers or 'audio/' not in headers['content-type']:
            print("返回结果不是音频，可能有错误")
            print(result_str.decode('utf-8') if IS_PY3 else result_str)
            return False
        with open(out_path, 'wb') as of:
            of.write(result_str)
        print("语音合成成功，文件保存为：", out_path)
        return True
    except URLError as err:
        print('请求错误，HTTP code:', err.code)
        return False

# 用法示例
if __name__ == '__main__':
    text_to_speech("欢迎使用百度语音合成。", "output.wav")
