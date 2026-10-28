# 02 — Wersja graniczna 2.0.0

**What to build:** Urządzenie, którego firmware jest poniżej wersji granicznej 2.0.0, nie dostaje przy sprawdzeniu żadnej aktualizacji, także wydania 2.0.0 (ADR-0001). Firmware, którego nie da się odczytać jako wersji, traktujemy jak wersję poniżej granicznej. Wersja graniczna to jedna wartość dla całego systemu, a nie pole wydania. Spec: `.scratch/ota-rollout-2-10/spec.md`.

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

- [ ] Urządzenie na 1.9.4 (np. TV-007, `1.9.4-eu`) dostaje brak aktualizacji, nawet gdy w danych są wydania 2.0.0 i 2.9.0.
- [ ] Urządzenie na dokładnie 2.0.0 kwalifikuje się do nowszych wydań.
- [ ] Urządzenie z nieczytelnym firmware'em dostaje brak aktualizacji.
- [ ] Wpis 2.0.0 zostaje w danych wydań bez zmian.
- [ ] Testy przez publiczne sprawdzenie aktualizacji z wydaniami ustawionymi w teście. Istniejące testy przechodzą bez zmian.
