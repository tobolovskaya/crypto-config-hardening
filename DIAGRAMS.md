# 📊 Візуальні діаграми проєкту

## Структура безпеки криптографічної конфігурації

```mermaid
graph TB
    subgraph "🔐 JWT Authentication"
        JWT[JWT Token]
        JWT --> ALG[Algorithm: RS256]
        JWT --> VER[Verify Signature: true]
        JWT --> EXP[Expiration: 900s]
        JWT --> CLAIMS[Claims Validation]
        CLAIMS --> AUD[Audience Check]
        CLAIMS --> ISS[Issuer Check]
        CLAIMS --> NBF[Not Before Check]
    end
    
    subgraph "🔑 Password Security"
        PWD[User Password]
        PWD --> HASH[Argon2id Hash]
        HASH --> TIME[Time Cost: 2]
        HASH --> MEM[Memory: 19 MiB]
        HASH --> SALT[Random Salt]
        HASH --> PEPPER[Pepper Secret]
    end
    
    subgraph "🛡️ Data Encryption"
        DATA[Sensitive Data]
        DATA --> AES[AES-256-GCM]
        AES --> KEY[256-bit Key]
        AES --> NONCE[Random Nonce]
        AES --> AAD[Auth Data]
        KEY --> HSM[HSM Storage]
    end
    
    subgraph "🌐 Transport Security"
        TLS[TLS 1.3]
        TLS --> HSTS[HSTS Enabled]
        TLS --> CERT[Certificate]
        TLS --> CIPHER[Modern Ciphers]
    end
    
    JWT --> TLS
    PWD --> TLS
    DATA --> TLS
    
    style JWT fill:#e1f5e1
    style PWD fill:#e1f5e1
    style DATA fill:#e1f5e1
    style TLS fill:#e1f5e1
```

---

## Порівняння рівнів безпеки конфігурацій

```mermaid
graph LR
    subgraph "❌ WE Config - 0/10"
        WE1[algorithm: none]
        WE2[verify: false]
        WE3[SHA-1]
        WE4[fixed IV]
    end
    
    subgraph "⚠️ LE Config - 4/10"
        LE1[HS256]
        LE2[hardcoded secret]
        LE3[bcrypt]
        LE4[DES]
    end
    
    subgraph "⚡ MI Config - 7/10"
        MI1[RS256]
        MI2[Argon2]
        MI3[AES-GCM]
        MI4[fixed IV ⚠️]
    end
    
    subgraph "✅ Secure Config - 10/10"
        SC1[RS256 + JWKS]
        SC2[Argon2id optimized]
        SC3[AES-256-GCM]
        SC4[Random Nonce]
        SC5[HSM Storage]
    end
    
    WE1 -.upgrade.-> LE1
    LE1 -.upgrade.-> MI1
    MI1 -.upgrade.-> SC1
    
    style WE1 fill:#ffcccc
    style WE2 fill:#ffcccc
    style WE3 fill:#ffcccc
    style WE4 fill:#ffcccc
    style LE1 fill:#fff4cc
    style LE2 fill:#fff4cc
    style LE3 fill:#fff4cc
    style LE4 fill:#fff4cc
    style MI1 fill:#ccf2ff
    style MI2 fill:#ccf2ff
    style MI3 fill:#ccf2ff
    style MI4 fill:#fff4cc
    style SC1 fill:#ccffcc
    style SC2 fill:#ccffcc
    style SC3 fill:#ccffcc
    style SC4 fill:#ccffcc
    style SC5 fill:#ccffcc
```

---

## Життєвий цикл JWT токену (Безпечний)

```mermaid
sequenceDiagram
    participant User
    participant Client
    participant AuthServer
    participant API
    participant HSM
    
    User->>Client: Login credentials
    Client->>AuthServer: POST /auth/login
    
    AuthServer->>HSM: Request private key
    HSM-->>AuthServer: Private key reference
    
    AuthServer->>AuthServer: Generate JWT<br/>(RS256, exp: 15min)
    Note over AuthServer: Claims: iss, aud,<br/>exp, iat, nbf
    
    AuthServer-->>Client: JWT Access Token
    Client->>API: Request + Bearer JWT
    
    API->>AuthServer: GET /.well-known/jwks.json
    AuthServer-->>API: Public keys (JWKS)
    
    API->>API: Verify signature<br/>Validate claims
    
    alt Valid Token
        API-->>Client: Protected Resource
        Client-->>User: Data
    else Invalid/Expired
        API-->>Client: 401 Unauthorized
        Client->>AuthServer: Refresh Token
        AuthServer-->>Client: New Access Token
    end
```

