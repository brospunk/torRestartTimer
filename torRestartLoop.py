import os
import time
import requests

# Configura il proxy Tor
proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

def get_public_ip():
    try:
        response = requests.get("https://checkip.amazonaws.com", proxies=proxies, timeout=10)
        return response.text.strip()
    except requests.RequestException:
        return "Errore nel recupero dell'IP"

cont = 1  # Contatore dei riavvii

while True:
    try:
        seconds = int(input("Inserisci il tempo in secondi per riavviare Tor: "))
        print(f"Tor verrà riavviato ogni {seconds} secondi. Premi Ctrl+C per uscire.")

        while True:
            for remaining in range(seconds, 0, -1):
                days = remaining // 86400
                hours = (remaining % 86400) // 3600
                minutes = (remaining % 3600) // 60
                secs = remaining % 60

                print(f"\rProssimo riavvio tra {days}d {hours}h {minutes}m {secs}s", end="", flush=True)
                time.sleep(1)

            print("\nRiavvio di Tor in corso...")
            os.system("sudo systemctl restart tor")

            time.sleep(5)  # Attendi qualche secondo per la riconnessione
            new_ip = get_public_ip()
            print(f"[{cont}] - Tor è stato riavviato! Nuovo IP: {new_ip}")

            cont += 1  # Incrementa il contatore
            
    except ValueError:
        print("Errore: Inserisci un numero valido di secondi.")
    except KeyboardInterrupt:
        print("\nUscita dal programma.")
        break
