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
   "0 (zero) zostało wprowadzone przez hinduskich matematyków i zrewolucjonizowało arytmetykę.",
"π (pi) to stosunek obwodu koła do jego średnicy — ma nieskończony, nieokresowy rozwój dziesiętny.",
"Liczba e (≈2.71828) pojawia się naturalnie w rachunku różniczkowym i w logarytmach naturalnych.",
"Liczba pierwsza to taka, która ma dokładnie dwa dzielniki: 1 i samą siebie.",
"Googol to 1 ze 100 zerami; googolplex to 1 i googol zer.",
"Zasada Dzielnika: suma cyfr wielokrotności 9 jest podzielna przez 9.",
"Zero nie występuje w zapisie rzymskim — Rzymianie nie używali symbolu na 'nic'.",
"Twierdzenie Pitagorasa: w trójkącie prostokątnym a² + b² = c².",
"Fermat twierdził, że nie ma całkowitych rozwiązań równania a^n + b^n = c^n dla n>2 (wykonane przez Andrew Wiles w 1994).",
"Liczba 1729 to najmniejsza liczba, którą można zapisać jako sumę dwóch sześcianów na dwa różne sposoby.",
"Suma kątów w trójkącie euklidesowym wynosi 180°.",
"Fraktale mają nieskończoną złożoność i samopodobieństwo przy różnych skalach.",
"Zero jest jedyną liczbą, która nie jest ani dodatnia, ani ujemna.",
"Liczby doskonałe to te równe sumie swoich dzielników właściwych (np. 6 = 1+2+3).",
"Permutacja to uporządkowanie elementów; kombinacja to wybór bez kolejności.",
"Liczba niewymierna nie może być zapisana jako ułamek dwóch liczb całkowitych (np. √2).",
"Kombinatoryka liczy sposoby wyboru i ułożenia obiektów — jest podstawą prawdopodobieństwa.",
"Silnia n! to iloczyn wszystkich liczb 1..n; używana przy permutacjach.",
"Matematyczna indukcja to technika dowodowa: baza + krok indukcyjny.",
"Liczby Fibonacciego (1,1,2,3,5,8...) pojawiają się w naturze i mają związek ze złotą proporcją.",
"Złota proporcja φ ≈ 1.618 występuje w przyrodzie i sztuce.",
"Irracjonalność √2: dowód elementarny pokazuje, że pierwiastek z 2 nie jest rationalny.",
"Przekształcenia geometryczne: translacja, obrót, odbicie i skala.",
"Macierz to prostokątna tablica liczb używana do równań liniowych i transformacji.",
"Determinant macierzy 2x2 to ad − bc; mówi m.in. czy macierz jest odwracalna.",
"Równania kwadratowe mają wzór rozwiązujący: x = (-b ± √(b²-4ac)) / (2a).",
"Prawo rozdzielności: a(b+c)=ab+ac — podstawowa własność mnożenia.",
"Redukcja reszt modulo: a ≡ b (mod n) oznacza, że n dzieli (a-b).",
"Liczba e pojawia się w zjawiskach wykładniczego wzrostu i zaniku.",
"Symetria grupowa opisuje ruchy zachowujące strukturę — fundament teorii grup.",
"Grafy składają się z wierzchołków i krawędzi; przydatne w sieciach i trasach.",
"Algorytm Euklidesa znajduje największy wspólny dzielnik (NWD) dwóch liczb.",
"Liczby Bernoulliego i szeregi potęgowe pojawiają się w analizie i teorii liczb.",
"Równanie różniczkowe opisuje zmiany — podstawowe w fizyce i modelowaniu.",
"Kąt prosty ma 90°; kąt półpełny 180°, pełny 360°.",
"Twierdzenie Talesa: jeśli A,B,C są na okręgu, to... (różne sformułowania).",
"Logarytm to odwrotność potęgowania: log_b(a) = c ↔ b^c = a.",
"Binom Newtona: (a+b)^n = suma_{k=0..n} C(n,k) a^{n-k} b^k.",
"Cycylindry i stożki: objętość walca V=πr^2h, stożka V=(1/3)πr^2h.",
"Granica funkcji to podstawowe pojęcie w analizie matematycznej.",
"Liczba Catalana pojawia się w problemach z drzewami i kombinatoryką.",
"Suma nieskończonego szeregu geometrycznego a/(1-r) dla |r|<1.",
"Pojęcie asymptoty: krzywa może zbliżać się do prostej, nie przecinając jej.",
"Dowód niekonstruktywny pokazuje istnienie obiektu bez jego zbudowania.",
"Transformata Fouriera rozkłada sygnał na składowe częstotliwościowe.",
"Rachunek prawdopodobieństwa opiera się na wynikach, przestrzeniach próbek i zdarzeniach.",
"Funkcja to przyporządkowanie każdemu x uniklany y; injekcja, surjekcja, bijekcja.",
"Mnożenie macierzy nie jest przemienne: AB ≠ BA w ogólności.",
"Rozwinięcie dziesiętne liczby niewymiernej jest nieskończone i nieokresowe.",
"Prawo dużych liczb: średnia prób zbiega do wartości oczekiwanej przy dużych próbach.",
"Statystyka opisowa obejmuje średnią, medianę, dominantę i odchylenie standardowe.",
"Punkt stały: f(x)=x; twierdzenie Banacha gwarantuje istnienie w pewnych warunkach.",
"Transformacje afiniczne zachowują równoległość, ale niekoniecznie kąty.",
"Równania Diofantyczne to równania z całkowitymi rozwiązaniami (np. a^2 + b^2 = c^2).",
"Kombinacje z powtórzeniami liczymy jako C(n+k-1,k).",
"Funkcja wykładnicza rośnie szybciej niż potęgi wielomianowe.",
"Macierz odwrotna A^{-1} spełnia AA^{-1}=I, jeśli determinant ≠ 0.",
"Metoda najmniejszych kwadratów dopasowuje prostą do punktów (regresja liniowa).",
"Zasada szufladkowa (Dirichleta): jeśli n+1 przedmiotów w n pudełkach → przynajmniej jedno pudełko ma ≥2.",
"Różniczka i pochodna: pochodna to szybkość zmian funkcji.",
"Całka oznaczona mierzy pole pod wykresem funkcji.",
"Różnice skończone są dyskretną analogią pochodnej.",
"Przekształcenie Laplace'a ułatwia rozwiązywanie równań różniczkowych.",
"Dualność w programowaniu liniowym łączy zadanie primal i dual.",
"Algorytm simpleks rozwiązuje zadania programowania liniowego.",
"Macierz diagonalna ma niezerowe elementy tylko na głównej przekątnej.",
"Własności liczb parzystych i nieparzystych przy mnożeniu i dodawaniu.",
"Przebieg funkcji: monotoniczność, ekstremum lokalne i globalne.",
"Ortogonalność wektorów: ich iloczyn skalarny wynosi 0.",
"Norma wektora to jego długość, np. norma euklidesowa.",
"Równania parametryczne opisują krzywe przez parametr t.",
"Podział na klasy zbieżności: zbieżność punktowa i jednostajna dla funkcji.",
"Kwantyzacja: reprezentowanie wartości ciągłych w postaci dyskretnej (informatyka).",
"Przykład rekurencji: a_{n+1} = a_n + 2 (ciąg arytmetyczny).",
"Rozwiązywanie układów równań: metoda podstawiania, przeciwnych współczynników i macierzy.",
"Macierz jedności I pozostawia wektor bez zmiany przy mnożeniu.",
"Równanie liniowe w jednej niewiadomej: ax + b = 0 → x = -b/a.",
"Algebra Boole'a używana w logice cyfrowej: AND, OR, NOT.",
"Transpozycja macierzy A^T zmienia wiersze na kolumny.",
"Złożenie funkcji: (f∘g)(x) = f(g(x)).",
"Cięciwa, promień i średnica: relacje w kole.",
"Prawo sinusa i cosinusa w trójkątach ogólnych.",
"Macierz ortogonalna ma odwrotność równą transpozycji: A^{-1} = A^T.",
"Równania rekurencyjne opisują ciągi poprzez poprzednie wyrazy.",
"Permutation parity: permutacje mają parzystość (parzysta/nieparzysta).",
"Rozkład na czynniki pierwsze jest jednoznaczny (Fundamentalne twierdzenie arytmetyki).",
"Szereg Taylora przybliża funkcję przez wielomian w okolicach punktu.",
"Prawo wielkich liczb: przy dużej liczbie prób przybliżona częstotliwość → prawdziwe prawdopodobieństwo.",
"Izomorfizm grup mówi, że dwie struktury są 'takie same' strukturalnie.",
"Algorytm BFS i DFS w grafach: eksplorują wierzchołki w różnej kolejności.",
"Złożoność obliczeniowa: np. O(1), O(n), O(n log n), O(n^2) opisuje skalowanie algorytmów.",
"Metoda Newtona (Newton-Raphson) przybliża pierwiastki funkcji.",
"Rozkład LU dekomponuje macierz na iloczyn macierzy dolnotrójkątnej i górnotrójkątnej.",
"Prawo addytywności wariancji dla niezależnych zmiennych losowych.",
"Kładzenie płytek (tiling) łączy geometrię i kombinatorykę.",
"Liczba Armstronga (np. 153 = 1^3+5^3+3^3) — ciekawostka z teorii liczb.",
"Transformacje Möbiusa mapują okręgi i proste na okręgi i proste.",
"Metoda elementów skończonych (FEM) przybliża rozwiązania równań różniczkowych cząstkowych.",
"Przekształcenia afiniczne zachowują barycentryczne współczynniki.",
"Spośród wszystkich prostokątów o danym obwodzie największe pole ma kwadrat.",
"Najkrótsza ścieżka w grafie ważonym: algorytm Dijkstry.",
"Dowód przez sprzeczność zaczyna od założenia negacji i dochodzi do sprzeczności.",
"Funkcje parzyste: f(-x)=f(x); nieparzyste: f(-x)=-f(x).",
"Twierdzenie Wilsona: p jest liczbą pierwszą ⇔ (p-1)! ≡ -1 (mod p).",
"Liczby Mersenne’a mają postać 2^p - 1 (p pierwsze) — ważne w poszukiwaniu dużych liczb pierwszych.",
"Kierunki gradientu wskazują na najszybszy wzrost funkcji.",
"Wektor własny i wartość własna: A v = λ v — kluczowe w wielu zastosowaniach.",
"Równania kwadratowe mogą mieć dwa, jeden lub zero rzeczywistych rozwiązań zależnie od delty.",
"Teoria grafów stosuje się w logistyce, sieciach społecznych i telekomunikacji.",
"Model probabilistyczny: np. rozkład Poissona modeluje rzadkie zdarzenia.",
"Paradoks Banacha-Tarskiego: rozdział i złożenie kuli daje dwie kule tej samej objętości (Aksjomaty ZF + wybór).",
"Geometria sferyczna rządzi się innymi regułami: suma kątów trójkąta >180°.",
"Uwaga: nie każda nieskończona suma ma sens — potrzeba warunków zbieżności.",
"Krzywa parametryczna może reprezentować ruch cząstki w czasie.",
"Rangą macierzy nazywamy liczbę liniowo niezależnych wierszy (kolumn).",
"Prawo De Morgana: ¬(A ∧ B) = ¬A ∨ ¬B oraz ¬(A ∨ B) = ¬A ∧ ¬B.",
"Reprezentacje liczb binarnych, ósemkowych i szesnastkowych są powszechne w informatyce.",
"Iloczyn skalarny daje miarę zgodności kierunków wektorów.",
"Współczynniki binominalne C(n,k) to liczba sposobów wyboru k elementów z n.",
"Dowolny wielomian stopnia n ma co najmniej jedno (może zespolone) zero (Podstawowe Twierdzenie Algebry).",
"Separacja zmiennych pomaga rozwiązywać niektóre równania różniczkowe zwyczajne.",
"Kwadratura koła — klasyczny problem; udowodniono, że nie da się skonstruować cyrklem i linijką liczby π.",
"Funkcja Dirichleta i funkcje arytmetyczne używane są w teorii liczb.",
"Równanie Schrödingera w fizyce kwantowej to równanie różniczkowe cząstkowe.",
"Macierz stożka: ciekawostki o macierzach symetrycznych i ich własnych wartościach.",
"Zastosowania matematyki dyskretnej: kryptografia, algorytmy i teoria informacji.",
"Równania rekurencyjne mają zastosowania w analizie algorytmów (np. sortowanie).",
"Przekształcenie złożenia: włóż jedną funkcję w drugą to często upraszcza model.",
"Własności wykresów funkcji: asymptoty pionowe i poziome mówią o zachowaniu dla dużych x.",
"Znakowanie sumy: Σ (sigma) oznacza sumę wyrazów.",
"Testy na całkowalność i zbieżność: Cauchy'ego, porównawczy, ilorazowy.",
"Funkcje elementarne: wielomiany, wykładnicze, logarytmy, trygonometryczne.",
"Algorytm euklidesowy można rozszerzyć do wyznaczenia współczynników kombinacji liniowej (rozszerzony algorytm Euklidesa).",
"Powierzchnia kuli: 4πr^2; objętość: (4/3)πr^3.",
"Analityczne i geometryczne interpretacje pochodnej: nachylenie stycznej i szybkość zmian.",
"Kwadrat magiczny: suma w każdym wierszu/kolumnie/przekątnej taka sama.",
"Reprezentacja funkcji jako sumy funkcji prostych (np. seria Fouriera).",
"Unikalność rozkładu na czynniki pierwsze jest fundamentem arytmetyki.",
"Złączenie probabilistyczne a independence: P(A∩B)=P(A)P(B) jeśli niezależne.",
"Topologia bada właściwości zachowane przy ciągłych deformacjach (np. rozciąganie, zgniatanie).",
"Algorytm szybkiego potęgowania (exponentiation by squaring) przyspiesza obliczenia potęg.",
"Dowód istnienia liczb pierwszych (Euklides): jest ich nieskończenie wiele.",
"Macierz stochastyczna używana jest w łańcuchach Markowa do opisu przejść.",
"Permutacje cykliczne i rozkład na cykle mają zastosowania w kombinatoryce.",
"Użycie logarytmów ułatwia mnożenie i dzielenie dużych liczb (przed kalkulatorami).",
"Suma harmoniczna H_n = 1 + 1/2 + ... + 1/n rośnie powoli (≈ ln n + γ).",
"Metody probabilistyczne pozwalają udowadniać twierdzenia istnienia.",
"Twierdzenie o wartości pośredniej: jeśli f jest ciągła na [a,b], to przyjmuje każdą wartość między f(a) i f(b).",
"Macierz projekcji 'rzuca' wektor na podprzestrzeń.",
"Polinom orthogonalny (np. Czebyszew) ma zastosowania numeryczne.",
"Modele regresji pozwalają przewidywać związek między zmiennymi.",
"Równanie różniczkowe liniowe ma rozwiązania sumy rozwiązania jednorodnego i szczególnego.",
"Metoda Gaussa eliminuje niewiadome w układach liniowych.",
"Twierdzenie Cayley-Hamilton: każda macierz spełnia swój własny wielomian charakterystyczny.",
"Analiza numeryczna zajmuje się przybliżeniami obliczeń i stabilnością.",
"Powtarzalne iteracje mogą prowadzić do okresów lub chaosu (teoria chaosu).",
"Zastosowania kombinatoryki w kryptografii (np. klucze i permutacje).",
"Liczba eulerowska dla grafu V-E+F = 2 dla grafów planarnych.",
"Symbole Newtona i wzór na pochodną potęgi: d/dx x^n = n x^{n-1}.",
"Dowolna permutacja może być przedstawiona jako produkt cykli.",
"Jeśli f jest różniczkowalna, to jest ciągła — ale nie odwrotnie.",
"Zastosowania macierzy w grafice komputerowej (skalowanie, rotacja).",
"Równania parametryczne okręgu: x = r cos t, y = r sin t.",
"Prawo malejącego przyrostu: przyrost jest proporcjonalny do aktualnej wartości (model wykładniczy).",
"Zastosowanie liczby pierwszej w kryptografii, np. RSA wykorzystuje dużą parę liczb pierwszych.",
"Funkcje trygonometryczne są okresowe; sin, cos mają okres 2π.",
"Dowód przez kontrapozycję: jeśli A ⇒ B, to ¬B ⇒ ¬A.",
"Funkcje wielomianowe stopnia n mają co najwyżej n miejsc zerowych (z uwzględnieniem krotności).",
"Styczna do okręgu w punkcie jest prostopadła do promienia w tym punkcie.",
"Irracjonalność liczby π została udowodniona przez Lindemanna w 1882.",
"Równania nieliniowe często wymagają metod numerycznych do rozwiązywania.",
"Permutacja z k cyklami ma parzystość zależną od długości cykli.",
"Model Markowa: przyszły stan zależy tylko od stanu obecnego (brak pamięci).",
"Obwód trójkąta równobocznego o boku a = 3a, pole = (√3/4) a^2.",
"Skala logarytmiczna pokazuje rzędy wielkości i ułatwia porównania.",
"Symetrie i grupy Liego mają zastosowania w fizyce teoretycznej.",
"Testy całkowe i kryteria porównawcze służą do badania zbieżności szeregów.",
"Uwaga: nie wszystkie nieskończone zbiory mają tę samą moc (np. ℕ vs ℝ).",
"Funkcja odwrotna f^{-1} istnieje jeśli f jest bijekcją.",
"Zasada minimalnego działania (z fizyki) może być zapisana matematycznie przy użyciu wariacyjnych metod.",
"Szeregi potęgowe przydają się do rozwiązywania równań i przybliżeń.",
"Geometria analityczna łączy algebrę z geometrią przez współrzędne.",
"Twierdzenie o reszcie chińskiej pozwala rozwiązywać kongruencje wielomodułowe.",
"Równanie Bernoulliego to przykład równania różniczkowego, który można sprowadzić do liniowego.",
"Teoria miary i całki Lebesgue'a rozszerza klasyczną całkę Riemanna.",
"Zestaw liczb: N, Z, Q, R, C — naturalne, całkowite, wymierne, rzeczywiste, zespolone.",
"Dowód konstruktywny pokazuje, jak zbudować obiekt, nie tylko, że istnieje.",
"Symetria w układach równań upraszcza rozwiązywanie.",
"Równania parametryczne i współrzędne biegunowe pozwalają opisać nietypowe krzywe.",
"Analogia między calką a sumą Riemanna: przybliżamy pole pod krzywą.",
"Metoda najmniejszych kwadratów minimalizuje sumę kwadratów błędów.",
"Zastosowania obliczeń symbolicznych: CAS (Computer Algebra Systems) upraszczają wyrażenia.",
"Teoria kategorii bada struktury i morfizmy — abstrakcja nad strukturami matematycznymi.",
"Macierz diagonalizowalna jest łatwa do potęgowania i analizy.",
"Zagadnienia NP i NP-zupełne: ważne w teorii złożoności obliczeniowej.",
"Algorytm sortowania quicksort ma przeciętną złożoność O(n log n).",
"Model regresji logistycznej przewiduje prawdopodobieństwo zdarzenia binarnego.",
"Macierz odwrotna istnieje tylko jeśli determinant ≠ 0.",
"Zastosowania algebry liniowej w uczeniu maszynowym: wektory cech, macierze wag.",
"Zachowanie iteracji funkcji może prowadzić do fraktali (np. zbiór Julii).",
"Twierdzenie Weierstrassa: każda funkcja ograniczona i ciągła na domkniętym przedziale osiąga maksimum i minimum.",
"Podstawowe algorytmy kryptograficzne opierają się na trudności faktoryzacji dużych liczb.",
"Metody Monte Carlo wykorzystują losowanie do przybliżeń numerycznych.",
"Rozkład wartości własnych macierzy ma znaczenie w dynamice i stabilności układów.",
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