---

## Процес хешування пароля (Argon2id)

```mermaid
flowchart TD
    A[User Password] --> B[Generate Random Salt<br/>16 bytes CSPRNG]
    B --> C[Get Pepper from HSM/Env]
    C --> D[Argon2id Hash Function]
    
    D --> E[time_cost: 2]
    D --> F[memory_cost: 19456 KiB]
    D --> G[parallelism: 1]
    
    E --> H[32-byte Hash Output]
    F --> H
    G --> H
    
    H --> I[Store in Database]
    I --> J[Format: $argon2id$params$salt$hash]
    
    style A fill:#e3f2fd
    style D fill:#fff9c4
    style H fill:#c8e6c9
    style J fill:#c8e6c9
```

---

## Процес шифрування даних (AES-256-GCM)

```mermaid
flowchart LR
    A[Plaintext Data] --> B[AES-256-GCM]
    
    subgraph "Inputs"
        C[256-bit Key from HSM]
        D[96-bit Random Nonce]
        E[Additional Auth Data]
    end
    
    C --> B
    D --> B
    E --> B
    
    B --> F[Ciphertext]
    B --> G[128-bit Auth Tag]
    
    F --> H[Store/Transmit]
    G --> H
    D --> H
    
    H --> I[Ciphertext + Tag + Nonce]
    
    style B fill:#fff9c4
    style C fill:#ffcccc
    style D fill:#ccf2ff
    style I fill:#c8e6c9
```

---

## Архітектура управління ключами

```mermaid
graph TB
    subgraph "Application Layer"
        APP[Application]
    end
    
    subgraph "Secret Management"
        VAULT[HashiCorp Vault]
        KMS[Cloud KMS]
        ENV[Environment Variables]
    end
    
    subgraph "Key Storage"
        HSM[Hardware Security Module]
        CLOUDKMS[AWS KMS / Azure Key Vault]
    end
    
    subgraph "Keys & Secrets"
        JWT_KEY[JWT Private Key]
        ENC_KEY[Encryption Keys]
        DB_PASS[Database Passwords]
        API_KEY[API Keys]
    end
    
    APP --> VAULT
    VAULT --> HSM
    VAULT --> JWT_KEY
    VAULT --> ENC_KEY
    VAULT --> DB_PASS
    VAULT --> API_KEY
    
    KMS --> CLOUDKMS
    
    HSM -.rotation 90d.-> JWT_KEY
    HSM -.rotation 90d.-> ENC_KEY
    
    style HSM fill:#ffcccc
    style VAULT fill:#c8e6c9
    style APP fill:#e3f2fd
```

---

## Матриця ризиків конфігурацій

```mermaid
quadrantChart
    title Security Risk Matrix
    x-axis Low Impact --> High Impact
    y-axis Low Probability --> High Probability
    quadrant-1 Critical (Fix Now)
    quadrant-2 High Risk
    quadrant-3 Monitor
    quadrant-4 Medium Risk
    
    WE - algorithm none: [0.9, 0.9]
    WE - no verify: [0.85, 0.85]
    LE - hardcoded secret: [0.6, 0.7]
    LE - DES encryption: [0.7, 0.6]
    MI - fixed IV GCM: [0.8, 0.7]
    MI - low Argon2 params: [0.4, 0.5]
    Secure Config: [0.1, 0.1]
```

---

## Timeline покращення безпеки

```mermaid
timeline
    title Security Improvement Journey
    
    section Critical Issues
        Week 1 : WE - Fix algorithm none
               : WE - Enable signature verification
               : MI - Fix fixed_iv for GCM
    
    section High Priority
        Week 2 : LE - Move secrets to Vault
               : LE - Replace DES with AES-GCM
               : WE - Replace SHA-1 with Argon2id
    
    section Medium Priority
        Week 3-4 : MI - Optimize Argon2 parameters
                 : Add JWT claims validation
                 : Implement key rotation
    
    section Enhancements
        Month 2 : Add TLS 1.3 configuration
                : Implement HSTS
                : Setup audit logging
    
    section Production Ready
        Month 3 : Security audit passed
                : Penetration testing completed
                : Compliance verified
                : ✅ Secure Config Deployed
```

---

## Compliance відповідність

