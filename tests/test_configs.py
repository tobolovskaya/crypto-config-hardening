"""The rules must catch every known problem in configs/before and nothing in configs/after."""
from pathlib import Path

import pytest
import yaml

from check_config import check, main

ROOT = Path(__file__).resolve().parent.parent

EXPECTED_BEFORE = {
    "01-critical.yaml": {"JWT-001", "JWT-002", "JWT-004", "JWT-005", "JWT-006", "PWD-001", "ENC-002", "ENC-003"},
    "02-legacy.yaml": {"JWT-003", "JWT-005", "PWD-002", "ENC-001", "ENC-004"},
    "03-subtle.yaml": {"JWT-005", "PWD-003", "PWD-004", "ENC-003"},
}


def rules(path: Path) -> set[str]:
    return {f.rule for f in check(yaml.safe_load(path.read_text()))}


@pytest.mark.parametrize("name,expected", EXPECTED_BEFORE.items())
def test_before_configs_are_caught(name, expected):
    assert rules(ROOT / "configs/before" / name) == expected


@pytest.mark.parametrize("name", EXPECTED_BEFORE)
def test_after_configs_are_clean(name):
    assert rules(ROOT / "configs/after" / name) == set()


def test_every_before_config_has_an_after_config():
    before = {p.name for p in (ROOT / "configs/before").glob("*.yaml")}
    after = {p.name for p in (ROOT / "configs/after").glob("*.yaml")}
    assert before == after == set(EXPECTED_BEFORE)


def test_placeholder_secret_is_not_hardcoded():
    assert rules_of({"jwt": {"shared_secret": "${JWT_SECRET}", "claims": {"exp_required": True}}}) == set()
    assert "JWT-003" in rules_of({"jwt": {"shared_secret": "${JWT_SECRET", "claims": {"exp_required": True}}})


def test_cli_exit_codes(capsys):
    assert main([str(ROOT / "configs/after/01-critical.yaml")]) == 0
    assert main([str(ROOT / "configs/before/01-critical.yaml")]) == 1
    assert main([]) == 2


def rules_of(cfg: dict) -> set[str]:
    return {f.rule for f in check(cfg)}
