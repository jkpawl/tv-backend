# Brak aktualizacji poniżej wersji granicznej 2.0.0

Urządzenia z firmware'em poniżej 2.0.0 (sprzed zmiany układu partycji) nie dostają żadnej aktualizacji, w tym wydania 2.0.0. Decyzję podjęto świadomie, wbrew pierwotnej prośbie produktu, żeby urządzenia „najpierw przechodziły na 2.0”. Backend nie prowadzi więc żadnej ścieżki aktualizacji przez zmianę partycji.

## Konsekwencje

- Wpis 2.0.0 zostaje w danych wydań, ale backend nie proponuje go żadnemu urządzeniu. To nie jest błąd i nie należy go „naprawiać”.
- Urządzenia poniżej 2.0.0 (np. TV-007 z `1.9.4-eu`) zostają na swojej wersji, dopóki ta decyzja nie zostanie zmieniona.
- Firmware, którego nie da się odczytać jako wersji, traktujemy jak wersję poniżej granicznej, więc takie urządzenie też nie dostaje aktualizacji.
