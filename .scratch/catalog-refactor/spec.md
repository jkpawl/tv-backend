# Refaktoryzacja `get_apps_for_device` w katalogu aplikacji

Status: ready-for-agent

## Problem Statement

`get_apps_for_device` w `backend/catalog.py` to jedna długa funkcja z flagą `ok`, dwukrotnie powielonym parsowaniem wersji, ręcznym scalaniem dwóch posortowanych list i jednoliterowymi nazwami (`mdl`, `fw`, `p`, `q`, `r`, `x`). Trudno z niej odczytać reguły katalogu: filtr regionu, minimalny firmware, wybór paczki (ze specjalną regułą dla modeli z 2019) i kolejność na ekranie.

Obecne zachowanie utrwalają testy charakteryzacyjne w `tests/test_catalog_characterization.py` (commit `c643b0e`).

## Solution

Rozbić funkcję na małe, nazwane helpery bez żadnej zmiany zachowania. Sygnatura `get_apps_for_device(store, device, include_hidden=False)` zostaje bez zmian, bo woła ją `backend/api.py`. Istniejące testy nie są zmieniane.

Zachowane zostają także wątpliwe zachowania:

- modele z 2019 zawsze dostają pierwszą paczkę, także powyżej `max_api`,
- przy pustej liście `packages` model z 2019 rzuca `IndexError`,
- wersja `"1.100"` liczy się jak `2.0` (`major*100 + minor`),
- przy zduplikowanym modelu w `models` wygrywa ostatni wpis.

## Krok 0: uzupełnić siatkę testów (osobny commit, przed refaktoryzacją)

Trzy zachowania łatwo zmienić przy refaktoryzacji, a testy ich dziś nie pilnują:

- [ ] **`firmware: None` w urządzeniu** rzuca `AttributeError` (`None.split` nie jest łapane przez `except (ValueError, IndexError)`).
- [ ] **Remis w `api` między paczkami:** wygrywa pierwsza paczka (porównanie `>` jest ścisłe).
- [ ] **`featured` o wartości truthy, ale nie `True`** (np. `1`): na wyjściu `featured` jest `True` albo `False`.

To dodanie testów, a nie refaktoryzacja, więc osobny commit.

## Kroki refaktoryzacji

Każdy krok to osobny commit, po którym wszystkie testy przechodzą.

1. **`_version_number(text)`:** jedno miejsce zamiast dwóch identycznych bloków parsowania `major*100 + minor`. Łapie tylko `ValueError` i `IndexError`, jak dziś. Wartości domyślne `"0.0"` zostają w miejscach wywołania.
2. **`_find_model(models, name)`:** wyszukanie modelu z zachowaną regułą „wygrywa ostatni wpis” (`reversed(models)` z `return` albo pętla bez `break`). `== None` zamienione na `is None`.
3. **`_is_available(app, device, firmware, include_hidden)`:** filtry ukrytych aplikacji, regionu i minimalnego firmware'u jako wczesne `return False` zamiast flagi `ok`. Brak pola `regions` nadal oznacza pustą listę.
4. **`_pick_package(app, model)`:** wybór paczki z wyraźnie nazwaną regułą dla 2019 (`packages[0]`, także z `IndexError` przy pustej liście). Dla nowszych modeli: najwyższe `api` mieszczące się w `max_api`, przy remisie pierwsza paczka, `None`, gdy nic się nie mieści.
5. **Budowa wyniku i sortowanie:** jedno stabilne sortowanie po kluczu `(not featured, name.lower())` zamiast list `feat`/`res` i podwójnej pętli. `featured` ustawiane przy tworzeniu elementu jako `bool(...)`.
6. **Nazwy lokalne:** `mdl`, `fw`, `fwn`, `p`, `q`, `r`, `x` zamienione na opisowe (można rozłożyć na poprzednie kroki).

Docelowo główna funkcja ma ok. 15 linii: znajdź model, policz firmware, przefiltruj, wybierz paczkę, posortuj.

## Out of Scope

- Naprawa reguły dla 2019, `IndexError` przy pustych paczkach i kolizji `1.100`. To zmiany zachowania wymagające zmiany testów charakteryzacyjnych (zasada 5 w `CLAUDE.md`). Osobne zadanie, po refaktoryzacji.
- Zmiany w `store.fixture(...)`, kontrakcie API, `tv/` i innych plikach niż `backend/catalog.py` (oraz nowe testy w kroku 0).

## Kryteria akceptacji

- [ ] Żaden istniejący test nie jest zmieniany. Wszystkie przechodzą po każdym commicie.
- [ ] Sygnatura i wynik `get_apps_for_device` bez zmian.
- [ ] `git diff --stat` w commitach refaktoryzacji obejmuje tylko `backend/catalog.py`.
