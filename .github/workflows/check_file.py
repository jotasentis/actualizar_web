import hashlib, os, smtplib, requests
from email.mime.text import MIMEText

URL = "https://URL-DE-LA-PAGINA-DEL-MINISTERIO"
HASH_FILE = "last_hash.txt"

def get_hash(url):
    r = requests.get(url, timeout=15)
    return hashlib.md5(r.text.encode()).hexdigest()

def send_email(old_hash, new_hash):
    msg = MIMEText(f"La página ha cambiado:\n{URL}\n\nHash anterior: {old_hash}\nHash nuevo: {new_hash}")
    msg["Subject"] = "⚠️ Cambio detectado en la página de oposiciones"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.environ["EMAIL_FROM"], os.environ["EMAIL_PASSWORD"])
        s.send_message(msg)

current = get_hash(URL)
previous = open(HASH_FILE).read().strip() if os.path.exists(HASH_FILE) else ""

if current != previous:
    if previous:  # No avisar en la primera ejecución
        send_email(previous, current)
    with open(HASH_FILE, "w") as f:
        f.write(current)
