## End-to-End (E2E) Testovi za Chatbot

1.  **Lokalno okruženje**: Testiranje bota na lokalno pokrenutom serveru. Ovo omogućuje testiranje na proširenom skupu podataka za treniranje.
2.  **Produkcijsko okruženje**: Testiranje bota koji je postavljen na Renderu. Ova verzija je trenirana na manjem skupu podataka.

### Predradnje

1.  **Kloniranje repozitorija**:
      ```
      git clone https://github.com/evucelic/RBA-assignment-jdev.git
      cd RBA-assignment-jdev
      git submodule update --init --recursive
      ```

2.  **Postavljanje virtualnog okruženja i instalacija paketa**:
    *   Preporučuje se korištenje virtualnog okruženja kako bi se izbjegli konflikti s drugim Python paketima.
      ```
      # Stvaranje virtualnog okruženja
      python -m venv .venv

      # Aktivacija okruženja (Linux/macOS)
      source .venv/bin/activate

      # Aktivacija okruženja (Windows)
      # .\.venv\Scripts\activate

      # Instalacija potrebnih paketa
      pip install -r requirements.txt
      ```

3.  **Konfiguracija okruženja (.env datoteka)**:
    *   U korijenu projekta stvorite datoteku naziva `.env`.
    *   Dodajte sljedeće varijable u datoteku:
      ```
      # API ključ potreban za rad bota
      API_KEY_RBA="vas_api_kljuc"

      # URL na kojem se bot nalazi
      # Za lokalno testiranje:
      BASE_URL="http://localhost:8000"
      # Za testiranje na Renderu:
      # BASE_URL="https://rba-chatbot-assignment.onrender.com/"
      ```

---

### Pokretanje Testova

#### Opcija 1: Testiranje u Lokalnom Okruženju

1.  **Ažuriranje skupa za treniranje (opcionalno, ali preporučeno)**:
    *   Kako bi lokalni bot prepoznavao sve testne primjere, prenesite podatke iz `tests/e2e/testdata.py` (varijabla `SENTENCES`) u `bot.py` datoteku unutar chatbot submodulea.

2.  **Pokretanje lokalnog servera**:
    *   Slijedite upute iz `README.md` datoteke unutar `rba-chatbot-assignment` repozitorija (submodulea) kako biste pokrenuli server. Uvjerite se da je server aktivan na `http://localhost:8000`.

3.  **Izvršavanje testova**:
    *   Pozicionirajte se u direktorij s testovima:
      ```
      cd tests/e2e
      ```
    *   Pokrenite Pytest:
      ```
      pytest
      ```

#### Opcija 2: Testiranje na Produkcijskom Okruženju (Render)

**Napomena**: Bot na Renderu je treniran na manjem skupu podataka, pa neki testovi (posebno oni s proširenim primjerima) mogu (i hoće) pasti.

1.  **Konfiguracija `.env` datoteke**:
    *   Provjerite je li u vašoj `.env` datoteci `BASE_URL` postavljen na `https://rba-chatbot-assignment.onrender.com/`.

2.  **Izvršavanje testova**:
    *   Pozicionirajte se u direktorij s testovima:
      ```
      cd tests/e2e
      ```
    *   Pokrenite Pytest:
      ```
      pytest
      ```
```
