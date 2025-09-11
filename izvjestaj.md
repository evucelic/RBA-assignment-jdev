# Izvještaj 
(korištena je umjetna inteligencija za formatiranje teksta, ali srž je pisana rukom)

## 1. Metodologija Testiranja (Selenium)

E2E testovi su automatizirani korištenjem **Selenium WebDrivera** kako bi se simulirala stvarna interakcija korisnika s grafičkim sučeljem (GUI) aplikacije.

**Proces testiranja:**
1.  **Autorizacija**: Test automatski unosi API ključ u odgovarajuće polje.
2.  **Slanje poruke**: Skripta pronalazi polje za unos teksta, upisuje poruku (rečenicu, ključnu riječ) i šalje je klikom na gumb.
3.  **Dohvaćanje odgovora**: Nakon slanja, skripta pronalazi posljednju poruku bota u sučelju kako bi analizirala njegov odgovor i prepoznatu namjeru.

Svi testni podaci i logika nalaze se u `tests/e2e/`. Iako je ova funkcionalnost ostvarena putem GUI testova, ista bi se provjera mogla postići i direktnim pozivima na REST API.

---

## 2. Pregled i Rezultati Testova

### Test 1: Provjera Dostupnosti (`/health` endpoint)

*   **Opis**: Jednostavan test koji provjerava je li server aktivan slanjem zahtjeva na `/health` endpoint i očekivanjem odgovora `ok`.
*   **Rezultat**: **PROŠAO** (dok god je server upaljen)
*   **Preporuka**: Trenutna provjera je skroz ok. Za produkcijska okruženja (npr. Docker), može se implementirati `HEALTHCHECK` mehanizam koji bi periodički provjeravao stanje kontejnera i automatski ga restartao u slučaju UNHEALTHY statusa.

### Test 2: Prepoznavanje Rečenica iz Trening Skupa

*   **Opis**: Ovaj test provjerava prepoznaje li bot ispravno namjeru za svaku rečenicu na kojoj je bio eksplicitno treniran.
*   **Rezultat**: **PROŠAO**. Kao što je i očekivano, model uspješno prepoznaje sve primjere koje je "vidio" tijekom treninga.

### Test 3: Prepoznavanje na Temelju Ključnih Riječi

*   **Opis**: S obzirom na to da korisnici često koriste kratke fraze, ovaj test procjenjuje uspješnost bota u prepoznavanju namjere na temelju pojedinačnih ključnih riječi.
*   **Zaključak**: Učinkovitost je mješovita.
    *   **Uspješno**: Ako je ključna riječ jedinstvena i bila je dio rečenica za treniranje.
    *   **Neuspješno**: Ako ključna riječ nije bila u trening skupu ili ako se pojavljuje u kontekstu više različitih namjera, model se muči s ispravnom klasifikacijom.

*   **Rezultati neuspjelih testova**:
    ```
    Keyword: 'gdje'          | Expected: 'adresa'        | Got: 'toaleti'
    Keyword: 'grad'          | Expected: 'adresa'        | Got: 'ulaznice'
    Keyword: 'izložba'       | Expected: 'danas_izlozbe' | Got: 'ulaznice'
    Keyword: 'pristupačnost' | Expected: 'pristupacnost' | Got: 'ulaznice'
    Keyword: 'garaža'        | Expected: 'parking'       | Got: 'ulaznice'
    ```

### Test 4: Provjera Dijakritičkih Znakova

*   **Opis**: Testira prepoznaje li bot riječi unesene bez hrvatskih dijakritičkih znakova (č, ć, š, đ, ž), s obzirom na to da je treniran isključivo na podacima s dijakriticima.
*   **Rezultat**: **SVI TESTOVI NEUSPJEŠNI**. Model ne uspijeva generalizirati i povezati riječi poput "kafic" s "kafić".
*   **Rezultati neuspjelih testova**:
    ```
    Keyword: 'kafic'       | Expected: 'kafic'         | Got: 'ulaznice'
    Keyword: 'clanstvo'    | Expected: 'clanstvo'      | Got: 'ulaznice'
    Keyword: 'izlozba'     | Expected: 'danas_izlozbe' | Got: 'ulaznice'
    ```

### Test 5: Prepoznavanje Rečenica izvan Trening Skupa (Out-of-Sample)

*   **Opis**: Ovaj test procjenjuje sposobnost generalizacije modela na potpuno novim rečenicama.
*   **Rezultat**: Djelomično uspješan. Uspjeh ovisi o količini preklapanja ključnih riječi između nove rečenice i rečenica iz trening skupa.
*   **Rezultati neuspjelih testova**:
    ```
    Sentence: 'Koji vam je raspored?'          | Expected: 'radno_vrijeme' | Got: 'danas_izlozbe'
    Sentence: 'Kakve su prednosti ako se učlanim?' | Expected: 'clanstvo'      | Got: 'danas_izlozbe'
    ```

---

## 3. Analiza Rada Bota i Preporuke za Poboljšanje

Glavni uzrok uočenih nedostataka leži u načinu na koji bot obrađuje tekst (vektorizacija).

### Problem: Vektorizacija na Riječima (`analyzer="word"`)

Model trenutno koristi `TfidfVectorizer` koji rečenice pretvara u vektore na temelju cijelih riječi i parova riječi (n-grami riječi).

```
pipe = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1,2),
        analyzer="word",  # <--- PROBLEM
        min_df=1,
        sublinear_tf=True,
    )),
    # ...
])
```

Ovaj pristup zahtijeva da korisnik unese gotovo identičnu riječ onoj iz trening skupa, što model čini neotpornim na:
*   Tipfelere
*   Riječi bez dijakritičkih znakova
*   Morfološke varijacije (npr. "ulaznica" vs. "ulaznice")

### Rješenje: Vektorizacija na Znakovima (`analyzer="char"`)

Rješenje koje sam testirao je promjena `analyzer` parametra u `char`. Ovim pristupom, model bi umjesto cijelih riječi analizirao nizove znakova (n-grame znakova).

**Primjer**: Za riječ `"jabuka"`, umjesto jednog tokena, generirali bi se tokeni poput `"jab"`, `"abu"`, `"buk"`, `"jabu"` itd.

*   **Prednosti**:
    *   Značajno poboljšana otpornost na tipfelere i nedostatak dijakritika.
    *   Bolje prepoznavanje riječi sa zajedničkim korijenom.
*   **Nedostaci**:
    *   Sporije treniranje i predikcija zbog većeg broja značajki.

### Dodatno Opažanje: Niska Pouzdanost (`Confidence`)

Uočeno je da model čak i za točne predikcije na trening primjerima vraća nisku razinu pouzdanosti (oko 30% u NAJBOLJEM slučaju). Mogući uzroci su sklearnova implementacija logističke regresije s opcijom 'multinomial' koja raspodjeljue vjerojatnosti na sve namjere, ili preklapanje riječi pošto puno rečenica sadrže iste riječi.
