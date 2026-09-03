import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_PATH = ROOT / "src" / "app.py"

spec = importlib.util.spec_from_file_location("app_module", APP_PATH)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)


def test_activities_persist_after_restart(monkeypatch):
    app = app_module.app
    stored = app_module.activities.copy()

    db_path = ROOT / "data" / "activities.json"
    db_path.parent.mkdir(exist_ok=True)
    db_path.write_text(__import__("json").dumps(stored), encoding="utf-8")

    monkeypatch.setattr(app_module, "activities", app_module.load_activities())

    assert app_module.activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    assert app_module.activities["Programming Class"]["participants"] == [
        "emma@mergington.edu",
        "sophia@mergington.edu",
    ]
