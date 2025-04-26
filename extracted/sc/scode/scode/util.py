def fwrite(path: str, text, encoding='cp949'):
    """
    It writes a text to a file
    
    :param path: The path to the file you want to write to
    :type path: str
    :param text: The text to be written
    :param encoding: The encoding of the file, defaults to cp949 (optional)
    """

    text = str(text)
    
    if not text:
        text += '\n'
    elif text[-1] != '\n':
        text += '\n'
    
    try:
        with open(path, 'a', encoding=encoding) as f:
            f.write(text)
    except UnicodeEncodeError:
        try:
            with open(path, 'a', encoding='cp949') as f:
                f.write(text)
        except UnicodeEncodeError:
            with open(path, 'a', encoding='utf-8') as f:
                f.write(text)


def distinct(myList: list):
    """
    It takes a list as an argument, converts it to a dictionary, and then returns the list of keys
    
    :param myList: list
    :type myList: list
    :return: A list of unique values from the list passed in.
    """
    return list(dict.fromkeys(myList))


def ip_change2():
    """Change IP.
    USB Tethering is Needed.

    Returns:
        bool: True if success, False otherwise.
    """
    import requests
    import subprocess
    import sys
    import time
    
    result_flag = False
    
    
    for _ in range(1,6):
        try:
            old_ip = requests.get("http://ip.wkwk.kr/", timeout=_).text
        except Exception as e:
            try:
                old_ip = requests.get("http://sub.wkwk.kr/ip/", timeout=_).text
            except Exception as e:
                pass
            else:
                break
        else:
            break
        time.sleep(_)
    else:
        # import socket
        # if socket.gethostbyname(socket.gethostname()) == '127.0.0.1':
        #     print('네트워크가 연결되어있지 않습니다.')
        # else:
        #     print('인터넷 속도가 불안정합니다.')
        return result_flag
    
    subprocess.run(['c:\\adb\\adb', 'shell', 'am', 'start', '-a', 'android.intent.action.MAIN', '-n', 'com.mmaster.mmaster/com.mmaster.mmaster.MainActivity'])

    for cnt in range(2,7):
        print('인터넷 접속대기중 - {}/5회'.format(cnt), end='')
        time.sleep(cnt)
        try:
            cur_ip = requests.get("http://ip.wkwk.kr/", timeout=cnt).text
        except Exception as e:
            try:
                cur_ip = requests.get("http://sub.wkwk.kr/ip/", timeout=cnt).text
            except Exception as e:
                pass
            else:
                break
        else:
            break

    if old_ip == cur_ip:
        print('\n아이피가 변경되지 않았습니다.')
        return result_flag
    else:
        print(f'\n{old_ip} -> {cur_ip} 변경 완료.')
        result_flag = True
        return result_flag


def http_remove(link: str):
    """
    It takes a string, removes the http:// or https:// from the beginning of the string, and then
    removes any trailing slashes
    
    :param link: str = The link you want to remove the http(s):// from
    :type link: str
    :return: The link without the http:// or https://
    """
    import re
    link = re.sub(r"https?://", '', link).strip('/')
    return link


def http_append(link: str):
    '''url에 https 추가'''
    return link if link.startswith('http') else "http://" + link


def get_code_from_image(img_path: str):
    """
    > The function takes an image path as an argument and returns the text in the image
    
    :param img_path: The path to the image file
    :type img_path: str
    :return: The return value is the text of the captcha.
    """
    import sys
    import datetime
    from python_anticaptcha import AnticaptchaClient, ImageToTextTask, AnticaptchaException
    
    ret_val = 'Failed'

    API_KEY = 'b336be7de932b65c877403893a382713'
    
    sys.stdout.write(f'> 보안코드 분석중 (이미지 기반) - {datetime.datetime.now().strftime("%H:%M:%S")}\n')

    try:
        img = open(img_path, 'rb')
    except:
        return ret_val
    
    client = AnticaptchaClient(API_KEY)
    task = ImageToTextTask(img)
    
    try:
        job = client.createTask(task)
        job.join()
    except AnticaptchaException:
        pass
    else:
        ret_val = job.get_captcha_text()
    
    return ret_val


