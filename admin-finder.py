#!/usr/bin/python
# -------------------------------------------------
# Advanced Subdomain & Directory Scanner
# Author: CyberSec Team
# Version: 2.0
# -------------------------------------------------
import os
import sys
import time
import concurrent.futures
import requests as req
from colorama import Fore, Style, init
from urllib.parse import urlparse

# Initialize colorama
init(autoreset=True)

# Configuration
MAX_WORKERS = 50
TIMEOUT = 15
RESULTS_FILE = "scan_results.txt"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}

# Color scheme
class Colors:
    HEADER = Fore.LIGHTMAGENTA_EX
    OK = Fore.LIGHTGREEN_EX
    FAIL = Fore.LIGHTRED_EX
    INFO = Fore.LIGHTCYAN_EX
    WARNING = Fore.LIGHTYELLOW_EX
    RESET = Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear_screen()
    banner = f"""
{Colors.HEADER}███████╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗
{Colors.HEADER}██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝
{Colors.HEADER}███████╗██████╔╝██████╔╝██║   ██║██████╔╝█████╗  
{Colors.HEADER}╚════██║██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝  
{Colors.HEADER}███████║██║     ██║  ██║╚██████╔╝██║  ██║███████╗
{Colors.HEADER}╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
{Colors.INFO}Version 2.0 | Advanced Subdomain & Directory Scanner
{Colors.INFO}Developed by CyberSec Team
    """
    print(banner)

def validate_url(url):
    """Validate and format target URL"""
    if not url.startswith(('http://', 'https://')):
        url = f"http://{url}"
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def check_connection(url):
    """Check if target is reachable"""
    try:
        response = req.get(url, headers=HEADERS, timeout=TIMEOUT)
        return response.status_code == 200
    except req.exceptions.RequestException:
        return False

def load_wordlist(filename):
    """Load wordlist from file"""
    if not os.path.exists(filename):
        print(f"{Colors.FAIL}[!] Wordlist file '{filename}' not found!{Colors.RESET}")
        sys.exit(1)
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_result(url):
    """Save found URL to results file"""
    with open(RESULTS_FILE, 'a') as f:
        f.write(f"{url}\n")

def scan_subdomain(subdomain, domain):
    """Subdomain scanning worker"""
    try:
        url = f"http://{subdomain}.{domain}"
        response = req.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 200:
            result = f"[{Colors.OK}FOUND{Colors.RESET}] {url}"
            print(result)
            save_result(url)
        else:
            print(f"[{Colors.FAIL}404{Colors.RESET}] {url}")
    except req.exceptions.RequestException:
        pass
    except KeyboardInterrupt:
        raise

def scan_directory(directory, domain):
    """Directory scanning worker"""
    try:
        url = f"{domain}/{directory}"
        response = req.get(url, headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 200:
            result = f"[{Colors.OK}FOUND{Colors.RESET}] {url}"
            print(result)
            save_result(url)
        else:
            print(f"[{Colors.FAIL}404{Colors.RESET}] {url}")
    except req.exceptions.RequestException:
        pass
    except KeyboardInterrupt:
        raise

def progress_indicator(total, current):
    """Display scan progress"""
    progress = (current / total) * 100
    print(f"\r{Colors.INFO}[Progress]{Colors.RESET} {progress:.2f}% complete", end='')

def main():
    display_banner()
    
    # Input target URL
    target = input(f"{Colors.INFO}[?]{Colors.RESET} Enter target URL (e.g., example.com): ").strip()
    target = validate_url(target)
    domain = urlparse(target).netloc
    
    # Check target reachability
    print(f"\n{Colors.INFO}[*]{Colors.RESET} Checking target reachability...")
    if not check_connection(target):
        print(f"{Colors.FAIL}[!]{Colors.RESET} Target is unreachable: {target}")
        sys.exit(1)
    
    # Choose scan method
    print(f"\n{Colors.HEADER}Select Scan Method:")
    print(f"{Colors.INFO}1{Colors.RESET}) Subdomain Scan")
    print(f"{Colors.INFO}2{Colors.RESET}) Directory Scan")
    method = input(f"\n{Colors.INFO}[?]{Colors.RESET} Choose method (1/2): ").strip()
    
    if method not in ['1', '2']:
        print(f"{Colors.FAIL}[!]{Colors.RESET} Invalid selection. Exiting...")
        sys.exit(1)
    
    # Load wordlist
    wordlist = {
        '1': '.sub.txt',
        '2': '.dir.txt'
    }.get(method, '.sub.txt')
    
    wordlist_path = os.path.join(os.path.dirname(__file__), wordlist)
    wordlist_content = load_wordlist(wordlist_path)
    total = len(wordlist_content)
    
    # Confirmation
    print(f"\n{Colors.INFO}[*]{Colors.RESET} Starting scan with {total} entries")
    input(f"{Colors.WARNING}[!]{Colors.RESET} Press Enter to continue...")
    
    # Initialize results file
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)
    
    # Start scan
    print(f"\n{Colors.HEADER}Scan started at: {time.ctime()}{Colors.RESET}\n")
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for index, entry in enumerate(wordlist_content, 1):
            if method == '1':
                future = executor.submit(scan_subdomain, entry, domain)
            else:
                future = executor.submit(scan_directory, entry, target)
            futures.append(future)
            
            # Update progress
            if index % 10 == 0:
                progress_indicator(total, index)
        
        # Final progress update
        progress_indicator(total, total)
    
    elapsed_time = time.time() - start_time
    print(f"\n\n{Colors.INFO}[*]{Colors.RESET} Scan completed in {elapsed_time:.2f} seconds")
    print(f"{Colors.OK}[+] Results saved to: {RESULTS_FILE}{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.FAIL}[!] Scan interrupted by user{Colors.RESET}")
        sys.exit(1)
