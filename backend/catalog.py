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


def get_apps_for_device(store, device, include_hidden=False):
    apps = store.fixture("apps")
    mdl = _find_model(store.fixture("models"), device["model"])
    if mdl is None:
        return []
    fwn = _version_number(device.get("firmware", "0.0"))
    res = []
    feat = []
    for a in apps:
        if not _is_available(a, device, fwn, include_hidden):
            continue
        pkg = None
        if mdl.get("year") == 2019:
            pkg = a["packages"][0]
        else:
            for x in a["packages"]:
                if x["api"] <= mdl.get("max_api", 0):
                    if pkg == None or x["api"] > pkg["api"]:
                        pkg = x
        if pkg == None:
            continue
        item = {
            "id": a["id"],
            "name": a["name"],
            "color": a.get("color", "#444444"),
            "version": pkg["version"],
            "api": pkg["api"],
        }
        if a.get("featured"):
            feat.append(item)
        else:
            res.append(item)
    feat.sort(key=lambda i: i["name"].lower())
    res.sort(key=lambda i: i["name"].lower())
    out = []
    for i in feat:
        i["featured"] = True
        out.append(i)
    for i in res:
        i["featured"] = False
        out.append(i)
    return out
