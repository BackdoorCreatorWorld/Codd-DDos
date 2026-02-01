#!/usr/bin/env python3
"""
THREAD MANAGER
Thread management and control
"""

import threading
import time
import queue
from colorama import Fore, Style

class ThreadController:
    def __init__(self, max_threads=10000):
        self.max_threads = min(max_threads, 10000)
        self.active_threads = 0
        self.thread_pool = []
        self.task_queue = queue.Queue()
        self.lock = threading.Lock()
        self.running = False
        
    def execute_threads(self, target_func, num_threads, *args, **kwargs):
        """Execute specified number of threads with target function"""
        num_threads = min(num_threads, self.max_threads)
        
        print(f"{Fore.CYAN}[*] Starting {num_threads} threads...")
        
        self.running = True
        self.thread_pool = []
        
        # Create and start threads
        for i in range(num_threads):
            if not self.running:
                break
            
            # Create thread
            thread = threading.Thread(
                target=self._thread_wrapper,
                args=(target_func, i, *args),
                kwargs=kwargs,
                daemon=True
            )
            
            with self.lock:
                self.active_threads += 1
                self.thread_pool.append(thread)
            
            # Start thread with slight delay to avoid overwhelming
            thread.start()
            
            # Stagger thread creation for large numbers
            if i % 100 == 0 and i > 0:
                time.sleep(0.05)
        
        print(f"{Fore.GREEN}[✓] Started {len(self.thread_pool)} threads")
        return self.thread_pool
    
    def _thread_wrapper(self, target_func, thread_id, *args, **kwargs):
        """Wrapper for thread execution with error handling"""
        try:
            target_func(thread_id, *args, **kwargs)
        except Exception as e:
            # Silent error handling - don't spam console
            pass
        finally:
            with self.lock:
                self.active_threads -= 1
    
    def stop_all(self):
        """Stop all active threads"""
        print(f"{Fore.YELLOW}[*] Stopping threads...")
        self.running = False
        
        # Wait for threads to finish
        timeout = 10
        start_time = time.time()
        
        while self.active_threads > 0:
            if time.time() - start_time > timeout:
                print(f"{Fore.RED}[!] Timeout waiting for threads")
                break
            time.sleep(0.1)
        
        print(f"{Fore.GREEN}[✓] Threads stopped. Active: {self.active_threads}")
    
    def add_task(self, task_func):
        """Add task to queue for worker threads"""
        self.task_queue.put(task_func)
    
    def start_workers(self, num_workers):
        """Start worker threads for task processing"""
        workers = []
        for i in range(num_workers):
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            workers.append(worker)
            worker.start()
        
        return workers
    
    def _worker_loop(self):
        """Worker thread processing loop"""
        while self.running:
            try:
                task = self.task_queue.get(timeout=1)
                if task:
                    try:
                        task()
                    except:
                        pass
                self.task_queue.task_done()
            except queue.Empty:
                continue
    
    def get_status(self):
        """Get current thread status"""
        with self.lock:
            return {
                'active': self.active_threads,
                'total': len(self.thread_pool),
                'running': self.running
            }
    
    def wait_completion(self, timeout=None):
        """Wait for all threads to complete"""
        start_time = time.time()
        
        while self.active_threads > 0:
            if timeout and (time.time() - start_time) > timeout:
                break
            time.sleep(0.1)
        
        return self.active_threads == 0
