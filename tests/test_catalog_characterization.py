"""Characterization tests: pin down what get_apps_for_device returns today.

Expectations were captured from the current implementation, not from a spec.
If one of these fails after a change, the catalog's behaviour changed.
"""

from backend.catalog import get_apps_for_device
from backend.registry import DeviceRegistry
from tests.support import StoreTestCase


def summary(apps):
    return [(a["id"], a["version"], a["api"], a["featured"]) for a in apps]


def ids(apps):
    return [a["id"] for a in apps]


class FixtureDevicesTest(StoreTestCase):
    """Full output for every device in fixtures/devices.json."""

    def apps_for(self, device_id):
        return summary(get_apps_for_device(self.store, DeviceRegistry(self.store).get(device_id)))

    def test_tv_001_q23_na_2_8(self):
        self.assertEqual(self.apps_for("TV-001"), [
            ("kidsclub", "2.2.0", 5, True),
            ("streamly", "6.1.0", 7, True),
            ("fithome", "1.5.1", 7, False),
            ("gallery", "2.0.0", 6, False),
            ("news24", "3.0.2", 6, False),
            ("weather", "3.3.3", 3, False),
            ("sportlive", "8.0.1", 7, False),
        ])

    def test_tv_002_s19_na_2_8(self):
        self.assertEqual(self.apps_for("TV-002"), [
            ("kidsclub", "2.0.0", 3, True),
            ("streamly", "4.2.1", 3, True),
            ("fithome", "1.0.4", 3, False),
            ("gallery", "1.1.0", 3, False),
            ("news24", "1.9.0", 3, False),
            ("weather", "3.3.3", 3, False),
            ("sportlive", "7.1.0", 5, False),
        ])

    def test_tv_003_x25_eu_2_8_suffixed(self):
        self.assertEqual(self.apps_for("TV-003"), [
            ("kidsclub", "3.0.0", 8, True),
            ("kinonet", "2.7.4", 6, True),
            ("streamly", "6.1.0", 7, True),
            ("fithome", "1.5.1", 7, False),
            ("gallery", "2.0.0", 6, False),
            ("news24", "3.0.2", 6, False),
            ("weather", "3.3.3", 3, False),
            ("radiowave", "1.4.0", 5, False),
        ])

    def test_tv_004_q21_apac_2_9(self):
        self.assertEqual(self.apps_for("TV-004"), [
            ("kidsclub", "2.2.0", 5, True),
            ("streamly", "5.0.3", 5, True),
            ("gallery", "2.0.0", 6, False),
            ("musicbox", "0.9.2", 5, False),
            ("news24", "3.0.2", 6, False),
            ("weather", "3.3.3", 3, False),
            ("radiowave", "1.4.0", 5, False),
        ])

    def test_tv_005_s19_eu_2_8_suffixed(self):
        self.assertEqual(self.apps_for("TV-005"), [
            ("kidsclub", "2.0.0", 3, True),
            ("kinonet", "2.3.0", 5, True),
            ("streamly", "4.2.1", 3, True),
            ("fithome", "1.0.4", 3, False),
            ("gallery", "1.1.0", 3, False),
            ("news24", "1.9.0", 3, False),
            ("weather", "3.3.3", 3, False),
            ("radiowave", "1.0.8", 3, False),
        ])

    def test_tv_006_q23_eu_2_9_suffixed(self):
        self.assertEqual(self.apps_for("TV-006"), [
            ("kidsclub", "2.2.0", 5, True),
            ("kinonet", "2.7.4", 6, True),
            ("streamly", "6.1.0", 7, True),
            ("fithome", "1.5.1", 7, False),
            ("gallery", "2.0.0", 6, False),
            ("musicbox", "1.0.0", 7, False),
            ("news24", "3.0.2", 6, False),
            ("weather", "3.3.3", 3, False),
            ("radiowave", "1.4.0", 5, False),
        ])

    def test_tv_007_q21_eu_1_9_gets_nothing(self):
        self.assertEqual(self.apps_for("TV-007"), [])


