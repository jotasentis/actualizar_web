import hashlib, os, smtplib, requests
from email.mime.text import MIMEText

URL = "https://www.transportes.gob.es/informacion-para-el-ciudadano/empleo-publico/procesos-selectivos/convocatorias-2025/personal-funcionario/cterc-tl-oep-2025"
HASH_FILE = "last_hash.txt"

def get_hash(url):
    r = requests.get(url, timeout=15)
    return hashlib.md5(r.text.encode()).hexdigest()

def send_email(old_hash, new_hash):
    msg = MIMEText(f"La página ha cambiado:\n{URL}\n\nHash anterior: {old_hash}\nHash nuevo: {new_hash}")
    msg["Subject"] = "⚠️ Cambio detectado en la página de oposiciones"
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]          # ← aquí los destinatarios
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.environ["EMAIL_FROM"], os.environ["EMAIL_PASSWORD"])
        s.sendmail(                              # ← aquí el envío real
            os.environ["EMAIL_FROM"],
            os.environ["EMAIL_TO"].split(","),   # ← esto separa los dos correos
            msg.as_string()
        )

current = get_hash(URL)
previous = open(HASH_FILE).read().strip() if os.path.exists(HASH_FILE) else ""

if current != previous:
    if previous:  # No avisar en la primera ejecución
        send_email(previous, current)
    with open(HASH_FILE, "w") as f:
        f.write(current)
