# 05 — Wpis wydania 2.10.1 (merge 2026-11-02)

**What to build:** Dane wydań zawierają wydanie 2.10.1 dla modeli LM-50Q21, LM-55Q23 i LM-65X25, z buildami `2.10.1` (NA, APAC) i `2.10.1-eu` (EU) oraz rolloutem `{"EU": 10}`. Na start urządzenia z EU objęte 10% dostają 2.10.1 w oknie aktualizacji, a NA i APAC nie dostają go wcale. Wpis trafia do `main` w poniedziałek 2026-11-02. Spec: `.scratch/ota-rollout-2-10/spec.md`.

**Blocked by:** 02 — Wersja graniczna 2.0.0; 03 — Okno aktualizacji; 04 — Rollout wydania per region

**Status:** ready-for-agent

- [ ] Rozmiar wydania (`size_bytes`) i opis zmian pochodzą od produktu (Kasia Wrona). Bez nich ticket nie jest gotowy do merge'a.
- [ ] Testy danych wydań przechodzą (poprawny format wersji, istniejące modele).
- [ ] Wersja 2.10.1 jest traktowana jako nowsza niż 2.9.0 (dwucyfrowy numer minor).
- [ ] Urządzenie z serii S nie dostaje 2.10.1.
- [ ] Urządzenie z NA ani APAC nie dostaje 2.10.1.
- [ ] Commit zawiera tylko zmianę danych wydań (`git diff --stat`).
