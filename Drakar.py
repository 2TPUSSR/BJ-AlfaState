import random
import json
import os
import sys

# Pliki i ustawienia
PLIK_ZAPISU = "save_drakar.json"

# Funkcje pomocnicze
def wyczysc():
    os.system('cls' if os.name == 'nt' else 'clear')

def pauza():
    input("\nNaciśnij Enter, aby kontynuować...")

def loguj(tekst):
    print("(log) {}".format(tekst))

# Dane gry (słowniki i listy)
POTWORY = [
    {"id": "p1", "nazwa": "Szczurek-Mutant", "hp": 25, "atak": 6, "obrona": 0, "exp": 8, "zloto": 5},
    {"id": "p2", "nazwa": "Szkielet", "hp": 18, "atak": 5, "obrona": 1, "exp": 10, "zloto": 6},
    {"id": "p3", "nazwa": "Goblin", "hp": 30, "atak": 7, "obrona": 1, "exp": 12, "zloto": 8},
    {"id": "p4", "nazwa": "Wilk", "hp": 28, "atak": 8, "obrona": 1, "exp": 13, "zloto": 9},
    {"id": "p5", "nazwa": "Pająk Jadowity", "hp": 16, "atak": 6, "obrona": 0, "exp": 9, "zloto": 5},
    {"id": "p6", "nazwa": "Bandyta", "hp": 36, "atak": 9, "obrona": 2, "exp": 18, "zloto": 12},
    {"id": "p7", "nazwa": "Strażnik Kamienny", "hp": 60, "atak": 12, "obrona": 4, "exp": 35, "zloto": 20},
    {"id": "p8", "nazwa": "Czarownik Cieni", "hp": 45, "atak": 14, "obrona": 2, "exp": 40, "zloto": 25},
    {"id": "p9", "nazwa": "Ognisty Imp", "hp": 22, "atak": 10, "obrona": 0, "exp": 15, "zloto": 10},
    {"id": "p10", "nazwa": "Troll", "hp": 80, "atak": 16, "obrona": 5, "exp": 60, "zloto": 40},
    {"id": "p11", "nazwa": "Zmora", "hp": 50, "atak": 11, "obrona": 3, "exp": 42, "zloto": 30},
    {"id": "p12", "nazwa": "Szkielet Arcy", "hp": 70, "atak": 13, "obrona": 4, "exp": 55, "zloto": 35},
    {"id": "p13", "nazwa": "Straszliwy Ptak", "hp": 34, "atak": 9, "obrona": 2, "exp": 20, "zloto": 12},
    {"id": "p14", "nazwa": "Mroczny Rycerz", "hp": 90, "atak": 18, "obrona": 6, "exp": 80, "zloto": 60},
    {"id": "p15", "nazwa": "Bandersnatch", "hp": 120, "atak": 22, "obrona": 8, "exp": 120, "zloto": 100},
    {"id": "p16", "nazwa": "Duch Mędrca", "hp": 40, "atak": 7, "obrona": 3, "exp": 30, "zloto": 18},
    {"id": "p17", "nazwa": "Karakon", "hp": 55, "atak": 12, "obrona": 3, "exp": 45, "zloto": 28},
    {"id": "p18", "nazwa": "Wodny Żmij", "hp": 48, "atak": 11, "obrona": 2, "exp": 38, "zloto": 22},
    {"id": "p19", "nazwa": "Kolekcjoner Kości", "hp": 66, "atak": 14, "obrona": 3, "exp": 52, "zloto": 32},
    {"id": "p20", "nazwa": "Stróż Grobowca", "hp": 78, "atak": 15, "obrona": 5, "exp": 58, "zloto": 36},
]

