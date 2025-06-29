# Analiza odchyleń od trendu przepływu głosów (I -> II tura)
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Analiza danych wyborczych")
parser.add_argument("n", nargs="?", type=int, default=30, help="Liczba zapisów")
parser.add_argument("k", nargs="?", type=str, default="", help="Kandydat (n/t/g)")
args = parser.parse_args()
rows_number = args.n
candidate = args.k

# Wczytanie plików z uwzględnieniem separatora i kodowania
pierwsza_tura = pd.read_csv("protokoly_po_obwodach_utf8.csv", sep=";", encoding="utf-8")
druga_tura = pd.read_csv("protokoly_po_obwodach_w_drugiej_turze_utf8.csv", sep=";", encoding="utf-8")

pierwsza_tura = pierwsza_tura[~pierwsza_tura["Gmina"].str.lower().str.contains("zagranica", na=False)]
druga_tura = druga_tura[~druga_tura["Gmina"].str.lower().str.contains("zagranica", na=False)]

# Czyszczenie nagłówków
pierwsza_tura.columns = pierwsza_tura.columns.str.strip().str.upper().str.replace("\xa0", " ")
druga_tura.columns = druga_tura.columns.str.strip().str.upper().str.replace("\xa0", " ")

# Klucz do łączenia
merge_key = ["GMINA", "POWIAT", "NR KOMISJI"]

# Łączenie danych
common = pd.merge(pierwsza_tura, druga_tura, on=merge_key, suffixes=("_1T", "_2T"))

# Preferencje drugoturówki (Trzaskowski, Nawrocki)
transfer = {
    "BARTOSZEWICZ ARTUR": (0.15, 0.70),
    "BIEJAT MAGDALENA AGNIESZKA": (0.80, 0.10),
    "BRAUN GRZEGORZ MICHAŁ": (0.05, 0.90),
    "HOŁOWNIA SZYMON FRANCISZEK": (0.85, 0.10),
    "JAKUBIAK MAREK": (0.10, 0.80),
    "MACIAK MACIEJ": (0.15, 0.70),
    "MENTZEN SŁAWOMIR JERZY": (0.05, 0.70),
    "SENYSZYN JOANNA": (0.85, 0.05),
    "STANOWSKI KRZYSZTOF JAKUB": (0.20, 0.20),
    "WOCH MAREK MARIAN": (0.20, 0.60),
    "ZANDBERG ADRIAN TADEUSZ": (0.80, 0.15),
}

# Liczba głosów w I i II turze (tylko głosy ważne)
common["SUMA_1T"] = common[[k for k in transfer.keys() if k in common.columns]].sum(axis=1) + \
                    common[["TRZASKOWSKI RAFAŁ KAZIMIERZ_1T", "NAWROCKI KAROL TADEUSZ_1T"]].sum(axis=1)
common["SUMA_2T"] = common[["TRZASKOWSKI RAFAŁ KAZIMIERZ_2T", "NAWROCKI KAROL TADEUSZ_2T"]].sum(axis=1)

# Współczynnik przeskalowania dla zmian liczby głosujących
common["WSPOL_SZACUNKOWY"] = common["SUMA_2T"] / common["SUMA_1T"]
common["WSPOL_SZACUNKOWY"] = common["WSPOL_SZACUNKOWY"].fillna(1.0)

# Obliczenia predykcyjne (tylko dla kandydatów spoza II tury)
trz_pred, naw_pred = 0, 0
for k, (t, n) in transfer.items():
    if k in common.columns:
        trz_pred += common[k] * t
        naw_pred += common[k] * n

trz_pred += common["TRZASKOWSKI RAFAŁ KAZIMIERZ_1T"]
naw_pred += common["NAWROCKI KAROL TADEUSZ_1T"]

