#!/usr/bin/env python3
"""Check crypto configuration files (YAML) against a small set of security rules.

Usage:
    python check_config.py configs/after/*.yaml

Exit code 0 when no findings, 1 when there are findings, 2 on a usage or parse error.
Thresholds follow the OWASP Password Storage and JWT cheat sheets and NIST SP 800-131A.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

WEAK_PASSWORD_HASHES = {"md5", "sha1", "sha256", "sha512", "plain", "plaintext"}
BROKEN_CIPHERS = {"des", "3des", "tripledes", "rc4", "blowfish"}
UNAUTHENTICATED_MODES = ("cbc", "ecb", "ctr")
ARGON2_MIN_MEMORY_KIB = 19456  # OWASP minimum: m=19 MiB, t=2, p=1
ARGON2_MIN_TIME = 2
BCRYPT_MIN_COST = 10
RSA_MIN_BITS = 2048


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    cwe: str
    message: str


def _is_placeholder(value) -> bool:
    """A value like ${JWT_SECRET} is injected at runtime and is not a hardcoded secret."""
    return isinstance(value, str) and value.startswith("${") and value.endswith("}")


def check(cfg: dict) -> list[Finding]:
    findings: list[Finding] = []
    add = lambda *a: findings.append(Finding(*a))  # noqa: E731

    jwt = cfg.get("jwt") or {}
    if jwt:
        alg = str(jwt.get("algorithm", "")).lower()
        if alg == "none":
            add("JWT-001", "critical", "CWE-347", "JWT algorithm 'none': tokens are not signed")
        if jwt.get("verify_signature") is False:
            add("JWT-002", "critical", "CWE-347", "JWT signature is not verified")
        secret = jwt.get("shared_secret")
        if secret is not None and not _is_placeholder(secret):
            add("JWT-003", "high", "CWE-798", "JWT secret is hardcoded in the config")
        key_size = jwt.get("key_size")
        if isinstance(key_size, int) and key_size < RSA_MIN_BITS:
            add("JWT-004", "high", "CWE-326", f"JWT key size {key_size} bits, minimum is {RSA_MIN_BITS}")
        claims = jwt.get("claims") or {}
        if not claims.get("exp_required"):
            add("JWT-005", "medium", "CWE-613", "JWT expiry is not required: a stolen token works forever")
        if claims.get("aud_check") is False:
            add("JWT-006", "medium", "CWE-287", "JWT audience is not checked")

    pwd = cfg.get("passwords") or {}
    if pwd:
        fn = str(pwd.get("hash_function", "")).lower()
        if fn in WEAK_PASSWORD_HASHES:
            add("PWD-001", "critical", "CWE-916", f"Password hash '{fn}' is a fast general-purpose hash, not a password hash")
        salt = pwd.get("salt")
        if salt is not None:
            add("PWD-002", "high", "CWE-760", "Fixed salt: equal passwords get equal hashes")
        if fn.startswith("argon2"):
            if fn != "argon2id":
                add("PWD-003", "low", "CWE-916", f"'{fn}' instead of argon2id")
            if (pwd.get("memory_cost") or 0) < ARGON2_MIN_MEMORY_KIB or (pwd.get("time_cost") or 0) < ARGON2_MIN_TIME:
                add("PWD-004", "medium", "CWE-916",
                    f"Argon2 below OWASP minimum (m={ARGON2_MIN_MEMORY_KIB} KiB, t={ARGON2_MIN_TIME})")
        if fn == "bcrypt" and pwd.get("cost_factor") is not None and pwd["cost_factor"] < BCRYPT_MIN_COST:
            add("PWD-005", "medium", "CWE-916", f"bcrypt cost below {BCRYPT_MIN_COST}")

    enc = cfg.get("encryption") or {}
    if enc:
        alg = str(enc.get("algorithm", "")).lower()
        if alg in BROKEN_CIPHERS:
            add("ENC-001", "critical", "CWE-327", f"Broken cipher '{alg}'")
        elif any(mode in alg for mode in UNAUTHENTICATED_MODES):
            add("ENC-002", "medium", "CWE-353", f"'{alg}' has no built-in integrity check, use an AEAD mode (GCM)")
        if str(enc.get("iv_strategy", "")).lower() in {"fixed", "fixed_iv", "static"}:
            add("ENC-003", "high", "CWE-329", "Fixed IV/nonce: repeats leak data, and break GCM entirely")
        if str(enc.get("key_storage", "")).lower() in {"hardcoded", "config", "inline"}:
            add("ENC-004", "high", "CWE-321", "Encryption key is hardcoded")

    return findings


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    total = 0
    for path in map(Path, argv):
        try:
            cfg = yaml.safe_load(path.read_text()) or {}
        except (OSError, yaml.YAMLError) as e:
            print(f"{path}: cannot read: {e}")
            return 2
        findings = check(cfg)
        total += len(findings)
        status = "OK" if not findings else f"{len(findings)} finding(s)"
        print(f"{path}: {status}")
        for f in findings:
            print(f"  {f.rule}  {f.severity:<8} {f.cwe:<8} {f.message}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