```mermaid
graph TD
    CONFIG[Secure Crypto Config]
    
    CONFIG --> GDPR[GDPR Compliance]
    CONFIG --> HIPAA[HIPAA Compliance]
    CONFIG --> PCI[PCI DSS Compliance]
    CONFIG --> SOC2[SOC 2 Compliance]
    
    GDPR --> G1[✅ Data Encryption at Rest]
    GDPR --> G2[✅ Data Encryption in Transit]
    GDPR --> G3[✅ Right to Erasure]
    GDPR --> G4[✅ Audit Logs]
    
    HIPAA --> H1[✅ ePHI Encryption]
    HIPAA --> H2[✅ Access Controls]
    HIPAA --> H3[✅ Audit Trails]
    
    PCI --> P1[✅ Strong Cryptography]
    PCI --> P2[✅ TLS 1.2+]
    PCI --> P3[✅ Key Rotation]
    
    SOC2 --> S1[✅ Security Controls]
    SOC2 --> S2[✅ Encryption Standards]
    SOC2 --> S3[✅ Incident Response]
    
    style CONFIG fill:#c8e6c9
    style GDPR fill:#e3f2fd
    style HIPAA fill:#e3f2fd
    style PCI fill:#e3f2fd
    style SOC2 fill:#e3f2fd
```

---

## Процес ротації ключів

```mermaid
stateDiagram-v2
    [*] --> Active: New Key Generated
    Active --> PreRetirement: 90 Days Passed
    PreRetirement --> Retired: New Key Active
    Retired --> Destroyed: Old Data Migrated
    Destroyed --> [*]
    
    Active : Key ID: key-2024-12-001
    Active : Status: Primary
    Active : Usage: All new operations
    
    PreRetirement : Key ID: key-2024-09-001
    PreRetirement : Status: Secondary
    PreRetirement : Usage: Decrypt only
    
    Retired : Key ID: key-2024-06-001
    Retired : Status: Deprecated
    Retired : Usage: Decrypt legacy only
    
    Destroyed : Secure deletion
    Destroyed : Audit log retained
```

---

## Attack Surface зменшення

```mermaid
graph LR
    subgraph "Before (WE Config)"
        B1[No JWT Signature]
        B2[SHA-1 Passwords]
        B3[Fixed IV]
        B4[No Expiration]
        B5[Hardcoded Secrets]
    end
    
    subgraph "After (Secure Config)"
        A1[RS256 + Verify]
        A2[Argon2id]
        A3[Random Nonce]
        A4[15min Expiration]
        A5[HSM Storage]
    end
    
    B1 -.Attack Vector<br/>Eliminated.-> A1
    B2 -.Attack Vector<br/>Eliminated.-> A2
    B3 -.Attack Vector<br/>Eliminated.-> A3
    B4 -.Attack Vector<br/>Eliminated.-> A4
    B5 -.Attack Vector<br/>Eliminated.-> A5
    
    style B1 fill:#ffcccc
    style B2 fill:#ffcccc
    style B3 fill:#ffcccc
    style B4 fill:#ffcccc
    style B5 fill:#ffcccc
    style A1 fill:#ccffcc
    style A2 fill:#ccffcc
    style A3 fill:#ccffcc
    style A4 fill:#ccffcc
    style A5 fill:#ccffcc
```

---

## Оцінка безпеки (0-10 шкала)

```mermaid
%%{init: {'theme':'base'}}%%
graph TD
    subgraph "Security Scores"
        WE["WE Config<br/>━━━━━━━━━━<br/>0/10 ❌"]
        LE["LE Config<br/>━━━━━━━━━━<br/>4/10 ⚠️"]
        MI["MI Config<br/>━━━━━━━━━━<br/>7/10 ⚡"]
        SC["Secure Config<br/>━━━━━━━━━━<br/>10/10 ✅"]
    end
    
    WE -->|+4| LE
    LE -->|+3| MI
    MI -->|+3| SC
    
    style WE fill:#ff4444,color:#fff
    style LE fill:#ffaa00,color:#fff
    style MI fill:#00aaff,color:#fff
    style SC fill:#00cc66,color:#fff
```

---

## Використання діаграм

### Для презентацій:
- Копіюйте Mermaid код
- Вставте у Markdown файл
- GitHub/GitLab автоматично відобразить діаграми

### Для документації:
- Використовуйте у README
- Додайте у wiki проєкту
- Включіть у технічну документацію

### Для навчання:
- Візуалізація процесів
- Пояснення архітектури
- Демонстрація покращень

---

## Інструменти для роботи з діаграмами

- **GitHub/GitLab:** Вбудована підтримка Mermaid
- **Mermaid Live Editor:** https://mermaid.live
- **VS Code:** Mermaid Preview Extension
- **Confluence:** Mermaid Macro
- **Notion:** Mermaid blocks

---

**Всі діаграми створені за допомогою Mermaid.js**  
**Легко редагувати та підтримувати! 📊**
