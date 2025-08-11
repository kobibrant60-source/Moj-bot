import requests
import hashlib
import time
from bs4 import BeautifulSoup

# Adres strony TTBS
URL = "https://www.ttbs.pl/3,aktualnosci"

# TWÓJ WEBHOOK Z DISCORDA
WEBHOOK_URL = "https://canary.discord.com/api/webhooks/1404527943937691698/Fj6E5Wc0VJSQ92NOw7BKgcVaL_uhfhZYBBy7n4NR_dpzO9WTh8DiBWglzsW6TZW917wT"  # <- Wklej tu swój link

# Co ile sekund sprawdzać stronę
INTERWAL = 60

def pobierz_hash_strony():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    tytuly = soup.select(".single-news__title")
    tekst = "".join(t.text.strip() for t in tytuly)
    return hashlib.md5(tekst.encode("utf-8")).hexdigest()

def wyslij_powiadomienie(tresc):
    payload = {"content": tresc}
    requests.post(WEBHOOK_URL, json=payload)

def monitoruj():
    ostatni_hash = pobierz_hash_strony()
    print("Bot uruchomiony. Oczekiwanie na zmiany...")
    while True:
        time.sleep(INTERWAL)
        nowy_hash = pobierz_hash_strony()
        if nowy_hash != ostatni_hash:
            wyslij_powiadomienie(f"📢 Nowy wpis lub zmiana na stronie TTBS!\n🔗 {URL}")
            ostatni_hash = nowy_hash

if __name__ == "__main__":
    # ✅ TEST – od razu wyślij powiadomienie po starcie
    wyslij_powiadomienie("✅ Bot został uruchomiony i działa na Render.com")

    monitoruj()
