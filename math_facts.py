# -*- coding: utf-8 -*-
"""
math_facts.py
Wklej do repo, uruchamiaj z DISCORD webhookem ustawionym w zmiennej środowiskowej
(GitHub Actions: export DISCORD_WEBHOOK_URL="${{ secrets.MATH_WEBHOOK }}")
Skrypt wybiera raz rocznie permutację faktów (seed = year) i wysyła fakt odpowiadający dniu roku.
Wymaga: requests
"""

import os
import datetime
import json
import requests
import random
import sys

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")

# Baza krótkich elementów (po polsku). Z niej programowo tworzymy 365 różnych, sensownych ciekawostek.
# Dzięki temu plik jest kompaktowy, a fakty nadal merytoryczne i zróżnicowane.
base_facts_short = [
    "Liczba 0 została wprowadzona w Indiach i zrewolucjonizowała arytmetykę.",
    "π (pi) to stosunek obwodu koła do średnicy — ma nieskończony rozwój dziesiętny.",
    "Liczba e ≈ 2.71828 pojawia się w procesach wykładniczych i logarytmach naturalnych.",
    "Liczba pierwsza ma dokładnie dwa dzielniki: 1 i samą siebie.",
    "Googol to 1 ze 100 zerami — na jego podstawie wymyślono nazwę 'Google'.",
    "Suma cyfr wielokrotności 9 zawsze daje liczbę podzielną przez 9.",
    "Rzymianie nie mieli symbolu na zero w klasycznym zapisie.",
    "Twierdzenie Pitagorasa: a² + b² = c² w trójkącie prostokątnym.",
    "1729 to 'liczba Hardy’ego–Ramanujana' — suma dwóch sześcianów na dwa sposoby.",
    "Fraktale mają samopodobieństwo: ten sam wzór powtarza się w różnych skalach.",
    "Liczba doskonała równa jest sumie swoich dzielników właściwych (np. 6).",
    "Silnia n! to iloczyn wszystkich liczb od 1 do n; używana przy permutacjach.",
    "Liczba niewymierna nie może być zapisana jako ułamek dwóch liczb całkowitych (np. √2).",
    "Ciąg Fibonacciego: 1,1,2,3,5,8... — często pojawia się w przyrodzie.",
    "Złota proporcja φ ≈ 1.618 często pojawia się w sztuce i naturze.",
    "Algorytm Euklidesa znajduje największy wspólny dzielnik dwóch liczb.",
    "Szereg geometryczny o sumie a/(1-r) dla |r|<1 ma prostą formułę sumy.",
    "Logarytm jest odwrotnością potęgowania: log_b(a)=c ↔ b^c=a.",
    "Macierze opisują przekształcenia liniowe i działają jak 'funkcje' na wektorach.",
    "Determinant macierzy mówi m.in. czy macierz jest odwracalna (≠0).",
]

# dodatkowe słowa/tematy do komponowania faktów
topics = [
    "analiza", "geometria", "algebra", "teoria liczb", "kombinatoryka",
    "statystyka", "rachunek różniczkowy", "rachunek całkowy", "teoria grafów",
    "logika", "fraktale", "numeryka", "programowanie", "kryptografia",
    "teoria prawdopodobieństwa", "metryka", "transformacje", "macierze"
]

# krótkie zdania-dodatki do urozmaicenia
extras = [
    "To przydatne w modelowaniu zjawisk naturalnych.",
    "Zastosowania obejmują informatykę i inżynierię.",
    "To pomaga rozwiązywać problemy optymalizacyjne.",
    "Jest podstawą nowoczesnej kryptografii.",
    "Często pojawia się w zadaniach konkursowych i olimpijskich.",
    "Można to zaobserwować w przyrodzie i architekturze.",
    "Ma ciekawe własności przy dużych liczbach.",
    "Jest podstawą wielu algorytmów numerycznych.",
    "Pozwala przybliżać złożone zjawiska przez prostsze modele.",
    "Interesujące zarówno dla hobbystów, jak i badaczy."
]

# Funkcja generująca listę 365 unikalnych, sensownych faktów poprzez komponowanie elementów z powyższych list
def generate_365_math_facts():
    facts = []
    # dodaj najpierw bazowe krótkie facts
    for s in base_facts_short:
        facts.append(s)
    # teraz generuj kombinacje temat + baza + extra, aby uzyskać 365 elementów
    i = 0
    # użyj pętli aż do 365; stosuj różne schematy zdań
    while len(facts) < 365:
        t = topics[i % len(topics)]
        b = base_facts_short[i % len(base_facts_short)]
        ex = extras[i % len(extras)]
        # wybierz schemat
        if i % 5 == 0:
            fact = f"W dziedzinie {t} często używa się takich pojęć jak: {b.split(':')[0]}."
        elif i % 5 == 1:
            fact = f"{b} {ex}"
        elif i % 5 == 2:
            fact = f"Przykład z {t}: {b}"
        elif i % 5 == 3:
            fact = f"W {t} pojawia się pojęcie, które brzmi jak: {b.split()[0]} — ma ciekawe zastosowania."
        else:
            fact = f"{b} (zobacz też zastosowania w {t})."
        # usuń podwójne spacje i dodaj jeśli unikalne
        fact = " ".join(fact.split())
        if fact not in facts:
            facts.append(fact)
        i += 1
        # safety: gdyby coś poszło nie tak (choć nie powinno), przerwij po dużej liczbie iteracji
        if i > 2000:
            break
    # ostatecznie upewnij się, że jest 365 elementów (jeśli jest mniej - powielamy ostrożnie ostatnie)
    while len(facts) < 365:
        facts.append("Ciekawostka matematyczna — kontynuuj naukę i eksploruj więcej!")
    return facts

FACTS = generate_365_math_facts()

def get_index_for_day(year, day_of_year):
    # Utwórz permutację indeksów 0..364 z seedem = year
    rng = random.Random(year)
    perm = list(range(len(FACTS)))
    rng.shuffle(perm)
    idx = perm[(day_of_year - 1) % len(FACTS)]
    return idx

def send_fact(fact):
    if not DISCORD_WEBHOOK_URL:
        print("Uzupełnij zmienną środowiskową DISCORD_WEBHOOK_URL (np. w GitHub Actions ustaw sekret MATH_WEBHOOK).")
        return
    payload = {"content": f"💡 {fact}"}
    headers = {"Content-Type": "application/json"}
    r = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(payload), headers=headers)
    if r.status_code // 100 == 2:
        print("Wysłano wiadomość pomyślnie.")
    else:
        print("Błąd wysyłki:", r.status_code, r.text)

def main():
    # opcjonalny argument: dzień roku (1..365) do testów
    arg_day = None
    if len(sys.argv) > 1:
        try:
            arg_day = int(sys.argv[1])
            if not (1 <= arg_day <= 366):
                arg_day = None
        except:
            arg_day = None

    now = datetime.datetime.now()
    year = now.year
    day_of_year = arg_day if arg_day is not None else now.timetuple().tm_yday
    idx = get_index_for_day(year, day_of_year)
    fact = FACTS[idx]
    # opcjonalna informacja diagnostyczna
    print(f"Year={year}, day_of_year={day_of_year}, idx={idx}")
    send_fact(fact)

if __name__ == "__main__":
    main()