class RegionTest(StoreTestCase):
    def device(self, **overrides):
        device = {"id": "X", "model": "LM-55Q23", "region": "EU", "firmware": "2.9.0"}
        device.update(overrides)
        return device

    def test_unknown_region_gets_only_wildcard_apps(self):
        apps = get_apps_for_device(self.store, self.device(region="LATAM"))
        self.assertEqual(ids(apps), ["kidsclub", "streamly", "gallery", "musicbox", "news24", "weather"])

    def test_missing_region_gets_only_wildcard_apps(self):
        device = self.device()
        del device["region"]
        apps = get_apps_for_device(self.store, device)
        self.assertEqual(ids(apps), ["kidsclub", "streamly", "gallery", "musicbox", "news24", "weather"])

    def test_na_gets_na_only_apps(self):
        apps = get_apps_for_device(self.store, self.device(region="NA"))
        self.assertEqual(ids(apps), ["kidsclub", "streamly", "fithome", "gallery", "musicbox", "news24", "weather", "sportlive"])

    def test_app_without_regions_is_never_shown(self):
        self.set_fixture("apps", [
            {"id": "noreg", "name": "NoReg", "min_firmware": "2.0", "packages": [{"api": 3, "version": "1.0"}]},
        ])
        self.assertEqual(get_apps_for_device(self.store, self.device()), [])


class FirmwareTest(StoreTestCase):
    def device(self, firmware):
        device = {"id": "X", "model": "LM-55Q23", "region": "EU"}
        if firmware is not None:
            device["firmware"] = firmware
        return device

    def test_min_firmware_is_inclusive(self):
        apps = get_apps_for_device(self.store, self.device("2.4"))
        self.assertIn("kinonet", ids(apps))

    def test_just_below_min_firmware_excludes_app(self):
        apps = get_apps_for_device(self.store, self.device("2.3.9"))
        self.assertEqual(ids(apps), ["streamly", "gallery", "news24", "weather", "radiowave"])

    def test_patch_and_suffix_are_ignored(self):
        plain = get_apps_for_device(self.store, self.device("2.9"))
        self.assertEqual(get_apps_for_device(self.store, self.device("2.9.7-eu")), plain)

    def test_missing_firmware_gets_nothing(self):
        self.assertEqual(get_apps_for_device(self.store, self.device(None)), [])

    def test_unparsable_firmware_gets_nothing(self):
        self.assertEqual(get_apps_for_device(self.store, self.device("abc")), [])

    def test_minor_is_not_zero_padded(self):
        # "1.100" is treated as 1*100 + 100 == 2.0
        self.set_fixture("apps", [
            {"id": "a", "name": "A", "regions": ["*"], "min_firmware": "2.0", "packages": [{"api": 3, "version": "1.0"}]},
        ])
        self.assertEqual(ids(get_apps_for_device(self.store, self.device("1.100"))), ["a"])

    def test_none_firmware_raises(self):
        with self.assertRaises(AttributeError):
            get_apps_for_device(self.store, {"id": "X", "model": "LM-55Q23", "region": "EU", "firmware": None})

    def test_unparsable_min_firmware_means_no_minimum(self):
        self.set_fixture("apps", [
            {"id": "a", "name": "A", "regions": ["*"], "min_firmware": "x", "packages": [{"api": 3, "version": "1.0"}]},
        ])
        self.assertEqual(ids(get_apps_for_device(self.store, self.device("abc"))), ["a"])