PRZEDMIOTY = {
    "Mikstura": {"cena": 8, "opis": "Przywraca 25 HP", "typ": "zuzywalny"},
    "Bomba": {"cena": 20, "opis": "Zadawaj jednorazowo duże obrażenia", "typ": "zuzywalny"},
    "Stalowy Miecz": {"cena": 40, "opis": "Zwiększa atak o 5", "typ": "ekwipunek"},
    "Skórzana Tarcza": {"cena": 35, "opis": "Zwiększa obronę o 3", "typ": "ekwipunek"},
    "Zioła": {"cena": 3, "opis": "Składnik do craftu", "typ": "material"},
    "Sztabka Żelaza": {"cena": 12, "opis": "Składnik do craftu", "typ": "material"},
    "Kawałek Skóry": {"cena": 7, "opis": "Składnik do craftu", "typ": "material"},
    "Eliksir Siły": {"cena": 60, "opis": "Tymczasowo zwiększa atak", "typ": "zuzywalny"},
    "Amulet Zdrowia": {"cena": 80, "opis": "Zwiększa max HP", "typ": "ekwipunek"},
    "Lina": {"cena": 10, "opis": "Pomocna przy eksploracji", "typ": "inne"},
    "Klucz Mrocznego Lochu": {"cena": 0, "opis": "Klucz do specjalnej komnaty", "typ": "quest"},
    "Złota Sfinksowa Moneta": {"cena": 0, "opis": "Cenny artefakt (quest)", "typ": "quest"},
    "Rękawica Mocy": {"cena": 45, "opis": "Zwiększa siłę uderzenia", "typ": "ekwipunek"},
    "Runa Ochrony": {"cena": 55, "opis": "Zmniejsza otrzymywane obrażenia", "typ": "ekwipunek"},
    "Kryształ Ognia": {"cena": 70, "opis": "Składnik magiczny", "typ": "material"},
    "Kryształ Wody": {"cena": 70, "opis": "Składnik magiczny", "typ": "material"},
    "Maska Cienia": {"cena": 90, "opis": "Zwiększa szansę uników", "typ": "ekwipunek"},
    "Stary Miecz": {"cena": 5, "opis": "Słaby miecz startowy", "typ": "ekwipunek"},
}

LOKACJE = [
    {"id": "wioska", "nazwa": "Wioska Khorinisu", "typ": "bezpieczna", "opis": "Mała wieś z karczmą i sklepikiem."},
    {"id": "wejscie", "nazwa": "Wejście do Lochu", "typ": "loch", "opis": "Ciemne wejście prowadzące niżej."},
    {"id": "ruiny", "nazwa": "Starożytne Ruiny", "typ": "loch", "opis": "Pozostałości po dawnej cywilizacji."},
    {"id": "las", "nazwa": "Mroczny Las", "typ": "dzicz", "opis": "Drzewa pełne dziwnych odgłosów."},
    {"id": "bagna", "nazwa": "Bagna Smierdaka", "typ": "dzicz", "opis": "Bagnista kraina pełna potworów."},
    {"id": "wieza", "nazwa": "Zrujnowana Wieża", "typ": "loch", "opis": "Wieża z tajemniczymi szeptami."},
    {"id": "krypta", "nazwa": "Krypta", "typ": "loch", "opis": "Miejsce spoczynku dawnych wojowników."},
    {"id": "jaskinia", "nazwa": "Jaskinia Kryształów", "typ": "loch", "opis": "Lśniące ściany z kryształów."},
    {"id": "rynek", "nazwa": "Rynek", "typ": "bezpieczna", "opis": "Miejsce wymiany i plotek."},
    {"id": "sciezka", "nazwa": "Górska Ścieżka", "typ": "dzicz", "opis": "Wietrzna ścieżka na urwisku."},
    {"id": "komnata", "nazwa": "Tajemna Komnata", "typ": "loch", "opis": "Ukryta sala z sekretami."},
    {"id": "plaza", "nazwa": "Opuszczona Plaża", "typ": "dzicz", "opis": "Piasek i wraki statków."},
    {"id": "kopalnia", "nazwa": "Opuszczona Kopalnia", "typ": "loch", "opis": "Stare szyby i ruiny maszyn."},
    {"id": "kaplice", "nazwa": "Kaplice Duchów", "typ": "loch", "opis": "Miejsce kultu i potęgi."},
    {"id": "oaza", "nazwa": "Oaza", "typ": "bezpieczna", "opis": "Spokojne miejsce odpoczynku."},
    {"id": "rowniny", "nazwa": "Zamrożone Równiny", "typ": "dzicz", "opis": "Chłodne powietrze i biały świat."},
    {"id": "jezioro", "nazwa": "Podziemne Jezioro", "typ": "loch", "opis": "Ciche wody, coś się porusza..."},
    {"id": "miasto", "nazwa": "Zrujnowane Miasto", "typ": "loch", "opis": "Miasto, które zatonęło w piachu."},
    {"id": "gaj", "nazwa": "Zaczarowana Gajówka", "typ": "dzicz", "opis": "Gaj pełen świateł i magii."},
    {"id": "komnata_koncowa", "nazwa": "Komnata Przeznaczenia", "typ": "loch", "opis": "Meble, artefakty i... boss?"}
]

PRZEPISY = {
    "Stalowy Miecz": {"Sztabka Żelaza": 2, "Kawałek Skóry": 1},
    "Skórzana Tarcza": {"Kawałek Skóry": 3},
    "Mikstura": {"Zioła": 3},
    "Eliksir Siły": {"Zioła": 2, "Kryształ Ognia": 1},
    "Amulet Zdrowia": {"Kryształ Wody": 1, "Sztabka Żelaza": 1},
}

