import os
import sqlite3
import base64
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging
import hashlib

class SecureMessageManager:
    def __init__(self, db_path='secure_messages.db'):

        self.db_path = db_path
        self.backend = default_backend()
        self._setup_logging()
        self._create_database()
    
    def _setup_logging(self):

        # langsung otomatis buat direktori logs kalau belum ada
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.FileHandler('logs/encryption_log.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _create_database(self):

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS encrypted_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_hash TEXT UNIQUE,
                    encrypted_message TEXT,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                conn.commit()
            self.logger.info("Database berhasil diinisialisasi")
        except Exception as e:
            self.logger.error(f"Gagal membuat database: {e}")
    
    def generate_key(self, password, salt=None):

        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bit untuk enkripsinya
            salt=salt,
            iterations=100000,
            backend=self.backend 
        )
        
        key = kdf.derive(password.encode()) 
        return key, salt
    
    def encrypt_message(self, message, password, metadata=None):

        try:
            # membuat kunci passwordnya
            key, salt = self.generate_key(password)
            
            # IV
            iv = os.urandom(16)
            
            # cipher
            cipher = Cipher(
                algorithms.AES(key), 
                modes.CFB(iv), 
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            
            # enkripsi pesan
            encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()
            
            # menggabungkan salt, IV, dan pesan yg terenkripsi
            encrypted_data = salt + iv + encrypted_message
            
            # encode ke base64
            encrypted_text = base64.b64encode(encrypted_data).decode()
            
            # membuat hash 
            message_hash = hashlib.sha256(message.encode()).hexdigest()
            
            # menyimoan ke database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                INSERT INTO encrypted_messages 
                (message_hash, encrypted_message, metadata) 
                VALUES (?, ?, ?)
                ''', (message_hash, encrypted_text, metadata or ''))
                conn.commit()
            
            self.logger.info(f"Pesan berhasil dienkripsi dan disimpan (Hash: {message_hash})")
            
            return {
                'encrypted_text': encrypted_text,
                'message_hash': message_hash
            }
        
        except Exception as e:
            self.logger.error(f"Gagal mengenkripsi pesan: {e}")
            raise
    
    def decrypt_message(self, encrypted_message, password):

        try:
            # decode dari base64
            encrypted_data = base64.b64decode(encrypted_message.encode())
            
            # mengekstrak salt dan IV
            salt = encrypted_data[:16]
            iv = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]
            
            # menghasilkn kunci dengan salt yang sama
            key, _ = self.generate_key(password, salt)
            
            # cipher buat dekripsinya
            cipher = Cipher(
                algorithms.AES(key), 
                modes.CFB(iv), 
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            # dekripsi pesan
            decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
            
            self.logger.info("Pesan berhasil didekripsi")
            return decrypted_message.decode()
        
        except Exception as e:
            self.logger.error(f"Gagal mendekripsi pesan: {e}")
            raise
    
    def get_message_by_hash(self, message_hash):

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT encrypted_message, metadata FROM encrypted_messages WHERE message_hash = ?', 
                    (message_hash,)
                )
                result = cursor.fetchone()
                
                if result:
                    return {
                        'encrypted_message': result[0],
                        'metadata': result[1]
                    }
                return None
        except Exception as e:
            self.logger.error(f"Gagal mengambil pesan: {e}")
            return None
    
    def list_messages(self):

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT message_hash, created_at, metadata FROM encrypted_messages')
                return cursor.fetchall()
        except Exception as e:
            self.logger.error(f"Gagal mengambil daftar pesan: {e}")
            return []

def main():
    # contoh penggunaanya
    message_manager = SecureMessageManager()
    
    while True:
        print("\n--- Secure Message Manager ---")
        print("1. Enkripsi Pesan")
        print("2. Dekripsi Pesan")
        print("3. Lihat Daftar Pesan")
        print("4. Keluar")
        
        pilihan = input("Pilih menu (1-4): ")
        
        try:
            if pilihan == '1':
                message = input("Masukkan pesan: ")
                password = input("Masukkan password enkripsi: ")
                metadata = input("Masukkan metadata (opsional): ")
                
                result = message_manager.encrypt_message(message, password, metadata)
                print(f"\nPesan Terenkripsi:")
                print(f"Hash: {result['message_hash']}")
                print(f"Encrypted Text: {result['encrypted_text']}")
            
            elif pilihan == '2':
                encrypted_msg = input("Masukkan pesan terenkripsi: ")
                password = input("Masukkan password dekripsi: ")
                
                decrypted_msg = message_manager.decrypt_message(encrypted_msg, password)
                print(f"\nPesan Terdekripsi: {decrypted_msg}")
            
            elif pilihan == '3':
                messages = message_manager.list_messages()
                print("\nDaftar Pesan Tersimpan:")
                for hash_msg, created_at, metadata in messages:
                    print(f"Hash: {hash_msg}")
                    print(f"Dibuat pada: {created_at}")
                    print(f"Metadata: {metadata}\n")
            
            elif pilihan == '4':
                break
            
            else:
                print("Pilihan tidak valid!")
        
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
