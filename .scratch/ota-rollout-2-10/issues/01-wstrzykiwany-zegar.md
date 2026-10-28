# 01 — Wstrzykiwany zegar w usłudze OTA i serwerze (prefaktoryzacja)

**What to build:** Usługa OTA, `Api` i `make_server` przyjmują opcjonalny zegar zwracający bieżący czas UTC (domyślnie czas rzeczywisty) i przekazują go do usługi OTA. Zachowanie się nie zmienia. To przygotowanie pod okno aktualizacji (03), które bez zegara jest nietestowalne. Spec: `.scratch/ota-rollout-2-10/spec.md`.

**Blocked by:** None — can start immediately

**Status:** ready-for-agent

- [ ] Usługę OTA można utworzyć z zegarem i bez niego. Bez zegara używa czasu rzeczywistego UTC.
- [ ] `Api` i `make_server` przyjmują ten sam opcjonalny zegar i przekazują go do usługi OTA.
- [ ] To refaktoryzacja: żaden istniejący test nie jest zmieniany, wszystkie przechodzą.
- [ ] Nic w `tv/` się nie zmienia, a `backend/` nie importuje niczego z `mcp_server/`.
