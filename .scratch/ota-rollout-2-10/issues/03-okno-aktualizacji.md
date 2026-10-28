# 03 — Okno aktualizacji

**What to build:** Aktualizację proponujemy tylko wtedy, gdy urządzenie jest w oknie aktualizacji, i dotyczy to każdego wydania. Muszą być spełnione oba warunki: stan urządzenia (po zapisaniu tego, co zgłosiło przy sprawdzeniu) to `standby`, a jego lokalny czas, czyli bieżący UTC z wstrzykniętego zegara plus `utc_offset_min`, mieści się w przedziale [02:00, 05:00). Przesunięcie bierzemy z zapytania, a gdy go brak, ostatnie zapisane w rejestrze. Gdy nie ma go nigdzie, aktualizacji nie ma. Spec: `.scratch/ota-rollout-2-10/spec.md`.

**Blocked by:** 01 — Wstrzykiwany zegar w usłudze OTA i serwerze

**Status:** ready-for-agent

- [ ] Stan `watching` i `menu` oznacza brak aktualizacji, także w nocy.
- [ ] `standby` o 01:59 i 05:00 czasu lokalnego oznacza brak aktualizacji. O 02:00 i 04:59 aktualizacja jest.
- [ ] Okno jest liczone poprawnie, gdy czas lokalny i UTC wypadają w różnych dobach (np. UTC−5, UTC+9).
- [ ] Brak przesunięcia w zapytaniu oznacza użycie wartości z rejestru. Brak go wszędzie oznacza brak aktualizacji.
- [ ] Istniejące testy OTA i kontraktu API, które oczekują aktualizacji, dostają zegar ustawiony w oknie aktualizacji. Ich asercje zostają bez zmian, a żaden test nie jest usuwany ani osłabiany.
- [ ] Kształt odpowiedzi `/api/ota/check` się nie zmienia.
