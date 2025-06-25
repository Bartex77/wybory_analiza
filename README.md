# wybory_analiza
Analiza wyników wyborów prezydenckich 2025

Sposób użycia programu:
```
python3 wybory_analiza.py [rows] [t/n/g]
```
gdzie: 
`rows` - liczba wyświetlanych komisji
`t` - wyniki na niekorzyść Trzaskowskiego
`n` - wyniki na niekorzyść Nawrockiego
`g` - wyniki w problematycznych gminach (ich lista jest w kodzie)

Brak opcji `t/n/g` powoduje wyświetlanie danych niezależnie od faworyzowanego kandydata.

Przykład:
```
python3 wybory_analiza.py 20 g
```
wyświetli 20 pierwszych komisji z wymienianych jako problematyczne.

```
python3 wybory_analiza.py 30 t
```
wyświetli 30 pierwszych komisji, w których Trzaskowski dostał mniej głosów, niż szacuje model.

Wyniki każdorazowo zapisywane są w pliku `wyniki.xlsx`.
