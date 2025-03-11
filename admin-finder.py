#!/usr/bin/python
# -------------------------------------------------
__AUTHOR__ = 'Moj'
__TELEGRAM_ID__ = '@iranLwner'
__INSTAGRAM_ID__ = '@MJi_Devil'
__GITHUB__ = 'https://github.com/C4ssif3r'
__COMMENT__ = '''plz get me Star ⭐ :)'''

# -------------------------------------------------
# Import modules |
# -------------------------------------------------
import os
import time
import sys
import concurrent.futures

# Ensure required modules are installed
try:
    import requests as req
except ImportError:
    print("[!] 'requests' module not found. Installing it now...")
    os.system('pip install requests')
    try:
        import requests as req  # Re-import after installation
    except ImportError:
        print("[!] Failed to install 'requests'. Exiting...")
        sys.exit(1)

try:
    from colorama import Fore, init
except ImportError:
    print("[!] 'colorama' module not found. Installing it now...")
    os.system('pip install colorama')
    try:
        from colorama import Fore, init  # Re-import after installation
    except ImportError:
        print("[!] Failed to install 'colorama'. Exiting...")
        sys.exit(1)

try:
    from colored import fg, bg, attr
except ImportError:
    print("[!] 'colored' module not found. Installing it now...")
    os.system('pip install colored')
    try:
        from colored import fg, bg, attr  # Re-import after installation
    except ImportError:
        print("[!] Failed to install 'colored'. Exiting...")
        sys.exit(1)

try:
    import pyuseragents as agent
except ImportError:
    print("[!] 'pyuseragents' module not found. Installing it now...")
    os.system('pip install pyuseragents')
    try:
        import pyuseragents as agent  # Re-import after installation
    except ImportError:
        print("[!] Failed to install 'pyuseragents'. Exiting...")
        sys.exit(1)

# Initialize colorama
init()

# Clear screen
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


{color.red}██ ██▄ █▀▄▀█ ▄█ ▄ {color.white}█ ▄▄ ██ ▄ ▄███▄ █ {color.green}▄████ ▄█ ▄ ██▄ ▄███▄ █▄▄▄▄
{color.red}█ █ █ █ █ █ █ ██ █ {color.white}█ █ █ █ █ █▀ ▀ █ {color.green}█▀ ▀ ██ █ █ █ █▀ ▀ █ ▄▀
{color.red}█▄▄█ █ █ █ ▄ █ ██ ██ █ {color.white}█▀▀▀ █▄▄█ ██ █ ██▄▄ █ {color.green}█▀▀ ██ ██ █ █ █ ██▄▄ █▀▀▌
{color.red}█ █ █ █ █ █ ▐█ █ █ █ {color.white}█ █ █ █ █ █ █▄ ▄▀ ███▄ {color.green}█ ▐█ █ █ █ █ █ █▄ ▄▀ █ █
{color.red} █ ███▀ █ ▐ █ █ █ {color.white} █ █ █ █ █ ▀███▀ ▀ {color.green} █ ▐ █ █ █ ███▀ ▀███▀ █
{color.red} █ ▀ █ ██ {color.white} ▀ █ █ ██ {color.green} ▀ █ ██ ▀
{color.red} ▀ {color.white} ▀ {color.green}

