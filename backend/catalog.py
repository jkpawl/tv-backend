"""App catalog: which apps a given TV shows on its home screen."""


def _version_number(text):
    """"2.9.0" -> 209: major*100 + minor, patch ignored, 0 when unparsable."""
    try:
        parts = text.split(".")
        return int(parts[0]) * 100 + int(parts[1])
    except (ValueError, IndexError):
        return 0


def _find_model(models, name):
    """The model entry called ``name``; the last one wins if listed twice."""
    for model in reversed(models):
        if model["model"] == name:
            return model
    return None


def _is_available(app, device, firmware, include_hidden):
    """Whether ``app`` may be shown on ``device`` running ``firmware`` (a version number)."""
    if app.get("hidden") and not include_hidden:
        return False
    regions = app.get("regions", [])
    if "*" not in regions and device.get("region") not in regions:
        return False
    return firmware >= _version_number(app.get("min_firmware", "0.0"))


def _pick_package(app, model):
    """The package to install on ``model``, or None if none fits.

    2019 models always get the first package, regardless of ``max_api``.
    Newer models get the highest api within ``max_api``; on a tie, the first one.
    """
    if model.get("year") == 2019:
        return app["packages"][0]
    max_api = model.get("max_api", 0)
    best = None
    for package in app["packages"]:
        if package["api"] <= max_api and (best is None or package["api"] > best["api"]):
            best = package
    return best


def get_apps_for_device(store, device, include_hidden=False):
    apps = store.fixture("apps")
    model = _find_model(store.fixture("models"), device["model"])
    if model is None:
        return []
    firmware = _version_number(device.get("firmware", "0.0"))
    result = []
    for app in apps:
        if not _is_available(app, device, firmware, include_hidden):
            continue
        package = _pick_package(app, model)
        if package is None:
            continue
        result.append({
            "id": app["id"],
            "name": app["name"],
            "color": app.get("color", "#444444"),
            "version": package["version"],
            "api": package["api"],
            "featured": bool(app.get("featured")),
        })
    # Featured first, then by name; the sort is stable, so ties keep catalog order.
    result.sort(key=lambda item: (not item["featured"], item["name"].lower()))
    return result
