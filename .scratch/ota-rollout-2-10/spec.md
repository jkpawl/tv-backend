# Rollout firmware'u 2.10.1 dla serii Q i X

Status: ready-for-agent

## Problem Statement

Produkt (Kasia Wrona) startuje w poniedziałek 2026-11-02 z firmware'em 2.10.1 dla modeli LM-50Q21, LM-55Q23 i LM-65X25. Backend przy sprawdzeniu aktualizacji proponuje dziś każdemu urządzeniu najwyższe pasujące wydanie, niezależnie od pory, od tego, co urządzenie robi, i od tego, czy aktualizacja ma trafić tylko do części urządzeń. Telewizory w terenie instalują zaproponowaną aktualizację natychmiast, z banerem na ekranie, a ich kodu nie da się zmienić. Wszystkie decyzje „czy teraz zaktualizować” musi więc podejmować serwer.

Brakuje trzech rzeczy:

- nie da się wypuścić wydania na część urządzeń w jednym regionie (10% EU, potem więcej),
- aktualizacja może przerwać oglądanie,
- urządzenia z firmware'em sprzed zmiany partycji (poniżej 2.0.0) dostają aktualizacje, których nie powinny.

## Solution

Sprawdzenie aktualizacji zyskuje trzy nowe warunki. Wszystkie obowiązują dla każdego wydania.

1. **Wersja graniczna**: urządzenie z firmware'em poniżej 2.0.0 nie dostaje żadnej aktualizacji (ADR-0001).
2. **Okno aktualizacji**: aktualizację proponujemy tylko urządzeniu w stanie `standby`, gdy jego lokalny czas mieści się w przedziale 02:00–05:00.
3. **Rollout**: wydanie może mieć rollout, czyli procent urządzeń dla każdego regionu. Urządzenie jest nim objęte, gdy jego koszyk rolloutu (stały, wyliczony z `id` urządzenia i wersji wydania) jest mniejszy niż procent dla jego regionu. Urządzenie spoza rolloutu danego wydania dostaje najwyższe inne wydanie, do którego się kwalifikuje.

Wydanie 2.10.1 trafia do danych wydań w poniedziałek z rolloutem EU 10% i 0% dla pozostałych regionów. Kolejne podbicia procentu to zmiana w danych wydań, commit i wdrożenie.

## User Stories

1. As a product manager, I want 2.10.1 to reach only 10% of EU devices at launch, so that a defect affects few customers.
2. As a product manager, I want NA and APAC devices to receive no 2.10.1 at launch, so that the EU goes first.
3. As a product manager, I want to raise the rollout percentage per region later, so that I can widen the release once it proves stable.
4. As a product manager, I want devices already in the rollout to stay in it when the percentage grows, so that nobody gets offered the release and then loses it.
5. As a product manager, I want the first group to differ between releases, so that the same customers are not always the early adopters.
6. As a release engineer, I want raising the percentage to be a one-line change in the release data with a commit, so that git history shows who widened the rollout and when.
7. As a release engineer, I want releases without a rollout to behave as today (all devices), so that existing releases keep working.
8. As a release engineer, I want a region missing from a release's rollout to mean 0%, so that a forgotten region is never released by accident.
9. As a customer watching TV, I want no update to start while I'm watching, so that my show is not interrupted.
10. As a customer browsing the menu, I want no update banner and download, so that I can use the TV undisturbed.
11. As a customer, I want updates to install at night while the TV is in standby, so that I don't notice them.
12. As a customer in any timezone, I want "night" to mean my local night, so that the update doesn't hit my evening.
13. As an operator, I want a device that reports no UTC offset to fall back to the offset last stored in the registry, so that a missing field doesn't block updates.
14. As an operator, I want a device with no known offset at all to get no update, so that we never guess the customer's time.
15. As an operator, I want devices below 2.0.0 to get no update at all, so that no device is moved across the partition change by the backend (ADR-0001).
16. As an operator, I want a device whose firmware can't be parsed to get no update, so that malformed reports are handled safely.
17. As a customer with an EU device outside the 2.10.1 rollout, I want to still get the newest release that has no rollout (e.g. 2.9.0), so that I keep receiving fixes during the rollout.
18. As a customer whose device enters the rollout, I want to be offered 2.10.1 directly, so that I don't install intermediate releases.
19. As a customer on 2.10.1, I want no further offer of 2.10.1, so that the TV doesn't reinstall it.
20. As a customer with an S-series TV, I want no 2.10.1 offer, so that I don't get firmware not built for my model.
21. As a TV already in the field, I want the check and download responses to keep their shape, so that my frozen client keeps working.
22. As a TV checking every 5 seconds, I want the same answer on every check under the same conditions, so that I don't flip between "update" and "no update".
23. As a developer, I want to inject the clock into the OTA service and the server, so that the update window is testable without waiting for the night.

