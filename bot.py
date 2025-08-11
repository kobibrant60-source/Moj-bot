import requests
import hashlib
import time
from bs4 import BeautifulSoup

URL = "https://www.ttbs.pl/3,aktualnosci"
WEBHOOK_URL = "https://canary.discord.com/api/webhooks/1404527943937691698/Fj6E5Wc0VJSQ92NOw7BKgcVaL_uhfhZYBBy7n4NR_dpzO9WTh8DiBWglzsW6TZW917wT"
INTERWAL = 60

def pobierz_hash_strony():
    try:
        res = requests.get(URL, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        tytuly = soup.select(".single-news__title")
        tekst = "".join(t.text.strip() for t in tytuly)
        return hashlib.md5(tekst.encode("utf-8")).hexdigest()
    except Exception as e:
        print(f"❌ Błąd podczas pobierania strony: {e}", flush=True)
        return None

def wyslij_powiadomienie(tresc):
    try:
        payload = {"content": tresc}
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code != 204:
            print(f"❌ Błąd wysyłania powiadomienia: {response.status_code} - {response.text}", flush=True)
    except Exception as e:
        print(f"❌ Błąd podczas wysyłania powiadomienia: {e}", flush=True)

def monitoruj():
    ostatni_hash = pobierz_hash_strony()
    if not ostatni_hash:
        print("❌ Nie udało się pobrać startowego hasha! Kończę działanie.", flush=True)
        return
    print(f"✅ Bot uruchomiony. Startowy hash: {ostatni_hash}", flush=True)
    wyslij_powiadomienie("✅ Bot został uruchomiony i działa.")
    while True:
        try:
            time.sleep(INTERWAL)
            nowy_hash = pobierz_hash_strony()
            if not nowy_hash:
                print("⚠️ Nie udało się pobrać hasha, pomijam iterację", flush=True)
                continue
            print(f"⏱ Sprawdzam stronę TTBS... Hash: {nowy_hash}", flush=True)
            if nowy_hash != ostatni_hash:
                print("🔄 Wykryto zmianę na stronie!", flush=True)
                wyslij_powiadomienie(f"📢 Nowy wpis lub zmiana na stronie TTBS!\n🔗 {URL}")
                ostatni_hash = nowy_hash
        except Exception as e:
            print(f"‼️ Błąd w monitorowaniu: {e}", flush=True)

if __name__ == "__main__":
    monitoruj()