def sound_alert(__msg: str='> 계속하려면 엔터를 입력하세요.\n> '):
    """
    > It plays a bell sound in a loop until the user presses the Enter key
    
    :param __msg: str='> 계속하려면 엔터를 입력하세요.\n> ', defaults to > 계속하려면 엔터를 입력하세요.\n> 
    :type __msg: str (optional)
    """
    import time
    import winsound
    import threading
    import pkgutil

    _pkg = '.'.join(__name__.split('.')[:-1])

    bell_data = pkgutil.get_data(_pkg, 'Bell.wav')

    class AlertThread(threading.Thread):
        
        def __init__(self):
            threading.Thread.__init__(self)
            self.flag = threading.Event()
        
        def run(self):

            while not self.flag.is_set():
                winsound.PlaySound(bell_data, winsound.SND_MEMORY)
                time.sleep(1)
    
    alert = AlertThread()

    alert.start()
    input(__msg)
    alert.flag.set()
    alert.join()


def sep_check(__input, __sep_cnt:int, __sep:str='\t') :
    """
    It check the line divied by param separater count 
    return : dictionary
    result = {
        'success' : boolean
        'error_data' : [ { 'line_no' : 'error_idx', 'sep_cnt' : 'error_line_sep_cnt }, { 'line_no' : 'error_idx', 'sep_cnt' : 'error_line_sep_cnt }, ...]
    }
    
    :param __input: The path to the file you want to read to or text list to splitlines()
    :type __input: str or list
    :param __sep_cnt: The separater count in input file text line
    :param __sep: the separate character
    """

    assert isinstance(__input,str) or isinstance(__input,list), "잘못된 인풋입니다."
    
    __result = {
        'success' : True,
        'error_data' : [],
        'sep' : repr(__sep)
    }

    islist = isinstance(__input,list)
    if islist:
        for __input_idx, __read_line in enumerate(__input, start=1):
            line_sep_cnt = __read_line.count(f'{__sep}')
            if __sep_cnt != line_sep_cnt:
                __result['success'] = False
                __result['error_data'].append({'line_no': str(__input_idx), 'sep_cnt': f'{line_sep_cnt}'})
    else:
        try:
            __input_list = open(f'{__input}','r').read().splitlines()
        except UnicodeDecodeError:
            __input_list = open(f'{__input}','r', encoding='utf-8').read().splitlines()
        for __input_idx, __read_line in enumerate(__input_list, start=1):
            line_sep_cnt = __read_line.count(f'{__sep}')
            if __sep_cnt != line_sep_cnt:
                __result['success'] = False
                __result['error_data'].append({'line_no': str(__input_idx), 'sep_cnt': f'{line_sep_cnt}'})
    return __result


def wait_until(__timestr: str=None):
    import re
    import sys
    import time
    from dateutil.parser import parse, ParserError
    from datetime import datetime

    loading_char_lst = [
        "     ",
        "•    ",
        "••   ",
        "•••  ",
        " ••• ",
        "  •••",
        "   ••",
        "    •",
        "     ",
    ]
    max_idx = len(loading_char_lst)

    if not __timestr:

        while True:
            sys.stdout.write('언제까지 대기할까요?\n')
            sys.stdout.write('ex)20220916 16:08\n')
            sys.stdout.write('ex)16:08\n')
            sys.stdout.write('＊ 형식에 맞게 입력해주세요\n')
            __timestr: str = input("> ")
            if re.match(r'\d{8} \d\d:\d\d', __timestr) or re.match(r'\d\d:\d\d', __timestr):
                break

    try:
        target_time = parse(__timestr)
    except ParserError:
        input("알 수 없는 시간 형식입니다.")
        sys.exit()

    sys.stdout.write(f'{target_time}까지 대기합니다.\n')

    for _ in range(round((target_time - datetime.now()).total_seconds()) * 6):
        time.sleep(1/6)
        sys.stdout.write(f'{loading_char_lst[_ % max_idx]}\r')
    else:
        sys.stdout.write('대기 완료.\n')


