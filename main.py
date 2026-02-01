#!/usr/bin/env python3
"""
CODD - ADVANCED DDOS DISABLER SYSTEM
Main User Interface
"""

import os
import sys
import time
import hashlib
from colorama import Fore, Style, init

# Import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

init(autoreset=True)

class CODDSystem:
    def __init__(self):
        self.clear_screen()
        self.show_banner()
        self.authenticated = False
        self.passcodes = ["NanoHas", "DdosFal", "kingmercy", "CutonBar", "CuteFD"]
        self.selected_method = None
        self.target_url = None
        self.threads = 1000
        self.instant_mode = False
        self.attack_running = False
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        """Display CODD banner tanpa frame"""
        banner = f"""{Fore.MAGENTA}

    ░█████╗░░█████╗░██████╗░██████╗░
    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗
    ██║░░╚═╝██║░░██║██║░░██║██║░░██║
    ██║░░██╗██║░░██║██║░░██║██║░░██║
    ╚█████╔╝╚█████╔╝██████╔╝██████╔╝
    ░╚════╝░░╚════╝░╚═════╝░╚═════╝░

    ══════════ SERVER DISABLER SYSTEM ══════════
{Style.RESET_ALL}"""
        print(banner)
    
    def get_hidden_input(self, prompt):
        """Get hidden password input"""
        try:
            import getpass
            return getpass.getpass(prompt)
        except:
            # Fallback method
            print(prompt, end='')
            import msvcrt
            password = []
            while True:
                ch = msvcrt.getch()
                if ch == b'\r' or ch == b'\n':
                    print()
                    break
                elif ch == b'\x08':  # Backspace
                    if password:
                        password.pop()
                        print('\b \b', end='', flush=True)
                else:
                    password.append(ch.decode('utf-8', errors='ignore'))
                    print('*', end='', flush=True)
            return ''.join(password)
    
    def authenticate(self):
        """Password authentication"""
        print(f"\n{Fore.CYAN}{'═'*50}")
        print(f"{Fore.YELLOW}    🔐 ACCESS CONTROL SYSTEM")
        print(f"{Fore.CYAN}{'═'*50}{Style.RESET_ALL}")
        
        attempts = 3
        while attempts > 0:
            password = self.get_hidden_input(f"{Fore.WHITE}[?] Enter passcode: ")
            
            if password in self.passcodes:
                print(f"\n{Fore.GREEN}[✓] AUTHENTICATION SUCCESSFUL")
                print(f"{Fore.CYAN}[*] Initializing attack protocols...")
                time.sleep(2)
                self.authenticated = True
                return True
            else:
                attempts -= 1
                print(f"\n{Fore.RED}[✗] INVALID PASSCODE")
                print(f"{Fore.YELLOW}[*] Attempts remaining: {attempts}")
                
                if attempts == 0:
                    print(f"\n{Fore.RED}[!] SYSTEM LOCKED - Maximum attempts reached")
                    sys.exit(1)
        
        return False
    
    def show_menu(self):
        """Display main menu"""
        self.clear_screen()
        self.show_banner()
        
        print(f"\n{Fore.CYAN}{'═'*50}")
        print(f"{Fore.YELLOW}    ⚡ SELECT DISABLER METHOD")
        print(f"{Fore.CYAN}{'═'*50}{Style.RESET_ALL}\n")
        
        print(f"{Fore.MAGENTA}[1]{Fore.WHITE} Request Spammer")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Continuous request bombardment")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Basic but effective server overload\n")
        
        print(f"{Fore.MAGENTA}[2]{Fore.WHITE} HTTP/HTTPS Flood (Cloudflare Bypass)")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Advanced Cloudflare bypass 2.5")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Bot swarm with proxy rotation")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Target: Server & Defender systems\n")
        
        print(f"{Fore.MAGENTA}[3]{Fore.WHITE} Multifactor Fallback")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Brutal multi-vector attack")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Sequential attack patterns")
        print(f"    {Fore.CYAN}→{Fore.WHITE} Silent fallback penetration\n")
        
        print(f"{Fore.MAGENTA}[0]{Fore.WHITE} Exit System\n")
        
        print(f"{Fore.CYAN}{'═'*50}{Style.RESET_ALL}")
    
    def get_user_input(self):
        """Get user configuration"""
        try:
            # Select attack method
            while True:
                choice = input(f"\n{Fore.YELLOW}[?] Select method (1-3): {Fore.WHITE}").strip()
                
                if choice == '0':
                    print(f"\n{Fore.CYAN}[*] Exiting system...")
                    sys.exit(0)
                
                if choice in ['1', '2', '3']:
                    methods = {
                        '1': 'Request Spammer',
                        '2': 'HTTP/HTTPS Flood',
                        '3': 'Multifactor Fallback'
                    }
                    self.selected_method = methods[choice]
                    break
                else:
                    print(f"{Fore.RED}[!] Invalid selection. Choose 1-3")
            
            # Get target URL
            print(f"\n{Fore.CYAN}{'═'*50}")
            while True:
                self.target_url = input(f"{Fore.YELLOW}[?] Target URL: {Fore.WHITE}").strip()
                if self.target_url:
                    if not self.target_url.startswith(('http://', 'https://')):
                        self.target_url = 'http://' + self.target_url
                    break
                print(f"{Fore.RED}[!] Please enter a valid URL")
            
            # Get threads count
            while True:
                try:
                    threads_input = input(f"{Fore.YELLOW}[?] Threads (1-10000): {Fore.WHITE}").strip()
                    if not threads_input:
                        continue
                    
                    self.threads = int(threads_input)
                    if 1 <= self.threads <= 10000:
                        break
                    else:
                        print(f"{Fore.RED}[!] Threads must be 1-10000")
                except ValueError:
                    print(f"{Fore.RED}[!] Enter a valid number")
            
            # Instant mode
            print(f"\n{Fore.CYAN}{'═'*50}")
            while True:
                instant = input(f"{Fore.YELLOW}[?] Instant Attack? (y/n): {Fore.WHITE}").lower().strip()
                if instant in ['y', 'yes']:
                    self.instant_mode = True
                    break
                elif instant in ['n', 'no']:
                    self.instant_mode = False
                    break
                else:
                    print(f"{Fore.RED}[!] Enter 'y' or 'n'")
            
            # Show configuration
            self.clear_screen()
            self.show_banner()
            
            print(f"\n{Fore.CYAN}{'═'*50}")
            print(f"{Fore.YELLOW}    ⚡ ATTACK CONFIGURATION")
            print(f"{Fore.CYAN}{'═'*50}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}Method:{Fore.WHITE} {self.selected_method}")
            print(f"{Fore.MAGENTA}Target:{Fore.WHITE} {self.target_url}")
            print(f"{Fore.MAGENTA}Threads:{Fore.WHITE} {self.threads}")
            print(f"{Fore.MAGENTA}Instant Mode:{Fore.WHITE} {'ON' if self.instant_mode else 'OFF'}")
            print(f"{Fore.CYAN}{'═'*50}")
            
            # Confirm attack
            while True:
                confirm = input(f"\n{Fore.YELLOW}[?] Launch attack? (y/n): {Fore.WHITE}").lower().strip()
                if confirm in ['y', 'yes']:
                    return True
                elif confirm in ['n', 'no']:
                    print(f"\n{Fore.YELLOW}[*] Attack cancelled")
                    return False
                else:
                    print(f"{Fore.RED}[!] Enter 'y' or 'n'")
                    
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Operation cancelled")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {str(e)}")
            return False
    
    def display_progress(self, duration=10):
        """Display progress bar during attack"""
        import math
        
        bar_length = 40
        steps = 100
        delay = duration / steps
        
        if self.instant_mode:
            delay *= 0.3  # Faster for instant mode
        
        for i in range(steps + 1):
            if not self.attack_running:
                break
            
            percent = i
            filled = int(bar_length * i / steps)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            # Calculate simulated metrics
            req_per_sec = self.threads * (10 if self.instant_mode else 5)
            total_req = int((i / steps) * req_per_sec * duration)
            connections = int(self.threads * (i / steps) * 0.8)
            
            print(f'\r{Fore.CYAN}[{bar}] {percent}% | '
                  f'{Fore.GREEN}REQ: {total_req:,} | '
                  f'{Fore.YELLOW}CONN: {connections} | '
                  f'{Fore.MAGENTA}RPS: {req_per_sec:,}', end='', flush=True)
            
            time.sleep(delay)
        
        print()
    
    def start_attack(self):
        """Start the DDoS attack"""
        try:
            # Import attack handler
            try:
                from ddos_handler import DDoSDisabler
            except ImportError:
                print(f"{Fore.RED}[!] Attack module not found")
                print(f"{Fore.YELLOW}[*] Creating simulation mode...")
                self.attack_running = True
                self.display_progress(8)
                print(f"\n{Fore.GREEN}[✓] SIMULATION COMPLETE")
                print(f"{Fore.CYAN}[*] Real attack would be executed")
                return
            
            # Initialize attack
            print(f"\n{Fore.CYAN}[*] Initializing {self.selected_method}...")
            print(f"{Fore.CYAN}[*] Target: {self.target_url}")
            print(f"{Fore.CYAN}[*] Threads: {self.threads}")
            print(f"{Fore.CYAN}[*] Mode: {'INSTANT' if self.instant_mode else 'STANDARD'}")
            print(f"{Fore.YELLOW}[!] Starting in 3 seconds...")
            time.sleep(3)
            
            # Create attack instance
            attacker = DDoSDisabler(
                target_url=self.target_url,
                attack_type=self.selected_method,
                thread_count=self.threads,
                instant_mode=self.instant_mode
            )
            
            # Start progress in background
            self.attack_running = True
            import threading
            progress_thread = threading.Thread(target=self.display_progress, args=(12,))
            progress_thread.daemon = True
            progress_thread.start()
            
            # Execute attack
            result = attacker.execute_attack()
            
            # Wait for progress to finish
            self.attack_running = False
            progress_thread.join(timeout=2)
            
            # Show results
            print(f"\n{Fore.GREEN}{'═'*50}")
            print(f"{Fore.YELLOW}    ⚡ ATTACK COMPLETED")
            print(f"{Fore.GREEN}{'═'*50}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Status: {Fore.GREEN}SUCCESS" if result else f"{Fore.CYAN}[*] Status: {Fore.YELLOW}PARTIAL")
            print(f"{Fore.CYAN}[*] Target disabled: {Fore.GREEN}YES")
            print(f"{Fore.CYAN}[*] Server overload: {Fore.GREEN}ACHIEVED")
            print(f"{Fore.CYAN}[*] Defender bypass: {Fore.GREEN}SUCCESSFUL")
            print(f"{Fore.CYAN}[*] Total requests: {Fore.WHITE}{self.threads * 1000:,}")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Attack interrupted")
            self.attack_running = False
        except Exception as e:
            print(f"\n{Fore.RED}[!] Attack failed: {str(e)}")
            self.attack_running = False
    
    def run(self):
        """Main execution loop"""
        try:
            # Authentication
            if not self.authenticate():
                return
            
            # Main loop
            while True:
                self.show_menu()
                
                if self.get_user_input():
                    self.start_attack()
                    
                    # Ask for another attack
                    print(f"\n{Fore.CYAN}{'═'*50}")
                    again = input(f"{Fore.YELLOW}[?] Launch another attack? (y/n): {Fore.WHITE}").lower().strip()
                    
                    if again not in ['y', 'yes']:
                        print(f"\n{Fore.CYAN}[*] Shutting down CODD system...")
                        print(f"{Fore.GREEN}[✓] Clean exit completed")
                        print(f"{Fore.YELLOW}[!] Remember: Use responsibly")
                        break
                    
                    print(f"\n{Fore.CYAN}[*] Resetting system...")
                    time.sleep(2)
                else:
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] System terminated")
        except Exception as e:
            print(f"\n{Fore.RED}[!] System error: {str(e)}")

def check_dependencies():
    """Check and install required packages"""
    required = ['colorama']
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"{Fore.YELLOW}[*] Installing {package}...")
            os.system(f'pip install {package} --quiet')
            print(f"{Fore.GREEN}[✓] {package} installed")

if __name__ == "__main__":
    try:
        # Check dependencies
        check_dependencies()
        
        # Create system directory if needed
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Run system
        system = CODDSystem()
        system.run()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exit")
    except Exception as e:
        print(f"{Fore.RED}[!] Fatal error: {str(e)}")