ZADANIA = [
    {"id": "z1", "nazwa": "Szczurza Plaga", "opis": "Zabij 3 Szczurki-Mutanty", "cel": "Szczurek-Mutant", "liczba": 3, "nagroda": {"zloto": 20, "exp": 30, "przedmioty": {"Zioła": 2}}},
    {"id": "z2", "nazwa": "Zaginiona Moneta", "opis": "Znajdź Złotą Sfinksową Monetę", "przedmiot_cel": "Złota Sfinksowa Moneta", "nagroda": {"zloto": 50, "exp": 50}},
    {"id": "z3", "nazwa": "Serwis Mieczy", "opis": "Przynieś 2 Sztabki Żelaza", "przedmioty_cel": {"Sztabka Żelaza": 2}, "nagroda": {"zloto": 30, "exp": 25}},
    {"id": "z4", "nazwa": "Strażnik Grobowca", "opis": "Pokonaj Stróża Grobowca", "cel": "Stróż Grobowca", "liczba": 1, "nagroda": {"zloto": 80, "exp": 100, "przedmioty": {"Klucz Mrocznego Lochu": 1}}},
]

# Funkcje tworzące gracza
def stworz_gracza(imie, klasa):
    bazowy = {
        "imie": imie,
        "klasa": klasa,
        "hp": 100,
        "max_hp": 100,
        "atak": 8,
        "obrona": 3,
        "zloto": 30,
        "exp": 0,
        "poziom": 1,
        "ekwipunek": {"Stary Miecz": 1, "Mikstura": 2, "Zioła": 1},
        "sprzet": {"bron": "Stary Miecz", "pancerz": None, "dodatki": None},
        "lokacja": "wioska",
        "zadania": {},
        "dziennik": [],
        "osiagniecia": []
    }
    if klasa == "Paladyn":
        bazowy["hp"] = 120
        bazowy["max_hp"] = 120
        bazowy["atak"] += 2
        bazowy["obrona"] += 2
    elif klasa == "Czarodziej":
        bazowy["hp"] = 80
        bazowy["max_hp"] = 80
        bazowy["atak"] += 4
        bazowy["obrona"] -= 1
    elif klasa == "Łucznik":
        bazowy["hp"] = 95
        bazowy["max_hp"] = 95
        bazowy["atak"] += 3
    return bazowy

def struktura_zapisu(gracz):
    return {"gracz": gracz, "meta": {"zapisano" "wersja": "1.0"}}

# Zapis i wczytywanie gry
def zapisz_gre(gracz):
    dane = struktura_zapisu(gracz)
    try:
        with open(PLIK_ZAPISU, "w", encoding="utf-8") as f:
            json.dump(dane, f, ensure_ascii=False, indent=2)
        gracz["dziennik"].append("Zapisano grę: {}")
        loguj("Zapisano grę dla {}".format(gracz["imie"]))
        print("Zapisano grę.")
    except Exception as e:
        print("Błąd zapisu:", e)
        loguj("Błąd zapisu: {}".format(e))

def wczytaj_gre():
    if not os.path.exists(PLIK_ZAPISU):
        print("Brak pliku zapisu.")
        return None
    try:
        with open(PLIK_ZAPISU, "r", encoding="utf-8") as f:
            dane = json.load(f)
        gracz = dane.get("gracz")
        if gracz:
            print("Wczytano zapis.")
            loguj("Wczytano grę dla {}".format(gracz.get("imie", "?")))
            return gracz
    except Exception as e:
        print("Błąd wczytu:", e)
        loguj("Błąd wczytu: {}".format(e))
    return None

# Mechanika walki
def oblicz_obrazenia(atak, obrona, wariancja=3):
    baza = atak + random.randint(0, wariancja)
    dmg = max(0, baza - obrona)
    return dmg