# Przeskalowanie do faktycznej liczby głosów w II turze
common["TRZASKOWSKI_SZAC"] = (trz_pred * common["WSPOL_SZACUNKOWY"]).round(0)
common["NAWROCKI_SZAC"] = (naw_pred * common["WSPOL_SZACUNKOWY"]).round(0)
common["TRZASKOWSKI_REAL"] = common["TRZASKOWSKI RAFAŁ KAZIMIERZ_2T"]
common["NAWROCKI_REAL"] = common["NAWROCKI KAROL TADEUSZ_2T"]

# Odchylenia
common["ODCH_TRZ"] = (common["TRZASKOWSKI_REAL"] - common["TRZASKOWSKI_SZAC"]).round(0)
common["ODCH_NAW"] = (common["NAWROCKI_REAL"] - common["NAWROCKI_SZAC"]).round(0)
common["ODCH_SUM"] = abs(common["ODCH_TRZ"]) + abs(common["ODCH_NAW"])

match candidate:
    case "g":
        filtered = common[
            ((common["NR KOMISJI"] == 4) &
             (common["GMINA"] == "gm. Bychawa")) |
            ((common["NR KOMISJI"] == 4) &
             (common["GMINA"] == "gm. Staszów")) |
            ((common["NR KOMISJI"] == 1) &
             (common["GMINA"] == "gm. Magnuszew")) |
            ((common["NR KOMISJI"] == 113) &
             (common["GMINA"] == "Mokotów")) |
            ((common["NR KOMISJI"] == 6) &
             (common["GMINA"] == "m. Kamienna Góra")) |
            ((common["NR KOMISJI"] == 95) &
             (common["GMINA"] == "m. Kraków")) |
            ((common["NR KOMISJI"] == 3) &
             (common["GMINA"] == "gm. Olesno")) |
            ((common["NR KOMISJI"] == 9) &
             (common["GMINA"] == "gm. Strzelce Opolskie")) |
            ((common["NR KOMISJI"] == 35) &
             (common["GMINA"] == "m. Tychy")) |
            ((common["NR KOMISJI"] == 61) &
             (common["GMINA"] == "m. Bielsko-Biała")) |
            ((common["NR KOMISJI"] == 30) &
             (common["GMINA"] == "m. Bielsko-Biała")) |
            ((common["NR KOMISJI"] == 10) &
             (common["GMINA"] == "gm. Tarnów")) |
            ((common["NR KOMISJI"] == 13) &
             (common["GMINA"] == "m. Mińsk Mazowiecki")) |
            ((common["NR KOMISJI"] == 17) &
             (common["GMINA"] == "m. Gdańsk")) |
            ((common["NR KOMISJI"] == 25) &
             (common["GMINA"] == "m. Grudziądz")) |
            ((common["NR KOMISJI"] == 4) &
             (common["GMINA"] == "gm. Brześć Kujawski")) |
            ((common["NR KOMISJI"] == 53) &
             (common["GMINA"] == "m. Katowice"))
            ]
    case "t":
        filtered = common[common["ODCH_TRZ"] < 0]
    case "n":
        filtered = common[common["ODCH_NAW"] < 0]
    case _:
        filtered = common

result = filtered.sort_values("ODCH_SUM", ascending=False)[
    merge_key + ["SUMA_1T", "SUMA_2T", "TRZASKOWSKI RAFAŁ KAZIMIERZ_1T", "TRZASKOWSKI_SZAC", "TRZASKOWSKI_REAL", "NAWROCKI KAROL TADEUSZ_1T", "NAWROCKI_SZAC", "NAWROCKI_REAL", "ODCH_TRZ", "ODCH_NAW", "ODCH_SUM"]
].head(rows_number)

with pd.option_context('display.float_format', '{:,.0f}'.format):
    print(result.to_string(index=False))

# Suma odchyleń dla kandydatów
suma_trz = common["ODCH_TRZ"].sum()
suma_naw = common["ODCH_NAW"].sum()
print(f"\nSuma odchyleń globalnie (Trzaskowski): {int(suma_trz)}")
print(f"Suma odchyleń globalnie (Nawrocki): {int(suma_naw)}")

result.to_excel("wyniki.xlsx", index=False)
