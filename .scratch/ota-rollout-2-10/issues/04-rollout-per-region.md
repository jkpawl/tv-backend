# 04 — Rollout wydania per region

**What to build:** Wydanie może mieć opcjonalne pole `rollout`, czyli mapę region → procent 0–100 (np. `{"EU": 10}`). Wydanie bez rolloutu dostają wszystkie urządzenia. W wydaniu z rolloutem region nieobecny w mapie ma 0%. Urządzenie jest objęte rolloutem, gdy jego koszyk rolloutu, czyli stała liczba 0–99 ze stabilnego hasha `id` urządzenia i wersji wydania (nie wbudowany `hash()`), jest mniejszy niż procent dla jego regionu. Urządzenie spoza rolloutu dostaje najwyższe inne wydanie, do którego się kwalifikuje. Spec: `.scratch/ota-rollout-2-10/spec.md`.

**Blocked by:** 03 — Okno aktualizacji (ta sama logika sprawdzenia, a testy muszą działać w oknie aktualizacji)

**Status:** ready-for-agent

- [ ] Rollout 0% dla regionu urządzenia albo region nieobecny w mapie oznacza, że wydanie nie jest proponowane.
- [ ] Rollout 100% oznacza, że wydanie jest proponowane.
- [ ] Urządzenie spoza rolloutu najnowszego wydania dostaje najwyższe wydanie bez rolloutu (np. 2.9.0).
- [ ] Urządzenie objęte rolloutem przy N% jest nim objęte także przy każdym wyższym procencie.
- [ ] Wielokrotne sprawdzenie w tych samych warunkach zawsze daje tę samą odpowiedź, także między restartami procesu.
- [ ] Testy nie wpisują na sztywno wartości koszyków. Wynik weryfikują przez 0%, 100% i monotoniczność procentu.
- [ ] Wydania bez pola `rollout` działają jak dotąd.
