import tkinter as tk #import biblioteki
from tkinter import filedialog, messagebox #import biblioteki
import pandas as pd #import biblioteki
import numpy as np  #import biblioteki
import matplotlib.pyplot as plt #import biblioteki

def wspolczynnik_giniego(x):  #definiujemy funkcję który policzy współczynnik giniego
    x = np.sort(x)  #sortujemy dane
    n = len(x)  #n posiada wartość równą długości tablicy
    indeksy = np.arange(1, n + 1)  #tworzymy tablice [1,2,3....n] 
    return (2 * np.sum(indeksy * x)) / (n * np.sum(x)) - (n + 1) / n   #zwracamy współczynnik giniego ze wzoru

def krzywa_lorenza(x):  #definiujemy funkcję, która rysuje nam wykres 
    x = np.sort(x)  #sortujemy tablicę
    S = np.cumsum(x) / np.sum(x)  #tworzymy skumulowane sumy zwane też sumami prefiksowymi
    S = np.insert(S, 0, 0)  #wrzucamy na przód tabeli punkt (0,0)
    return np.linspace(0, 1, len(S)), S #zwracamy oś X czyli punkty w zakresie od 0 do 1 (skumulowany udział populacji) oraz Y  udział dochodów

def wybierz_plik(wynik_label): #definiujemy funkcję dzięki której możemy wybrać plik i wygenerowac wykres
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")]) #wybieramy plik (format .xlsx czyli Excel)
    if not filepath: #jezeli pliku nie ma
        return #zwracamy nic
    
    try: #obsługa błędów
        df = pd.read_excel(filepath) #zbieramy wartości z pliku
        if 'dochód' not in df.columns: #szukamy kolumny dochód
            messagebox.showerror("Błąd", "Kolumna 'dochód' nie została znaleziona w pliku.") #błąd
            return #zwracamy nic
        
        dochody = df['dochód'].values #tworzymy tablice z wartości kolumny dochód
        gini = wspolczynnik_giniego(dochody) #liczymy współczynnik giniego
        
        
        wynik_label.config(text=f"Współczynnik Giniego: {gini:.4f}")# Wyświetlenie wyniku
        
        
        x_lorenz, y_lorenz = krzywa_lorenza(dochody) #oś OX i OY
        plt.figure(figsize=(6, 6)) #wielkość okna z wykresem
        plt.plot(x_lorenz, y_lorenz, label='Krzywa Lorenza', color='blue') #elementy estetyczne 
        plt.plot([0, 1], [0, 1], '--', color='red', label='Linia równości') #elementy estetyczne
        plt.title(f'Krzywa Lorenza\n(Gini = {gini:.4f})') #tytuł z wynikiem 
        plt.xlabel('Skumulowany udział populacji') #tytuł osi OX
        plt.ylabel('Skumulowany udział dochodu') #tytuł osi OY
        plt.legend() #legenda
        plt.grid() #siatka
        plt.tight_layout() #wyrównywanie elementów wykresu aby na siebie nie nachodziły
        plt.show() #pokaz wykres

    except Exception as e: #obsługa błędów
        messagebox.showerror("Błąd", f"Coś poszło nie tak:\n{e}") #informacja o błędzie

def click_fun(wn, _ml):
    # GUI - Tkinter
    root = tk.Tk()  #Okno aplikacji
    root.title("Obliczanie współczynnika Giniego") #tytuł

    wynik_label = tk.Label(root, text="Witamy!!!", font=('Times New Roman', 10)) #etykieta
    wynik_label.pack(pady=2) #elementy kosmetyczne

    btn = tk.Button(root, text="Wybierz plik Excel", command=lambda: wybierz_plik(wynik_label)) #przycisk do wyboru pliku i funkcja lambda która pomaga nam się odwołać do funkcji "wybierz plik"
    btn.pack(pady=10) #elementy kosmetyczne

    root.mainloop() #bez tego okno GUI by sie nie pokazało

if __name__ == '__main__': #sekcja testowa 
    click_fun(None,None) #wywołanie funkcji main