def losuj_potwora(utrudnienie=1):
    pula = []
    for p in POTWORY:
        waga = max(1, p["exp"] // 5)
        for _ in range(waga):
            pula.append(p)
    return random.choice(pula)

def atak_gracza(gracz, potwor):
    bron = gracz["sprzet"].get("bron")
    bonus = 0
    if bron and bron in PRZEDMIOTY and PRZEDMIOTY[bron]["typ"] == "ekwipunek":
        if "Miecz" in bron:
            bonus = 5
        if "Stary" in bron:
            bonus = 1
    baza = gracz["atak"] + bonus
    dmg = oblicz_obrazenia(baza, potwor.get("obrona", 0), 4)
    if random.random() < 0.08:
        dmg *= 2
        gracz["dziennik"].append("Krytyk: {} dmg".format(dmg))
    potwor["hp_aktualne"] -= dmg
    return dmg

def atak_potwora(gracz, potwor):
    dmg = oblicz_obrazenia(potwor.get("atak", 5), gracz.get("obrona", 0), 3)
    dodatki = gracz["sprzet"].get("dodatki")
    if dodatki in ("Runa Ochrony", "Amulet Zdrowia"):
        dmg = max(0, dmg - 2)
    gracz["hp"] -= dmg
    return dmg

def rozpocznij_walke(gracz, szablon):
    potwor = dict(szablon)
    potwor["hp_aktualne"] = potwor["hp"]
    loguj("{} napotkał {}".format(gracz["imie"], potwor["nazwa"]))
    gracz["dziennik"].append("Start walki z {}".format(potwor["nazwa"]))
    bomba = False

    while potwor["hp_aktualne"] > 0 and gracz["hp"] > 0:
        print("\n=== WALKA ===")
        print("Przeciwnik: {} (HP: {}/{})".format(potwor["nazwa"], potwor["hp_aktualne"], potwor["hp"]))
        print("Twoje HP: {}/{} | Złoto: {} | EXP: {}".format(gracz["hp"], gracz["max_hp"], gracz["zloto"], gracz["exp"]))
        print("1) Atak   2) Użyj przedmiotu   3) Ucieczka   4) Ekwipunek")
        wybor = input("> ").strip()
        if wybor == "1":
            dmg = atak_gracza(gracz, potwor)
            print("Zadałeś {} obrażeń.".format(dmg))
            gracz["dziennik"].append("Zadałeś {} {}".format(dmg, potwor["nazwa"]))
        elif wybor == "2":
            print("Przedmioty:", gracz["ekwipunek"])
            it = input("Co użyć? > ").strip()
            res = uzyj_przedmiotu(gracz, it)
            if res == "bomba":
                bomba = True
                print("Przygotowałeś bombę - następny atak zada dodatkowe obrażenia.")
            elif isinstance(res, int) and res > 0:
                print("Przedmiot zadał {} obrażeń.".format(res))
                potwor["hp_aktualne"] -= res
        elif wybor == "3":
            if random.random() < 0.5:
                print("Uciekłeś!")
                gracz["dziennik"].append("Ucieczka udana")
                return True
            else:
                print("Nie udało się uciec!")
        elif wybor == "4":
            pokaz_ekwipunek(gracz)
            pauza()
            continue
        else:
            print("Niepoprawny wybór.")
            continue

        if bomba and potwor["hp_aktualne"] > 0:
            extra = 25
            potwor["hp_aktualne"] -= extra
            print("Bomba eksploduje! +{} obrażeń.".format(extra))
            gracz["dziennik"].append("Bomba: {} dmg".format(extra))
            bomba = False

        if potwor["hp_aktualne"] > 0:
            otrzymane = atak_potwora(gracz, potwor)
            print("{} zadaje Ci {} obrażeń.".format(potwor["nazwa"], otrzymane))
            gracz["dziennik"].append("Otrzymałeś {} od {}".format(otrzymane, potwor["nazwa"]))
            if gracz["hp"] <= 0:
                print("Zostałeś pokonany...")
                gracz["dziennik"].append("Zginąłeś w walce")
                loguj("{} zginął od {}".format(gracz["imie"], potwor["nazwa"]))
                return False
        else:
            print("Pokonałeś {}!".format(potwor["nazwa"]))
            gracz["zloto"] += potwor.get("zloto", 0)
            gracz["exp"] += potwor.get("exp", 0)
            print("Otrzymujesz {} zł i {} EXP.".format(potwor.get("zloto",0), potwor.get("exp",0)))
            gracz["dziennik"].append("Pokonałeś {}".format(potwor["nazwa"]))
            loguj("{} pokonał {}".format(gracz["imie"], potwor["nazwa"]))
            sprawdz_zadanie_po_zabiciu(gracz, potwor["nazwa"])
            sprawdz_awans(gracz)
            return True
    return gracz["hp"] > 0

# Przedmioty / ekwipunek
def dodaj_przedmiot(gracz, nazwa, ilosc=1):
    gracz["ekwipunek"][nazwa] = gracz["ekwipunek"].get(nazwa, 0) + ilosc
    gracz["dziennik"].append("Otrzymano {}x {}".format(ilosc, nazwa))

def usun_przedmiot(gracz, nazwa, ilosc=1):
    ile = gracz["ekwipunek"].get(nazwa, 0)
    if ile >= ilosc:
        gracz["ekwipunek"][nazwa] = ile - ilosc
        if gracz["ekwipunek"][nazwa] <= 0:
            del gracz["ekwipunek"][nazwa]
        gracz["dziennik"].append("Zużyto {}x {}".format(ilosc, nazwa))
        return True
    return False

def uzyj_przedmiotu(gracz, nazwa):
    if nazwa not in gracz["ekwipunek"]:
        print("Nie masz tego przedmiotu.")
        return None
    typ = PRZEDMIOTY.get(nazwa, {}).get("typ")
    if typ == "zuzywalny":
        if nazwa == "Mikstura":
            if usun_przedmiot(gracz, "Mikstura", 1):
                ile = min(gracz["max_hp"] - gracz["hp"], 25)
                gracz["hp"] += ile
                print("Odzyskałeś {} HP.".format(ile))
                return None
        if nazwa == "Bomba":
            if usun_przedmiot(gracz, "Bomba", 1):
                return "bomba"
        if nazwa == "Eliksir Siły":
            if usun_przedmiot(gracz, "Eliksir Siły", 1):
                buff = 6
                gracz["atak"] += buff
                print("Atak +{} (na stałe w tej sesji).".format(buff))
                gracz["dziennik"].append("Użyto Eliksiru Siły")
                return None
    elif typ == "ekwipunek":
        slot = "bron"
        if "Tarcza" in nazwa or "Pancerz" in nazwa or "Skórzana" in nazwa:
            slot = "pancerz"
        if "Amulet" in nazwa or "Runa" in nazwa or "Maska" in nazwa or "Rękawica" in nazwa:
            slot = "dodatki"
        gracz["sprzet"][slot] = nazwa
        print("Wyposażyłeś {} w slot {}.".format(nazwa, slot))
        gracz["dziennik"].append("Wyposażono {}".format(nazwa))
        return None
    else:
        print("Nie możesz użyć tego przedmiotu w ten sposób.")
        return None

def pokaz_ekwipunek(gracz):
    print("\n--- EKWIPUNEK ---")
    for k,v in gracz["ekwipunek"].items():
        print("{}: {}".format(k, v))
    print("Sprzęt:", gracz["sprzet"])
    print("-----------------")

# Sklep
def menu_sklep(gracz):
    wyczysc()
    print("=== SKLEP ===")
    lista = list(PRZEDMIOTY.items())
    for i, (nazwa, info) in enumerate(lista, start=1):
        print("{}) {} - {} zł - {}".format(i, nazwa, info["cena"], info["opis"]))
    print("\nTwoje złoto: {}".format(gracz["zloto"]))
    print("Wpisz numer, aby kupić, 0 aby wyjść.")
    wybor = input("> ").strip()
    if not wybor.isdigit():
        print("Niepoprawny wybór.")
        return
    idx = int(wybor)
    if idx == 0:
        return
    if 1 <= idx <= len(lista):
        nazwa = lista[idx-1][0]
        cena = lista[idx-1][1]["cena"]
        if gracz["zloto"] >= cena:
            gracz["zloto"] -= cena
            dodaj_przedmiot(gracz, nazwa, 1)
            print("Kupiłeś {}.".format(nazwa))
            loguj("{} kupił {} za {} zł".format(gracz["imie"], nazwa, cena))
        else:
            print("Nie masz wystarczająco złota.")
    else:
        print("Nie ma takiego przedmiotu.")

# Eksploracja i lokacje
def opis_lokacji(id_l):
    loc = None
    for l in LOKACJE:
        if l["id"] == id_l:
            loc = l
            break
    if loc:
        print("\nJesteś w: {} - {}".format(loc["nazwa"], loc["opis"]))
    else:
        print("\nNieznana lokacja.")

def losowe_zdarzenie(gracz, id_l):
    loc = None
    for l in LOKACJE:
        if l["id"] == id_l:
            loc = l
            break
    if not loc:
        print("Nic tu nie ma.")
        return
    typ = loc["typ"]
    r = random.random()
    if typ == "bezpieczna":
        if r < 0.2:
            print("Spotykasz wędrownego kupca.")
            menu_sklep(gracz)
        elif r < 0.4:
            print("Spotykasz podróżnika - opowieść nic nie daje.")
        else:
            print("Dzień mija spokojnie.")
    elif typ == "dzicz":
        if r < 0.5:
            m = losuj_potwora(gracz.get("poziom",1))
            rozpocznij_walke(gracz, m)
        elif r < 0.7:
            zl = random.randint(5,25)
            gracz["zloto"] += zl
            print("Znalazłeś sakiewkę z {} zł.".format(zl))
            gracz["dziennik"].append("Znalazłeś {} zł w {}".format(zl, loc["nazwa"]))
        else:
            przed = random.choice(list(PRZEDMIOTY.keys()))
            dodaj_przedmiot(gracz, przed, 1)
            print("Znalazłeś przedmiot: {}".format(przed))
    elif typ == "loch":
        if r < 0.65:
            m = losuj_potwora(gracz.get("poziom",1)+1)
            rozpocznij_walke(gracz, m)
        elif r < 0.85:
            if random.random() < 0.12:
                dodaj_przedmiot(gracz, "Złota Sfinksowa Moneta", 1)
                print("Znalazłeś rzadki artefakt: Złota Sfinksowa Moneta!")
                gracz["dziennik"].append("Znalazłeś Złotą Sfinksową Monetę")
            else:
                zl = random.randint(10,40)
                gracz["zloto"] += zl
                print("Znalazłeś {} zł.".format(zl))
        else:
            dmg = random.randint(5,18)
            gracz["hp"] -= dmg
            print("Pułapka! Otrzymujesz {} obrażeń.".format(dmg))
            gracz["dziennik"].append("Pułapka: -{} HP".format(dmg))
    else:
        print("Nic się nie dzieje tutaj.")

# Zadania
def przyjmij_zadanie(gracz, id_z):
    q = None
    for zad in ZADANIA:
        if zad["id"] == id_z:
            q = zad
            break
    if not q:
        print("Brak takiego zadania.")
        return
    if id_z in gracz["zadania"]:
        print("Masz już to zadanie.")
        return
    prog = {"id": id_z, "postep": 0, "aktywne": True}
    gracz["zadania"][id_z] = prog
    gracz["dziennik"].append("Przyjęto zadanie: {}".format(q["nazwa"]))
    print("Przyjęto: {}".format(q["nazwa"]))

def sprawdz_zadanie_po_zabiciu(gracz, nazwa_potwora):
    for q in ZADANIA:
        if q.get("cel") == nazwa_potwora and q["id"] in gracz["zadania"]:
            prog = gracz["zadania"][q["id"]]
            prog["postep"] += 1
            gracz["dziennik"].append("Postęp {}: {}/{}".format(q["nazwa"], prog["postep"], q.get("liczba",1)))
            if prog["postep"] >= q.get("liczba",1):
                zakoncz_zadanie(gracz, q["id"])

def zakoncz_zadanie(gracz, id_z):
    q = None
    for zad in ZADANIA:
        if zad["id"] == id_z:
            q = zad
            break
    if not q or id_z not in gracz["zadania"]:
        return
    rew = q.get("nagroda", {})
    zl = rew.get("zloto", 0)
    ex = rew.get("exp", 0)
    przed = rew.get("przedmioty", {})
    gracz["zloto"] += zl
    gracz["exp"] += ex
    for it, il in przed.items():
        dodaj_przedmiot(gracz, it, il)
    gracz["zadania"][id_z]["aktywne"] = False
    gracz["dziennik"].append("Ukończono zadanie: {}".format(q["nazwa"]))
    print("Ukończono: {}! Otrzymujesz {} zł i {} EXP.".format(q["nazwa"], zl, ex))
    sprawdz_awans(gracz)

def pokaz_zadania(gracz):
    print("\n--- ZADANIA ---")
    for q in ZADANIA:
        qi = gracz["zadania"].get(q["id"])
        if qi:
            prog = qi["postep"]
            req = q.get("liczba", 1)
            status = "aktywne" if qi["aktywne"] else "ukończone"
            print("{}: {} - {} - postęp: {}/{}".format(q["id"], q["nazwa"], status, prog, req))
    print("----------------")

# Crafting
def warsztat(gracz):
    wyczysc()
    print("=== WARSZTAT ===")
    przep = list(PRZEPISY.items())
    for i, (nazwa, sklad) in enumerate(przep, start=1):
        comps = ", ".join(["{}x{}".format(k,v) for k,v in sklad.items()])
        print("{}) {} <- {}".format(i, nazwa, comps))
    print("Wpisz numer aby wykonać, 0 aby wyjść.")
    wyb = input("> ").strip()
    if not wyb.isdigit():
        print("Niepoprawny wybór.")
        return
    idx = int(wyb)
    if idx == 0:
        return
    if 1 <= idx <= len(przep):
        nazwa, sklad = przep[idx-1]
        ok = True
        for mat, ile in sklad.items():
            if gracz["ekwipunek"].get(mat,0) < ile:
                ok = False
                break
        if not ok:
            print("Brakuje surowców.")
            return
        for mat, ile in sklad.items():
            usun_przedmiot(gracz, mat, ile)
        dodaj_przedmiot(gracz, nazwa, 1)
        print("Stworzono {}!".format(nazwa))
        gracz["dziennik"].append("Stworzono {}".format(nazwa))
    else:
        print("Nie ma takiego przepisu.")

# Poziomy i osiągnięcia
def sprawdz_awans(gracz):
    potrzeba = gracz["poziom"] * 50
    while gracz["exp"] >= potrzeba:
        gracz["exp"] -= potrzeba
        gracz["poziom"] += 1
        gracz["max_hp"] += 15
        gracz["hp"] = gracz["max_hp"]
        gracz["atak"] += 2
        gracz["obrona"] += 1
        print("Awansowałeś na poziom {}! Statystyki zwiększone.".format(gracz["poziom"]))
        gracz["dziennik"].append("Awans: {}".format(gracz["poziom"]))
        sprawdz_osiagniecia(gracz)
        potrzeba = gracz["poziom"] * 50

OSIAGN = {
    "pierwsza_krew": {"nazwa": "Pierwsza Krew", "opis": "Pokonaj pierwszego potwora"},
    "skarb_100": {"nazwa": "Mały Skarb", "opis": "Zdobądź 100 zł"},
    "mistrz_zadan": {"nazwa": "Rozwiązywacz Zadań", "opis": "Ukończ 3 zadania"},
}

def sprawdz_osiagniecia(gracz):
    if "pierwsza_krew" not in gracz["osiagniecia"]:
        if any("Pokonałeś" in s for s in gracz["dziennik"]):
            gracz["osiagniecia"].append("pierwsza_krew")
            print("Osiągnięcie: Pierwsza Krew")
    if "skarb_100" not in gracz["osiagniecia"]:
        if gracz["zloto"] >= 100:
            gracz["osiagniecia"].append("skarb_100")
            print("Osiągnięcie: Mały Skarb")
    if "mistrz_zadan" not in gracz["osiagniecia"]:
        done = sum(1 for q in gracz["zadania"].values() if not q["aktywne"])
        if done >= 3:
            gracz["osiagniecia"].append("mistrz_zadan")
            print("Osiągnięcie: Rozwiązywacz Zadań")

# Menu: wioska i podziemia
def menu_wioska(gracz):
    while True:
        wyczysc()
        opis_lokacji("wioska")
        print("\n1) Sklep  2) Warsztat  3) Odpocznij (10 zł)  4) Zadania  5) Ekwipunek  6) Wyjdź")
        c = input("> ").strip()
        if c == "1":
            menu_sklep(gracz)
            pauza()
        elif c == "2":
            warsztat(gracz)
            pauza()
        elif c == "3":
            if gracz["zloto"] >= 10:
                gracz["zloto"] -= 10
                gracz["hp"] = gracz["max_hp"]
                print("Odpocząłeś. HP przywrócone.")
                gracz["dziennik"].append("Odpoczynek")
            else:
                print("Brak 10 zł.")
            pauza()
        elif c == "4":
            menu_zadan(gracz)
            pauza()
        elif c == "5":
            pokaz_ekwipunek(gracz)
            pauza()
        elif c == "6":
            return
        else:
            print("Niepoprawny wybór.")
            pauza()

def menu_zadan(gracz):
    wyczysc()
    print("=== ZADANIA ===")
    for q in ZADANIA:
        print("{} ) {} - {}".format(q["id"], q["nazwa"], q["opis"]))
    print("\n1) Przyjmij zadanie  2) Pokaż aktywne  0) Wyjdź")
    c = input("> ").strip()
    if c == "1":
        qid = input("Podaj ID zadania: ").strip()
        przyjmij_zadanie(gracz, qid)
    elif c == "2":
        pokaz_zadania(gracz)
    elif c == "0":
        return
    else:
        print("Niepoprawny wybór.")

def menu_podziemia(gracz):
    while True:
        wyczysc()
        print("=== PODZIEMIA (HP: {}/{}) ===".format(gracz["hp"], gracz["max_hp"]))
        print("1) Eksploruj  2) Wybierz lokację  3) Zapisz  4) Wróć do wioski")
        c = input("> ").strip()
        if c == "1":
            loc = random.choice([l for l in LOKACJE if l["typ"] in ("loch","dzicz")])
            gracz["lokacja"] = loc["id"]
            print("Idziesz do: {}".format(loc["nazwa"]))
            losowe_zdarzenie(gracz, loc["id"])
            pauza()
            if gracz["hp"] <= 0:
                print("Zginąłeś! Koniec rozgrywki.")
                loguj("{} zginął poza wioską".format(gracz["imie"]))
                zapisz_gre(gracz)
                return
        elif c == "2":
            lista_lokacji()
            wybor = input("Podaj ID lokacji lub 0: ").strip()
            if wybor == "0":
                continue
            if any(l["id"] == wybor for l in LOKACJE):
                gracz["lokacja"] = wybor
                opis_lokacji(wybor)
                losowe_zdarzenie(gracz, wybor)
            else:
                print("Brak takiej lokacji.")
            pauza()
            if gracz["hp"] <= 0:
                print("Zginąłeś! Koniec.")
                zapisz_gre(gracz)
                return
        elif c == "3":
            zapisz_gre(gracz)
            pauza()
        elif c == "4":
            return
        else:
            print("Niepoprawny wybór.")
            pauza()

def lista_lokacji():
    print("\nDostępne lokacje:")
    for l in LOKACJE:
        print("{} - {} ({})".format(l["id"], l["nazwa"], l["typ"]))

# Menu główne i pętla gry
def pokaz_statystyki(gracz):
    print("\n--- STATYSTYKI ---")
    print("Imię: {} | Klasa: {}".format(gracz["imie"], gracz["klasa"]))
    print("Poziom: {} | EXP: {}".format(gracz["poziom"], gracz["exp"]))
    print("HP: {}/{} | Atak: {} | Obrona: {}".format(gracz["hp"], gracz["max_hp"], gracz["atak"], gracz["obrona"]))
    print("Złoto: {} | Lokacja: {}".format(gracz["zloto"], gracz["lokacja"]))
    print("------------------")

def start_nowej_gry():
    wyczysc()
    imie = input("Podaj imię postaci: ").strip() or "Bezimienny"
    print("Wybierz klasę:")
    print("1) Paladyn   2) Czarodziej   3) Łucznik")
    k = input("> ").strip()
    klasy = {"1":"Paladyn","2":"Czarodziej","3":"Łucznik"}
    wybrana = klasy.get(k, "Paladyn")
    gr = stworz_gracza(imie, wybrana)
    gr["dziennik"].append("Utworzono: {}, klasa: {}".format(imie, wybrana))
    loguj("Nowa gra: {}, klasa: {}".format(imie, wybrana))
    przyjmij_zadanie(gr, "z1")
    petla_gry(gr)

def petla_gry(gracz):
    while True:
        wyczysc()
        print("Witaj, {} ({})!".format(gracz["imie"], gracz["klasa"]))
        print("1) Wioska   2) Podziemia   3) Statystyki   4) Ekwipunek   5) Zapisz   6) Wyjdź")
        c = input("> ").strip()
        if c == "1":
            menu_wioska(gracz)
        elif c == "2":
            menu_podziemia(gracz)
            if gracz["hp"] <= 0:
                print("Zginąłeś — koniec gry.")
                zapisz_gre(gracz)
                return
        elif c == "3":
            pokaz_statystyki(gracz)
            pauza()
        elif c == "4":
            pokaz_ekwipunek(gracz)
            pauza()
        elif c == "5":
            zapisz_gre(gracz)
            pauza()
        elif c == "6":
            print("Zapisuję i wychodzę.")
            zapisz_gre(gracz)
            return
        else:
            print("Niepoprawny wybór.")
            pauza()

def menu_glowne():
    wyczysc()
    print("=== PODZIEMIA DRAKARU (wersja BEZ TYPING) ===")
    print("1) Nowa gra")
    print("2) Wczytaj grę")
    print("3) Instrukcja")
    print("4) Zakończ")
    wybor = input("> ").strip()
    if wybor == "1":
        start_nowej_gry()
    elif wybor == "2":
        gr = wczytaj_gre()
        if gr:
            petla_gry(gr)
    elif wybor == "3":
        instrukcja()
    elif wybor == "4":
        print("Do widzenia!")
        sys.exit(0)
    else:
        print("Niepoprawny wybór.")
        pauza()

def instrukcja():
    wyczysc()
    print("""
Instrukcja:
- Eksploruj lokacje, walcz z potworami, zdobywaj złoto i EXP.
- W wiosce możesz kupować i craftować.
- Użyj mikstur i bomb w walce.
- Zapisz grę, aby wrócić później.
Powodzenia!
""")
    pauza()

# Debug/demo helper
def demo_gracz():
    g = stworz_gracza("Demo", "Łucznik")
    g["ekwipunek"]["Kryształ Ognia"] = 1
    g["ekwipunek"]["Sztabka Żelaza"] = 3
    g["ekwipunek"]["Kawałek Skóry"] = 2
    g["zloto"] = 120
    g["exp"] = 40
    return g

# Start programu
if __name__ == "__main__":
    try:
        while True:
            menu_glowne()
    except KeyboardInterrupt:
        print("\nWyjście (CTRL+C). Kończę.")
        sys.exit(0)