def get_spreadsheet(__url: str):
    import subprocess
    try:
        import gspread
    except ImportError:
        subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'gspread'], stdout=subprocess.DEVNULL)
        import gspread
    try:
        from google.oauth2.service_account import Credentials
    except ImportError:
        subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'google'], stdout=subprocess.DEVNULL)
        from google.oauth2.service_account import Credentials

    service_account_info = {
        "type": "service_account",
        "project_id": "gspread-361304",
        "private_key_id": "fcf10e7f306bf140765fbd239123a1d7e2e80f87",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2iBmCwuI//TnK\nvM8B89l07DJoX6abUB9+T5ZuJMwaq8G6Hv/ROEIl6K08+Ifvl+dWzlmajBTq2C8x\nPwxCV9x5Fdkg0VPMRKfXn4jJ/kw2T2iorFOPGTeAjpYUgVflFqZ5WDqUwp6eIekA\nt8XDyGPfCAwtmCHGOYEsXrld1TJwCzcH3Ynn9fLiLc6GyDfnfptRaxn0GqKReStm\nlpraCaF57TsKfFJhzoinUs4OLzjtAnIEpTmafVrbE4ksda9ugBar9dLM7xTA7eST\nxzV28oYkYaDRselLQgCUwhqylI9eYr1tp3uyJa2jlVbg4ZLAY6903yYF2YNuTGek\nfbbl9lUJAgMBAAECggEACcTb9Ksgd8NCOg8D1ztpSoAvrHVeEdbmcJiq2OdAQzcp\nDaCGGXj01VmQGADHKbQMDhHKKuLPZcg/MlgI/G3+Xz6jmcWKQhb0kq43oHPrOUbj\nt49Ng42acldvQdawURL2wuzNadPGsHjpIwAy5ekOK0wfdrs7J4RBXRIOwq5b3jIs\nQ+JyCHbAPrn3BplWxprXGBMtOxxbdZVJiWhwjV30znuTPi+7V3Y/PhaTNDInM0te\n3FN8ZEU2NiZ5p5VH230Vws3d2pnVUBiEcJ3ZlT5wbrxLkS4+/iO+tqMrkC1ToiEA\nURcXCsAJgnSrTnO12B5fVIrG7tKqK00C5Mcw/mI9hwKBgQDoFIfLqWzXQRNJNCNN\nGMl/uoiX7YU9l+OjUA1kK9i9vEUC2G5jWrO74rWnsHCvlmNR3+VAHpKbL5+6X/Sg\nAG0oY88XnvBD3ptB+4Ox9Wz/pzB3j1Aqn5JrBVqp11NB7Glb+P0zjAvwPfnKF0U+\n4jIp/1EfllNjDRuC3FiauNqIXwKBgQDJWDksyfSaCyM5aYkLp8wVgE/txO0CcpPh\nchlmuDnaseo4I9LsDsMEzBJhnIXoFCAw19VX+5loGJcJuyyxOKbt2h1p8rd6XSKI\n0h7u01/QoWnGzWXtyrARwVXWIuY6sODvJvpWnJ/xZnhsoM9cKhVjhthBEq2ThK+M\nJ7bqy547lwKBgQCYreEEiEq1dfdlImrS7qqpYCM6qCUO91zn9ONKclodwL05+P7u\nWB6ETcqqLjaEHZDrrTtZqoNSmssfRr9df8pQVxFH/eUdEVbc2sWyDr8NlYUaMutP\njzk5NQWHVMROS2SpAC47ejfkbjFl1VdV3mOYI4LQIApt0JK3zZRw/YmvSwKBgFCp\nTmZ6FcrssVTbybJoq6Llf5/ip4y2eDX2LuTu4waRBiMtft9g3pH6a1a9jQu3nFnU\n7bxMqF2ClGeqm7H33zAklGoQeZ7E1wP3IbtN5PHA6I5jVPVZoQXL7WZXHuLeX46P\nj/TI1G6yPYZPOiNTHLR9nf8by3vwyR8d/fK8VgzLAoGAMpCOS1oNsLSF/onnSwS0\nWYFTUCUGi3TXCQkGaVXUVeWb8OIAAjcGpqaVEsPCa6/s9pE5/fySC6PSXxHJ++oO\ntGBxZ2WXWyZy9RGYLsQ6bpS3dJS4oD6LOcwuEr9DVuAOiBThhzdkFlQG56gx3gUi\nOfWMoYdmWkQfjvPuzva1XsM=\n-----END PRIVATE KEY-----\n",
        "client_email": "gspread@gspread-361304.iam.gserviceaccount.com",
        "client_id": "101884032187465764375",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gspread%40gspread-361304.iam.gserviceaccount.com"
        }

    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    cred = Credentials.from_service_account_info(service_account_info, scopes=scopes)

    return gspread.authorize(cred).open_by_url(__url)


