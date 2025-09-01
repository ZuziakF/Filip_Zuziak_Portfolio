#Filip Zuziak i Karolina Wróbel
import math                                                                 # Importuje moduł matematyczny do obliczeń (np. exp, potęgi)

def oblicz(x1, x2, x3):                                                     # Definiuje funkcję do obliczenia wartości Y na podstawie wzoru matematycznego
    try:                                                                    # Przechwytuje błędy, które mogą wystąpić w trakcie obliczeń
        y = math.exp(-((x1 - x3) / (x1 - x2 )) ** 2)                         # Oblicza wartość Y wg wzoru: y = e^(-(x1-x3 / x1-x2)^2)
        return y                                                            # Zwraca wynik obliczeń
    except Exception as e:                                                 # Przechwytuje wyjątek (np. dzielenie przez zero)
         raise ValueError(f"Błąd w obliczaniu: {e}")                       # Zwraca komunikat o błędzie jako string

def plik(plik_we="Dane.dat", plik_wy="Wyniki.dat"):       # Funkcja otwiera pliki wejściowy i wyjściowy, przetwarza dane
    
    try:
        with open(plik_we, 'r', encoding='utf-8') as p, open(plik_wy, 'w', encoding='utf-8') as l:  # Otwiera oba pliki z kodowaniem UTF-8
            linie = p.readlines()                                              # Czyta wszystkie linie z pliku wejściowego jako listę

            l.write(linie[0].split('\n')[0] + ",Y\n")                         # Usuwa znak nowej linii z nagłówka, dodaje kolumnę "Y", zapisuje

            for nr, linia in enumerate(linie[1:], start=2):                   # Iteruje po każdej linii (od drugiej), numeruje od 2 (dla błędów)
                try:                                                           # Przechwytuje potencjalne błędy
                    dane = linia.strip().split(",")                                    # Dzieli wiersz po przecinkach, tworzy listę elementów
                    opis, x1, x2, x3 = dane                                     # Próbuje rozpakować dane na 4 zmienne
                    y = oblicz(float(x1), float(x2), float(x3))                # Konwertuje liczby i oblicza Y przy pomocy funkcji
                    l.write(f"{opis},{x1},{x2},{x3},{y}\n")                    # Zapisuje poprawnie przetworzony wiersz do pliku wyjściowego
                except Exception as e:                                         # Jeśli wystąpi wyjątek np. za mało danych, błędna konwersja
                    print(f"BLAD w wierszu {nr}: {e}\n")                     # Zapisuje do pliku komunikat o błędzie z numerem wiersza
    except Exception as e:                                                      #obsluga bledow
        print(f"Wystąpił błąd podczas otwierania plików: {e}")                  #obsluga bledow

if __name__ == "__main__":                                                 # Sprawdza, czy plik został uruchomiony bezpośrednio
    plik()                                                                 # Wywołuje funkcję główną przetwarzającą dane