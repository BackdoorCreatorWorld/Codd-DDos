#!/usr/bin/env python3
"""
UTILITY FUNCTIONS
Helper functions for DDoS system
"""

import random
import string
import time
import hashlib
from colorama import Fore, Style

def generate_id(length=8):
    """Generate random ID"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def calculate_hash(data):
    """Calculate SHA256 hash"""
    return hashlib.sha256(str(data).encode()).hexdigest()

def format_number(num):
    """Format number with commas"""
    return f"{num:,}"

def print_status(message, level="info"):
    """Print status message with color coding"""
    colors = {
        "info": Fore.CYAN,
        "success": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
        "debug": Fore.MAGENTA
    }
    
    color = colors.get(level, Fore.WHITE)
    timestamp = time.strftime("%H:%M:%S")
    
    print(f"{Fore.WHITE}[{timestamp}] {color}{message}{Style.RESET_ALL}")

def validate_url(url):
    """Validate URL format"""
    from urllib.parse import urlparse
    
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def measure_time(func):
    """Decorator to measure execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{Fore.CYAN}[*] Execution time: {elapsed:.2f}s")
        return result
    return wrapper

def create_log_file(filename):
    """Create log file with timestamp"""
    import os
    from datetime import datetime
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/{filename}_{timestamp}.log"
    
    return log_file

def get_terminal_width():
    """Get terminal width for formatting"""
    import os
    try:
        return os.get_terminal_size().columns
    except:
        return 80