def get_time_now(__format: str, __delta=False):
    '''
    The function is return current time according to delta value
    If delta value is True, return datetime object current time ( '%Y-%m-%d %H:%M:%S' )
    If delta value is False, return string current time according to format type and format type is not correct, return error
    :param  format:set format type
    :type   format:string
    :param  delta:set return type ( datetime object / string )
    :type   delta:Boolean ( default=False )
    '''
    import datetime
    import re

    __now = datetime.datetime.now()
    __format_list = ['%Y','%y','%m','%B','%b','%d','%j','%H','%I','%p','%M','%S','%f','%w','%A','%a','%W','%U','%c','%_x','%X']

    if __delta == True:
        __datetime_format = '%Y-%m-%d %H:%M:%S'
        __now_str =__now.strftime(__datetime_format)
        __result =__now.strptime(__now_str,__datetime_format)
    else:
        __param_format_list = re.findall('%[a-zA-Z]+', __format)
        for __x in __param_format_list:
            if __x in __format_list:
                pass
            else:
                raise Exception(f'format 형식에 문제가 있습니다.\ninput_error_format : {__x}')

        __result =__now.strftime(__format)

    return __result


def err_logging(input_data, program_title=None, path='./error.txt', msg_flag = False):
    '''
    Write error_log in 'error.txt'
    If raise error, Send telegram message
    '''
    import sys
    import os
    import re
    from datetime import datetime
    import requests
    try:
        import telegram as tel
    except:
        os.system('pip install python-telegram-bot==13.15')
    # Send result message
    telegram_send_message = ''
    error_str = ''

    if '__title__' in globals():
        telegram_send_message += f'프로그램명 : {__title__}\n'
    else:
        if program_title == None:
            pwd = os.getcwd()
            program_title = pwd.split('\\')[-1]
            telegram_send_message += f'프로그램명 : {program_title}\n'
        else:
            telegram_send_message += f'프로그램명 : {program_title}\n'

    try:
        ip_check = requests.get('http://sub.wkwk.kr/ip/')
        ip_address = ip_check.text
        ip_check.close()
    except:
        ip_address = 'None("http://sub.wkwk.kr/ip/"와 연결이 되지 않아 ip를 확인 할 수 없습니다.)'
    telegram_send_message += f'IP : {ip_address}\n'

    # Get now datetime
    now = datetime.now().strftime('%y-%m-%d %H:%M:%S')
    error_str += f'------------------------{now}------------------------\n'
    if not isinstance(input_data,(list,dict)):
        raise Exception('Input_data type error : "input_data" is not list and not dict')

    # if input_data is list
    if isinstance(input_data,list):
        for data_dict in input_data:
            for data_key, data_value in data_dict.items():
                error_str += f'{data_key} : {data_value}\n'
                telegram_send_message += f'{data_key} : {data_value}\n'
    # if input_data is dict
    elif isinstance(input_data,dict):
        for data_key, data_value in input_data.items():
            error_str += f'{data_key} : {data_value}\n'
            telegram_send_message += f'{data_key} : {data_value}\n'

    # Get error script
    error_flag = sys.exc_info()
    if isinstance(error_flag,tuple):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        prob_file = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        prob_line_num = exc_tb.tb_lineno
        err_class = re.search("'.*'",str(exc_type).split(' ')[1]).group()
        err_script = str(exc_obj)
    else:
        prob_file = 'None'
        prob_line_num = 'None'
        err_class = 'It is not Error'
        err_script = 'It is not Error'

    error_str += f'Problem_File : {prob_file}\n'
    error_str += f'Problem_Line_Number : {prob_line_num}\n'
    error_str += f'Error_Class : {err_class}\n'
    error_str += f'Error_Script : {err_script}\n'

    telegram_send_message += f'Error_Class : {err_class}\n'
    telegram_send_message += f'Error_Script : {err_script}\n'
    telegram_send_message += f'Problem_Line_Number : {prob_line_num}\n'

    # Write error_log
    try:
        with open(path,'a',encoding='cp949') as err_f:
            err_f.write(error_str)
    except UnicodeEncodeError:
        with open(path,'a',encoding='utf-8') as err_f:
            err_f.write(error_str)
    
    # Send telegram
    bot_token = '5725160981:AAGem1A-euTFPOA1u87RbIjCRH-aS6hngic'
    chat_id = '-1001831517733'

    bot = tel.Bot(token=bot_token)
    
    if msg_flag:
        bot.send_message(chat_id, telegram_send_message)