## Implementation Decisions

- **Version 2.10.1.** The release is written as `2.10.1` with builds `2.10.1` (NA, APAC) and `2.10.1-eu` (EU), for models LM-50Q21, LM-55Q23, LM-65X25. Versions are compared numerically as three numbers. Size and release notes come from product. The entry lands on Monday 2026-11-02 as a separate commit.
- **Release data shape.** A release gains an optional `rollout` field: a map from region to an integer percentage 0–100, e.g. `{"EU": 10}`. Release without `rollout` → every device. Release with `rollout` → region missing from the map has 0%. 2.10.1 starts with `{"EU": 10}`.
- **Rollout bucket.** A stable integer 0–99 derived from the device `id` and release version through a stable hash (e.g. SHA-256 of both, modulo 100). Python's built-in `hash()` must not be used, because it is randomised between processes. Device is in the rollout when `bucket < percentage`.
- **Version floor.** A single system-wide value 2.0.0, defined in the OTA module rather than per release. Device whose current firmware is below it (including unparsable firmware, which parses to 0.0.0) gets `None`. The 2.0.0 release entry stays in the data and is simply never offered (ADR-0001).
- **Update window.** An update is offered only when both hold: (1) the device state, after the check's report is applied, is `standby`; (2) the device's local time, i.e. current UTC plus `utc_offset_min` (from the request, otherwise the value stored in the registry), is in [02:00, 05:00). No known offset → `None`. Applies to every release.
- **Selection order.** Report what the device sent (as today). Then return `None` if the device is below the version floor or outside the update window. Otherwise pick the highest release that matches model, has a build for the region, is newer than the current firmware and includes the device in its rollout.
- **Clock seam.** `OtaService` takes an optional clock (callable returning the current UTC time, defaulting to real time). `Api` and `make_server` accept and pass it through, so the server can be tested at a chosen time.
- **API contract unchanged.** `/api/ota/check` and `/api/ota/download` keep their request and response shapes. Download is not blocked for devices outside a rollout: the TV only downloads builds the check offered.
- **Nothing changes in the TV client.**

## Testing Decisions

- A good test drives the public seam with a device, a release list and a time, and asserts only the offered update (or `None`). It does not test the hash function, bucket values or private helpers directly. Rollout tests pick devices or percentages whose outcome is known (0% and 100%, plus "a device in at N% is still in at a higher percentage"). Bucket numbers are never hard-coded.
- **Primary seam:** `OtaService.check(device_id, firmware, state, utc_offset_min)` with releases set through `set_fixture` and an injected clock, as in the existing OTA tests.
- **Contract:** the existing API contract tests stay as the HTTP-level check. They get an injected clock in the window.
- **Existing tests:** the current OTA and contract tests that expect an update (offers newer release, picks the highest version, respects region builds, check with update) currently pass at any time of day. They are changed only to run with a clock inside the update window. Their assertions stay as they are. This is an intended change of behaviour, not a refactoring, and does not weaken those tests.
- **New cases to cover:** below the floor (1.9.4) → none, including when 2.0.0 is in the data; exactly 2.0.0 → eligible; unparsable firmware → none; `watching` and `menu` → none; standby at 01:59 / 02:00 / 04:59 / 05:00 local; window computed from offset across midnight UTC; missing offset falls back to the registry value; rollout 0% / 100% / region missing; device outside rollout gets the next-best release without rollout; stickiness when the percentage grows; 2.10.1 newer than 2.9.0 (two-digit minor).
- The fixture tests already check that every release version is well formed and every model exists. The 2.10.1 entry must pass them.

## Out of Scope

- Any change in the TV client.
- Moving devices below 2.0.0 through 2.0.0 (rejected, ADR-0001).
- A runtime control or MCP tool for changing rollout percentages without a deploy.
- A scheduled start date in the data (the entry is simply merged on Monday).
- Blocking downloads of builds outside the rollout.
- Rollout analytics or reporting on how many devices updated.

## Further Notes

- Effect on the simulator demo: `http://localhost:8765/tv/` shows an update only when the device is in standby and its local time is 02:00–05:00. During a daytime demo, no update will appear.
- Devices that are unplugged at night never fall in the update window, and the first 10% of EU will spread over several nights.
- Product asked for devices below 2.0 to "first move to 2.0". This was deliberately rejected (ADR-0001). Product should be told.
- Glossary terms used here (Urządzenie, Region, Stan urządzenia, Okno aktualizacji, Wersja graniczna, Wydanie, Build, Rollout, Koszyk rolloutu) are defined in `CONTEXT.md`.
