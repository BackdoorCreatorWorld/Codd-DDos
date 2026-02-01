#!/usr/bin/env python3
"""
CLOUDFLARE BYPASS HANDLER
Cloudflare protection bypass and proxy management
"""

import requests
import random
import time
from colorama import Fore, Style

class CloudflareBypass:
    def __init__(self):
        self.proxies = []
        self.user_agents = []
        self.cf_cookies = {}
        
    def load_proxies(self, max_proxies=500):
        """Load proxy list from multiple sources"""
        print(f"{Fore.CYAN}[*] Loading proxy database...")
        
        proxy_list = []
        
        # Static proxy list (always available)
        static_proxies = [
            '45.77.56.114:8080',
            '138.197.157.32:8080',
            '165.227.36.191:8080',
            '167.71.41.76:8080',
            '45.76.44.175:8080',
            '45.32.140.23:8080',
            '209.97.150.167:8080',
            '51.158.68.26:8811',
            '51.158.68.133:8811',
            '188.166.83.17:3128',
            '159.203.61.169:8080',
            '167.99.123.158:8080'
        ]
        proxy_list.extend(static_proxies)
        
        # Try to fetch from online sources
        sources = [
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
            'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt'
        ]
        
        for source in sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    lines = response.text.strip().split('\n')
                    proxy_list.extend([line.strip() for line in lines if ':' in line])
                    print(f"{Fore.GREEN}[+] Added {len(lines)} proxies from {source.split('/')[-1]}")
            except Exception as e:
                continue
        
        # Remove duplicates
        self.proxies = list(set(proxy_list))[:max_proxies]
        print(f"{Fore.GREEN}[✓] Total proxies: {len(self.proxies)}")
        return self.proxies
    
    def detect_cloudflare(self, url):
        """Detect if website uses Cloudflare"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
            
            # Check headers for Cloudflare indicators
            cf_indicators = ['cloudflare', 'cf-ray', '__cfduid', 'cf-cache-status', '__cf_bm']
            
            for indicator in cf_indicators:
                if indicator in response.headers or indicator in response.text.lower():
                    return True
            
            # Check for Cloudflare challenge page
            if 'cf-chl-bypass' in response.text.lower() or 'jschl_vc' in response.text:
                return True
            
            return False
            
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Cloudflare detection failed: {str(e)}")
            return False
    
    def execute_bypass(self, url):
        """Execute Cloudflare bypass v2.5"""
        print(f"{Fore.CYAN}[*] Executing Cloudflare bypass v2.5...")
        
        bypass_methods = [
            self._method_header_manipulation,
            self._method_cookie_injection,
            self._method_js_challenge_solver,
            self._method_proxy_rotation
        ]
        
        # Try each method
        for method in bypass_methods:
            try:
                print(f"{Fore.YELLOW}[*] Trying {method.__name__}...")
                success = method(url)
                if success:
                    print(f"{Fore.GREEN}[✓] Bypass successful with {method.__name__}")
                    return True
            except Exception as e:
                continue
        
        print(f"{Fore.RED}[!] All bypass methods failed")
        return False
    
    def _method_header_manipulation(self, url):
        """Method 1: Advanced header manipulation"""
        try:
            # Generate stealth headers
            headers = self.generate_stealth_headers()
            
            # Add Cloudflare specific headers
            headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            })
            
            response = requests.get(url, headers=headers, timeout=10)
            
            # Check if bypass was successful
            if response.status_code == 200 and 'cf-browser-verification' not in response.text:
                # Store cookies for future use
                if 'set-cookie' in response.headers:
                    self.cf_cookies = response.cookies.get_dict()
                return True
            
            return False
            
        except Exception:
            return False
    
    def _method_cookie_injection(self, url):
        """Method 2: Cookie injection"""
        try:
            # Common Cloudflare cookie patterns
            cf_cookies = {
                '__cfduid': 'd8f8a9e9a7f8a7f8a7f8a7f8a7f8a7f8a' + str(random.randint(1000000000, 9999999999)),
                'cf_clearance': ''.join(random.choices('abcdef0123456789', k=40)),
                '__cf_bm': ''.join(random.choices('abcdef0123456789', k=60))
            }
            
            headers = self.generate_stealth_headers()
            response = requests.get(url, headers=headers, cookies=cf_cookies, timeout=10)
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def _method_js_challenge_solver(self, url):
        """Method 3: JavaScript challenge solver (simulated)"""
        print(f"{Fore.YELLOW}[*] Simulating JS challenge solving...")
        time.sleep(2)  # Simulate solving time
        
        # After "solving" challenge, make request with clearance
        headers = self.generate_stealth_headers()
        headers['Cookie'] = 'cf_clearance=simulated_clearance_' + ''.join(random.choices('0123456789abcdef', k=32))
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def _method_proxy_rotation(self, url):
        """Method 4: Proxy rotation bypass"""
        if not self.proxies:
            self.load_proxies()
        
        # Try multiple proxies
        tested_proxies = random.sample(self.proxies, min(10, len(self.proxies)))
        
        for proxy in tested_proxies:
            try:
                proxy_dict = {
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'
                }
                
                headers = self.generate_stealth_headers()
                response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=5)
                
                if response.status_code == 200:
                    print(f"{Fore.GREEN}[+] Working proxy found: {proxy}")
                    return True
                    
            except:
                continue
        
        return False
    
    def generate_stealth_headers(self):
        """Generate stealth headers for bypass"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        ]
        
        accept_languages = [
            'en-US,en;q=0.9',
            'en-GB,en;q=0.8',
            'en;q=0.7',
            'en-US,en;q=0.5'
        ]
        
        return {
            'User-Agent': random.choice(user_agents),
            'Accept': '*/*',
            'Accept-Language': random.choice(accept_languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': '1'
        }
    
    def get_random_proxy(self):
        """Get random proxy from list"""
        if not self.proxies:
            self.load_proxies()
        
        if self.proxies:
            return random.choice(self.proxies)
        return None
