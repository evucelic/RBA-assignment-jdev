inicijalna razmišljanja:

testovi:
jedan za health je dovoljan, iako je kodiran tako da uvijek vraća ok dok god server radi
prijedlog : moze se dodati health check u odredenim intervalima u dockerfile za robusniji tracking(starting, healthy, unhealthy)

test koji ce slati promptove s identicnim recenicama kao u train setu, ocekuje se tocna klasifikacija

test koji ce slati promptove s recenicama bez dijaktritickih znakova, asserta se tocna klasifikacija (iako mislim da će failati jer se u bot.py provjeravaju cijele rijeci a ne podnizovi, nije case insensitive, mozda na ovom prosirenom train setu nece failati iako sumnjam)

test za provjeru confidence odgovora koji su identični onima iz train seta, iz rucnog testiranja nije preveliki confidence, ne znam točno koji interval ciljam za točnu klasifikaciju, idealno blizu 1 ali sumnjam zbog malog dataseta i ne uzimanje u obzir case insensitive opcija.

test za provjeru confidence odgovora na prompt koji sadrži riječi koje se ne nalaze u niti jednom od train rečenica. očekujem confidence oko 1/10 

test za provjeru singularnih ključnih riječi jer ljudi ne upisuju cesto pune recenice.

jos neki test s recenicama koje nisu u train setu, izvaditi podatke i napraviti neki graf je li dobro klasificirano il ne, confidence itd

lagano poboljšanje -> umjesto word u botu koristiti 'char' opciju za analyzer koji gleda n-gramove odredene duljine, npr. djelove rijeci duljine od 3 do 6 umjesto cijelih rijeci kako bi bolje spojio korisnikovu poruku s namjerom, takoder dobro rjesenje za dijakriticke znakove