class PackageSelectionTest(StoreTestCase):
    def device(self, model):
        return {"id": "X", "model": model, "region": "NA", "firmware": "3.0"}

    def test_newer_models_pick_highest_api_within_max_api(self):
        apps = get_apps_for_device(self.store, self.device("LM-65X25"))
        self.assertEqual(summary(apps), [
            ("kidsclub", "3.0.0", 8, True),
            ("streamly", "6.1.0", 7, True),
            ("fithome", "1.5.1", 7, False),
            ("gallery", "2.0.0", 6, False),
            ("musicbox", "1.0.0", 7, False),
            ("news24", "3.0.2", 6, False),
            ("weather", "3.3.3", 3, False),
            ("sportlive", "8.0.1", 7, False),
        ])

    def test_2019_models_always_take_first_package(self):
        # streamly has api 5 available, yet a 2019 model (max_api 5) gets the api 3 package.
        apps = get_apps_for_device(self.store, self.device("LM-43S19"))
        self.assertEqual(summary(apps), [
            ("kidsclub", "2.0.0", 3, True),
            ("streamly", "4.2.1", 3, True),
            ("fithome", "1.0.4", 3, False),
            ("gallery", "1.1.0", 3, False),
            ("musicbox", "0.9.2", 5, False),
            ("news24", "1.9.0", 3, False),
            ("weather", "3.3.3", 3, False),
            ("sportlive", "7.1.0", 5, False),
        ])

    def test_2019_models_ignore_max_api(self):
        self.set_fixture("apps", [
            {"id": "a", "name": "A", "regions": ["*"], "min_firmware": "2.0", "packages": [{"api": 9, "version": "9.0"}]},
        ])
        apps = get_apps_for_device(self.store, self.device("LM-43S19"))
        self.assertEqual(summary(apps), [("a", "9.0", 9, False)])

    def test_newer_models_drop_app_without_fitting_package(self):
        self.set_fixture("apps", [
            {"id": "a", "name": "A", "regions": ["*"], "min_firmware": "2.0", "packages": [{"api": 9, "version": "9.0"}]},
        ])
        self.assertEqual(get_apps_for_device(self.store, self.device("LM-65X25")), [])

    def test_2019_model_with_no_packages_raises(self):
        self.set_fixture("apps", [
            {"id": "a", "name": "A", "regions": ["*"], "min_firmware": "2.0", "packages": []},
        ])
        with self.assertRaises(IndexError):
            get_apps_for_device(self.store, self.device("LM-43S19"))

    def test_api_tie_picks_first_package(self):
        self.set_fixture("apps", [
            {"id": "a", "name": "A", "regions": ["*"], "min_firmware": "2.0",
             "packages": [{"api": 5, "version": "first"}, {"api": 5, "version": "second"}]},
        ])
        apps = get_apps_for_device(self.store, self.device("LM-65X25"))
        self.assertEqual(summary(apps), [("a", "first", 5, False)])

    def test_model_without_max_api_gets_nothing(self):
        self.set_fixture("models", [{"model": "LM-T", "year": 2024}])
        self.assertEqual(get_apps_for_device(self.store, self.device("LM-T")), [])

    def test_duplicate_model_last_entry_wins(self):
        self.set_fixture("models", [
            {"model": "LM-D", "year": 2024, "max_api": 8},
            {"model": "LM-D", "year": 2024, "max_api": 3},
        ])
        apps = get_apps_for_device(self.store, self.device("LM-D"))
        self.assertEqual({a["api"] for a in apps}, {3})


class VisibilityAndOrderTest(StoreTestCase):
    def device(self):
        return {"id": "X", "model": "LM-55Q23", "region": "EU", "firmware": "2.9.0"}

    def test_hidden_apps_shown_only_on_request(self):
        self.assertNotIn("diagnostics", ids(get_apps_for_device(self.store, self.device())))
        apps = get_apps_for_device(self.store, self.device(), include_hidden=True)
        self.assertEqual(summary(apps)[-1], ("diagnostics", "0.9.0", 3, False))

    def test_featured_first_then_case_insensitive_name_order(self):
        self.set_fixture("apps", [
            {"id": n.lower(), "name": n, "regions": ["*"], "min_firmware": "2.0", "featured": f,
             "packages": [{"api": 3, "version": "1.0"}]}
            for n, f in [("beta", False), ("Alpha", False), ("zeta", True), ("Delta", True)]
        ])
        apps = get_apps_for_device(self.store, self.device())
        self.assertEqual([(a["name"], a["featured"]) for a in apps],
                         [("Delta", True), ("zeta", True), ("Alpha", False), ("beta", False)])

    def test_featured_is_normalized_to_bool(self):
        self.set_fixture("apps", [
            {"id": "a", "name": "A", "regions": ["*"], "min_firmware": "2.0", "featured": 1,
             "packages": [{"api": 3, "version": "1.0"}]},
            {"id": "b", "name": "B", "regions": ["*"], "min_firmware": "2.0", "featured": 0,
             "packages": [{"api": 3, "version": "1.0"}]},
        ])
        apps = get_apps_for_device(self.store, self.device())
        self.assertEqual([(a["id"], a["featured"]) for a in apps], [("a", True), ("b", False)])
        self.assertIs(apps[0]["featured"], True)
        self.assertIs(apps[1]["featured"], False)

    def test_default_color(self):
        self.set_fixture("apps", [
            {"id": "a", "name": "A", "regions": ["*"], "min_firmware": "2.0", "packages": [{"api": 3, "version": "1.0"}]},
        ])
        self.assertEqual(get_apps_for_device(self.store, self.device())[0]["color"], "#444444")
