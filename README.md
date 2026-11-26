# Crypto config hardening: before and after

[![Crypto config check](https://github.com/tobolovskaya/crypto-config-hardening/actions/workflows/crypto-config.yml/badge.svg)](https://github.com/tobolovskaya/crypto-config-hardening/actions/workflows/crypto-config.yml)

> 🇳🇴 **Kort på norsk:** Tre usikre kryptokonfigurasjoner (JWT, passordhashing, kryptering) og en herdet versjon av hver. Et lite Python-skript sjekker reglene i GitHub Actions: de herdede må bestå, de usikre må bli fanget.

Three insecure crypto configurations and a hardened version of each. A small rule checker ([`check_config.py`](check_config.py)) runs in CI in both directions:

- **`configs/after/` must be clean.** Any finding fails the pipeline.
- **`configs/before/` must be caught.** If the checker stops finding problems there, the pipeline fails. This proves the rules actually work.

**Skills shown:** JWT security · password hashing (Argon2id, bcrypt) · authenticated encryption (AES-GCM) · secret management · CWE mapping · Python · pytest · GitHub Actions

## Before and after

### 01-critical: almost every control switched off

| Setting | Before | After | Rule | CWE |
|---|---|---|---|---|
| `jwt.algorithm` | `none` | `RS256` | JWT-001 | CWE-347 |
| `jwt.verify_signature` | `false` | `true` | JWT-002 | CWE-347 |
| `jwt.key_size` | `1024` | `2048` | JWT-004 | CWE-326 |
| `jwt.claims.exp_required` | `false` | `true`, 15 min | JWT-005 | CWE-613 |
| `jwt.claims.aud_check` | `false` | `true` | JWT-006 | CWE-287 |
| `passwords.hash_function` | `sha1` | `argon2id` (m=19 MiB, t=2) | PWD-001 | CWE-916 |
| `encryption.algorithm` | `AES-CBC` | `AES-256-GCM` | ENC-002 | CWE-353 |
| `encryption.iv_strategy` | `fixed_iv` | `random_nonce` | ENC-003 | CWE-329 |

### 02-legacy: secrets in the file and a 1970s cipher

| Setting | Before | After | Rule | CWE |
|---|---|---|---|---|
| `jwt.shared_secret` | `"hardcoded-secret"` | `"${JWT_SECRET}"` from the environment | JWT-003 | CWE-798 |
| `jwt.claims` | missing | `exp_required: true`, 15 min | JWT-005 | CWE-613 |
| `passwords.salt` | `fixed_salt` | removed, bcrypt makes a unique salt per hash | PWD-002 | CWE-760 |
| `encryption.algorithm` | `DES` | `AES-256-GCM` | ENC-001 | CWE-327 |
| `encryption.key_storage` | `hardcoded` | `kms` with envelope encryption | ENC-004 | CWE-321 |

### 03-subtle: looks right, is not

| Setting | Before | After | Rule | CWE |
|---|---|---|---|---|
| `jwt.claims` | missing | expiry, audience, issuer checked | JWT-005 | CWE-613 |
| `passwords.hash_function` | `argon2` | `argon2id` | PWD-003 | CWE-916 |
| `passwords.memory_cost` / `time_cost` | `1024` KiB / `1` | `19456` KiB / `2` | PWD-004 | CWE-916 |
| `encryption.iv_strategy` | `fixed_iv` with AES-GCM | `random_nonce` | ENC-003 | CWE-329 |

AES-GCM is a good choice, which is why this one is easy to miss. With a repeated nonce, GCM leaks the XOR of the plaintexts and lets an attacker forge messages.

**17 findings in total, all fixed.** Each one is a rule in the checker, so the same review runs again on every change.

## Rules

| Rule | Severity | What it checks | Source of the threshold |
|---|---|---|---|
| JWT-001 | critical | `algorithm: none` | OWASP JWT Cheat Sheet |
| JWT-002 | critical | signature verification off | OWASP JWT Cheat Sheet |
| JWT-003 | high | secret not taken from `${ENV}` | CWE-798 |
| JWT-004 | high | RSA key under 2048 bits | NIST SP 800-131A |
| JWT-005 | medium | expiry not required | OWASP JWT Cheat Sheet |
| JWT-006 | medium | audience check off | RFC 7519 |
| PWD-001 | critical | MD5/SHA-x for passwords | OWASP Password Storage |
| PWD-002 | high | fixed salt | OWASP Password Storage |
| PWD-003 | low | Argon2 variant other than `argon2id` | OWASP Password Storage |
| PWD-004 | medium | Argon2 below m=19456 KiB, t=2 | OWASP Password Storage |
| PWD-005 | medium | bcrypt cost under 10 | OWASP Password Storage |
| ENC-001 | critical | DES, 3DES, RC4, Blowfish | NIST SP 800-131A |
| ENC-002 | medium | mode without integrity (CBC, ECB, CTR) | prefer AEAD (GCM) |
| ENC-003 | high | fixed IV/nonce | NIST SP 800-38D |
| ENC-004 | high | key hardcoded in the config | CWE-321 |

## How to run locally

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python check_config.py configs/before/*.yaml   # 17 findings, exit code 1
.venv/bin/python check_config.py configs/after/*.yaml    # clean, exit code 0
.venv/bin/python -m pytest -q
```

## Hva jeg lærte / What I learned

- **A review written as code can be repeated.** My first review was a written report. Turning it into 15 rules means every change to a config is checked the same way.
- **A good algorithm can still be used wrong.** AES-GCM and Argon2 were already in 03-subtle, but a fixed nonce and weak parameters undid them.
- **Test the test.** The pipeline fails if the insecure configs stop producing findings, so a broken rule cannot hide.

---

Originally built as coursework during my MSc in Computer Science (Woolf / GoIT Neoversity), then turned into a checked, tested lab.

**Yevheniia Tobolovska** · IT operations and security · [Portfolio](https://tobolovska.no) · [LinkedIn](https://www.linkedin.com/in/yevheniia-tobolovska)

License: [MIT](LICENSE)
