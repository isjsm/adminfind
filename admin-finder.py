#!/usr/bin/python
# -------------------------------------------------
# import mudules                                  |
# -------------------------------------------------
import os
import time
import sys
import concurrent.futures

# ------------------------------------------------
# تثبيت المكتبات المطلوبة مع إعادة الاستيراد بعد التثبيت
# ------------------------------------------------
try:
    import requests as req
except ImportError:
    os.system('pip install requests')
    import requests as req

try:
    from colorama import Fore, init
    init()  # تفعيل الألوان
except ImportError:
    os.system('pip install colorama')
    from colorama import Fore, init
    init()

# إزالة استيراد مكتبة colored لتجنب التعارض
# (استخدم colorama فقط للألوان)

# ------------------------------------------------
os.system('clear')

class color:
    red = '\033[31m'
    green = '\033[32m'
    blue = '\033[36m'
    pink = '\033[35m'
    orang = '\033[34m'
    white = '\033[00m'

def banner():
    print(f'''
{color.red}██   ██▄   █▀▄▀█ ▄█    ▄       {color.white}█ ▄▄  ██      ▄   ▄███▄   █         {color.green}▄████  ▄█    ▄   ██▄   ▄███▄   █▄▄▄▄ 
{color.red}█ █  █  █  █ █ █ ██     █      {color.white}█   █ █ █      █  █▀   ▀  █         {color.green}█▀   ▀ ██     █  █  █  █▀   ▀  █  ▄▀ 
{color.red}█▄▄█ █   █ █ ▄ █ ██ ██   █     {color.white}█▀▀▀  █▄▄█ ██   █ ██▄▄    █         {color.green}█▀▀    ██ ██   █ █   █ ██▄▄    █▀▀▌  
{color.red}█  █ █  █  █   █ ▐█ █ █  █     {color.white}█     █  █ █ █  █ █▄   ▄▀ ███▄      {color.green}█      ▐█ █ █  █ █  █  █▄   ▄▀ █  █  
{color.red}   █ ███▀     █   ▐ █  █ █     {color.white} █       █ █  █ █ ▀███▀       ▀     {color.green} █      ▐ █  █ █ ███▀  ▀███▀     █   
{color.red}  █          ▀      █   ██     {color.white}  ▀     █  █   ██                   {color.green}  ▀       █   ██                ▀    
{color.red} ▀                             {color.white}       ▀                                        {color.green}
''')

banner()

# استخدام colorama لتنسيق الألوان
print(Fore.WHITE + '[' + Fore.RED + '#' + Fore.WHITE + '] Enter target url example: google.com (without http or https or www !)')
target_url = input('TARGET [URL] ' + Fore.RED + '>_ ' + Fore.GREEN)

print(Fore.RESET)

# التحقق من صحة الـ URL
if 'http://' in target_url or 'https://' in target_url:
    pass
else:
    target_url = 'http://' + target_url

try:
    test = req.get(target_url, timeout=10)
    if test.status_code != 200:
        print(Fore.RED + 'Cant connect to target ' + Fore.WHITE + '> ' + Fore.YELLOW + target_url)
        sys.exit()
except req.exceptions.RequestException:
    print(Fore.RED + 'Cant connect to target ' + Fore.WHITE + '> ' + Fore.YELLOW + target_url)
    sys.exit()

# إزالة http/https من الـ URL لاستخدامه في البحث
target_url = target_url.replace('http://', '').replace('https://', '')

print(f'''
methods:
    method 1 :
        the subdomains searcher for find subdomains from {target_url}
        example test with sub_manual:
        target > {target_url}
        example[1] > admin.{target_url}
        example[2] > cpanel.{target_url}
    
    method 2 :
        the manual list search admin panels with [patch(dirs)]
        example search with manual list:
        target > {target_url}
        example[1] > {target_url}/admin
        example[2] > {target_url}/cpanel
''')

select_method = input('Select [method]: 1[subdomain[finder]] —— 2[patch-dirs[finder]] ' + Fore.RED + '>_ ' + Fore.WHITE)

def sub_manual():
    print('[' + Fore.GREEN + '*' + Fore.WHITE + '] TARGET >>> ' + Fore.GREEN + target_url)
    links = open('.sub.txt', 'r').read().split()

    def check_link(link):
        try:
            url = f'http://{link}.{target_url}'
            get_req = req.get(url, timeout=20)
            if get_req.status_code == 200:
                print(f'[' + Fore.GREEN + 'OK' + Fore.WHITE + f'] Founded a page - URL > {url}')
            else:
                print(f'[' + Fore.RED + 'NOT' + Fore.WHITE + f'] Cant found page - URL > {url}')
        except req.exceptions.RequestException:
            print(f'[' + Fore.RED + 'NOT' + Fore.WHITE + f'] Cant found page - URL > {url}')
        except KeyboardInterrupt:
            print('\nBye !')
            sys.exit()

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_link, links)

def manual_list():
    print('[' + Fore.GREEN + '*' + Fore.WHITE + '] TARGET >>> ' + Fore.GREEN + target_url)
    links = open('.link.txt', 'r').read().split()

    def check_link(link):
        try:
            url = f'http://{target_url}/{link}'
            get_req = req.get(url, timeout=20)
            if get_req.status_code == 200:
                print(f'[' + Fore.GREEN + 'OK' + Fore.WHITE + f'] Founded a page - URL > {url}')
            else:
                print(f'[' + Fore.RED + 'NOT' + Fore.WHITE + f'] Cant found page - URL > {url}')
        except req.exceptions.RequestException:
            print(f'[' + Fore.RED + 'NOT' + Fore.WHITE + f'] Cant found page - URL > {url}')
        except KeyboardInterrupt:
            print('\nBye !')
            sys.exit()

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_link, links)

if select_method == '1':
    sub_manual()
elif select_method == '2':
    manual_list()
else:
    print(Fore.RED + '[ERROR]' + Fore.WHITE + ' Please enter valid method (1) or (2) ! \n Enter to exit.')
    input()
    sys.exit(1)
