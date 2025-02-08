# 🔐 AES Text Encryptor

**AES Text Encryptor** is a Python application that allows you to encrypt and decrypt text messages using the **AES (Advanced Encryption Standard)** algorithm. With encrypted storage in SQLite database, you can manage messages securely and efficiently! 🚀

### ✨ Main Features
- 🔑 **Message Encryption**: Encrypt text messages with a password using the AES algorithm
- 🔓 **Message Decryption**: Decrypt encrypted messages with the correct password
- 🗂️ **Database Storage**: Encrypted messages are stored in SQLite with metadata for reference
- 🕵️‍♂️ **Key Security**: Encryption keys are generated using PBKDF2 for additional security
- 📜 **Activity Logging**: Application activities are automatically recorded in log files for monitoring

### 📦 Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/rexzea/AES-Text-Encryptor.git
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # For Linux/MacOS
   myenv\Scripts\activate     # For Windows
   ```

**Special Access**
```bash
cd AES-Text-Encryptor
```

## 🚀 How to Use
### 1. Run the program:
```bash
python AES.py
```

### 2. Choose one of the menu options:
  - 1: Encrypt a new message
  - 2: Decrypt an encrypted message
  - 3: View list of saved messages
  - 4: Exit application

## 🛠️ Technologies Used
Python 3.10+
- Cryptography: For message encryption and decryption
- SQLite: As local database storage
- Logging: For recording application activities

## 📷 Review
### Usage Review
![Review](review.png)

### Message List
![Review](daftar-pesan.png)

### Error If Password Is Wrong
![Review](eror-password-salah.png)

### Cannot Decrypt Encryption Before Creating Encryption
![Review](tidak-bisa-mendeteksi-enkripsi.png)

## 🤝 Contributing
Your contributions are always welcome! You can help by:
- Adding new features
- Fixing bugs
- Improving documentation

## 📝 License
cr: Rexzea

## 📧 Contact
If you have any questions or suggestions, don't hesitate to contact me at:
- futzfary@gmail.com
- 08988610455
