# Lumio TV backend

Backend obsługujący telewizory Lumio, które są już u klientów: rejestr urządzeń, aktualizacje firmware'u (OTA) i katalog aplikacji.

## Język

### Urządzenia

**Urządzenie**:
Konkretny egzemplarz telewizora u klienta, identyfikowany przez `id` (np. `TV-007`).
_Unikaj_: telewizor (w kodzie i specyfikacjach), klient, egzemplarz

**Model**:
Typ telewizora (np. `LM-50Q21`), do którego należy każde urządzenie. Modele grupują się w serie (S, Q, X).
_Unikaj_: wariant, SKU

**Region**:
Rynek, do którego przypisane jest urządzenie (`EU`, `NA`, `APAC`). Od regionu zależy, który build dostaje urządzenie.
_Unikaj_: kraj, strefa

**Stan urządzenia**:
To, co urządzenie robi w chwili zgłoszenia: `standby` (czuwanie), `menu` albo `watching` (oglądanie).
_Unikaj_: tryb, status

### Aktualizacje

**Okno aktualizacji**:
Warunek, w którym urządzeniu wolno zaproponować aktualizację: stan `standby` i lokalny czas urządzenia od 02:00 do 05:00 (05:00 jest już poza oknem). Obowiązuje dla każdego wydania.
_Unikaj_: okno serwisowe, cisza nocna

**Wersja firmware**:
Trzyczęściowy numer `X.Y.Z` porównywany liczbowo (2.10.1 > 2.9.0). Regionalny przyrostek builda (`-eu`) nie należy do wersji.
_Unikaj_: wersja dwuczęściowa („2.10”)

**Wersja graniczna**:
Najniższa wersja firmware (2.0.0), od której urządzenie w ogóle dostaje aktualizacje. Urządzenie poniżej niej nie dostaje żadnego wydania (zob. ADR-0001).
_Unikaj_: wersja minimalna, stepping stone, wydanie pośrednie

**Wydanie**:
Konkretna wersja firmware'u udostępniona dla listy modeli, z buildem dla każdego regionu.
_Unikaj_: release, aktualizacja (jako rzeczownik dla wydania)

**Build**:
Plik firmware'u konkretnego wydania dla jednego regionu (np. `2.10.1-eu`). To build urządzenie pobiera i instaluje.
_Unikaj_: paczka, obraz

**Rollout**:
Stopniowe udostępnianie wydania: osobny procent urządzeń w każdym regionie. Gdy wydanie ma rollout, region bez ustawionego procentu ma 0%. Wydanie bez rolloutu dostają wszystkie urządzenia.
_Unikaj_: wdrożenie, dystrybucja

**Koszyk rolloutu**:
Stała liczba 0–99 wyliczona z `id` urządzenia i wersji wydania. Urządzenie jest objęte rolloutem, gdy jego koszyk jest mniejszy niż procent dla jego regionu.
_Unikaj_: grupa, próbka