''')

banner()

print(Fore.WHITE + '[' + Fore.RED + '#' + Fore.WHITE + '] Enter target url example: google.com (without http or https or www !)')

target_url = input('TARGET [URL] ' + Fore.RED + '>_' + Fore.GREEN + ' ')

print(Fore.RESET + '')

# Ensure the URL starts with 'http://' or 'https://'
if 'http://' not in target_url and 'https://' not in target_url:
    target_url = 'http://' + target_url

# Test connection to the target URL
try:
    test = req.get(target_url, timeout=10)
    if test.status_code != 200:
        print(Fore.RED + 'Cannot connect to target ' + Fore.WHITE + '> ' + Fore.YELLOW + target_url)
        sys.exit()
except req.exceptions.RequestException as e:
    print(Fore.RED + 'Cannot connect to target ' + Fore.WHITE + '> ' + Fore.YELLOW + target_url)
    print(Fore.RED + 'Error: ' + str(e))
    sys.exit()

# Remove 'http://' or 'https://' for further processing
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

select_method = input('Select [method]: 1[subdomain[finder]] —— 2[patch-dirs[finder]] ' + Fore.RED + '>_' + Fore.WHITE + ' ')

def sub_manual():
    '''
    the sub_manual for find subdomains
    example test with sub_manual:
    target > test.com
    to > admin.test.com
    to2 > cpanel.test.com
    '''
    print('[' + Fore.GREEN + '*' + Fore.WHITE + '] TARGET >>> ' + Fore.GREEN + target_url)

    # Check if .sub.txt exists
    if not os.path.exists('.sub.txt'):
        print(Fore.RED + '[ERROR] .sub.txt file not found. Exiting...')
        sys.exit(1)

    links = open('.sub.txt', 'r').read().split()

    def headers():
        hd = agent.random()
        return hd

    headers1 = {
        'User-Agent': headers()
    }

    def check_link(link):
        try:
            url = f'http://{link}.{target_url}'
            get_req = req.get(url, timeout=20, headers=headers1)
            print(f'[' + Fore.GREEN + 'OK' + Fore.WHITE + '] Found a page - URL > %s%s {} %s'.format(url) % (fg('black'), bg('green'), attr('reset')))
        except Exception:
            print(f'[' + Fore.RED + 'NOT' + Fore.WHITE + '] Cannot find page - URL > %s%s {} %s'.format(url) % (fg('black'), bg('red'), attr('reset')))
        except KeyboardInterrupt:
            print('\nBye!')
            time.sleep(3)
            sys.exit()

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_link, links)

def manual_list():
    '''
    the manual_list search admin panels with [patch{dirs}]
    example search with manual_list:
    target > test.com
    to > test.com/admin
    to2 > test.com/cpanel
    '''
    print('[' + Fore.GREEN + '*' + Fore.WHITE + '] TARGET >>> ' + Fore.GREEN + target_url)

    # Check if .link.txt exists
    if not os.path.exists('.link.txt'):
        print(Fore.RED + '[ERROR] .link.txt file not found. Exiting...')
        sys.exit(1)

    links = open('.link.txt', 'r').read().split()

    def headers():
        hd = agent.random()
        return hd

    headers1 = {
        'User-Agent': headers()
    }

    def check_link(link):
        try:
            url = f'http://{target_url}/{link}'
            get_req = req.get(url, timeout=20, headers=headers1)
            sisad = 399
            charsad = 400
            charnono = 499

            if get_req.status_code < sisad:
                print(f'[' + Fore.GREEN + 'OK' + Fore.WHITE + '] Found a page - URL > %s%s {} %s'.format(url) % (fg('black'), bg('green'), attr('reset')))

            if get_req.status_code > charsad:
                print(f'[' + Fore.RED + 'NOT' + Fore.WHITE + '] Cannot find page - URL > %s%s {} %s'.format(url) % (fg('black'), bg('red'), attr('reset')))

            if get_req.status_code > charnono:
                print(f'[' + Fore.YELLOW + 'Server-ERROR' + Fore.WHITE + '] SERVER ERROR - URL > %s%s {} %s'.format(url) % (fg('white'), bg('yellow'), attr('reset')))
        except KeyboardInterrupt:
            print('\nBye!')
            time.sleep(3)
            sys.exit()

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_link, links)

if select_method == '1':
    sub_manual()
elif select_method == '2':
    manual_list()
else:
    print(Fore.RED + '[ERROR]' + Fore.WHITE + ' Please enter a valid method (1) or (2)! \n Press Enter to exit.')
    input('')
    sys.exit(1)
