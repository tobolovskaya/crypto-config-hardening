# Домашнє завдання: Проєктування криптозахисту для мікросервісу

## Сервіс зберігання медичних записів (Electronic Health Records - EHR)

**Дата виконання:** Грудень 2025  
**Базується на:** Лабораторній роботі з аналізу криптоконфігурацій

---

## 1. Дані, що потребують захисту

### 1.1 Персональні дані пацієнтів (PII - Personally Identifiable Information)

#### 🔴 Критично чутливі:
- **ПІБ пацієнта** (прізвище, ім'я, по батькові)
- **Дата народження** (точна дата)
- **Номер медичної картки** (унікальний ідентифікатор)
- **Номер соціального страхування** (SSN або аналог)
- **Контактна інформація:**
  - Email адреса
  - Номер телефону
  - Домашня адреса
  - Адреса місця роботи

#### 🔴 Біометричні дані:
- **Група крові та резус-фактор**
- **Відбитки пальців** (для ідентифікації)
- **Скани райдужної оболонки** (biometric auth)
- **Генетичні дані** (DNA profiles)
- **Антропометричні дані** (зріст, вага, тощо)

---

### 1.2 Медичні дані (PHI - Protected Health Information)

#### 🔴 Діагнози та історія хвороб:
- **Встановлені діагнози** (поточні та історичні)
- **Хронічні захворювання** (діабет, гіпертонія, астма, тощо)
- **Психіатричні діагнози** (особливо чутливі!)
- **ВІЛ-статус** (критично конфіденційно)
- **Онкологічні захворювання**
- **Генетічні захворювання**
- **Інфекційні захворювання**

#### 🔴 Лікарські призначення:
- **Рецепти** (назва препарату, дозування, частота)
- **Історія прийому ліків**
- **Алергічні реакції на медикаменти**
- **Побічні ефекти від препаратів**
- **Протипоказання**

#### 🔴 Медичні процедури:
- **Операції** (тип, дата, результат)
- **Лабораторні аналізи** (результати крові, сечі, тощо)
- **Рентгенівські знімки та КТ/МРТ**
- **УЗД результати**
- **ЕКГ дані**
- **Біопсії та гістологічні дослідження**

#### 🔴 Медичні зображення:
- **DICOM файли** (рентген, МРТ, КТ)
- **Фотографії ран та травм**
- **Дерматологічні фото**
- **Ендоскопічні зображення**

---

### 1.3 Дані автентифікації та авторизації

#### 🔴 Облікові дані:
- **Паролі користувачів** (лікарі, медсестри, адміністратори)
- **Паролі пацієнтів** (для пацієнтського порталу)
- **PIN-коди** (для швидкого доступу)
- **Відповіді на секретні питання**

#### 🔴 Токени та сесії:
- **JWT токени** (access та refresh)
- **API ключі** (для інтеграцій)
- **OAuth токени** (для зовнішніх систем)
- **Session cookies**
- **CSRF токени**

#### 🔴 Сертифікати та ключі:
- **Приватні ключі TLS/SSL**
- **Цифрові підписи лікарів**
- **Сертифікати мікросервісів**
- **Encryption keys**

---

### 1.4 Аудит та логи

#### 🟡 Чутливі логи:
- **Логи доступу до медичних записів** (хто, коли, які дані)
- **Історія змін записів** (audit trail)
- **Логи автентифікації** (успішні та невдалі спроби)
- **Логи експорту даних**
- **Логи друку медичних документів**

#### 🟡 Метадані:
- **IP адреси доступу**
- **Часові мітки дій**
- **Місцезнаходження (геолокація)**
- **Пристрій доступу** (browser, OS)

---

### 1.5 Фінансові дані

#### 🔴 Платіжна інформація:
- **Номери кредитних карток**
- **Номери медичних страховок**
- **Деталі страхового полісу**
- **Рахунки за лікування**
- **Історія платежів**

---

### 1.6 Комунікації

#### 🔴 Повідомлення:
- **Листування пацієнт-лікар**
- **Консультації між лікарями**
- **Телемедичні сесії** (відео/аудіо записи)
- **SMS з медичною інформацією**
- **Email повідомлення**

---

### 1.7 Дані міжсервісної комунікації

#### 🟡 Service-to-Service:
- **API запити між мікросервісами**
- **Message queue дані** (RabbitMQ, Kafka)
- **Кеш даних** (Redis, Memcached)
- **Тимчасові файли**
- **Backup дані**

---

## Класифікація даних за чутливістю

### 🔴 КРИТИЧНО (Tier 1 - Top Secret)
**Вимоги:** Обов'язкове шифрування + HSM + повний аудит + обмежений доступ

- Паролі та authentication credentials
- Номери соціального страхування
- Генетичні дані
- ВІЛ-статус та інші особливо чутливі діагнози
- Психіатричні діагнози
- Номери кредитних карток
- Приватні ключі та сертифікати

### 🟠 ВИСОКОЧУТЛИВІ (Tier 2 - Confidential)
**Вимоги:** Шифрування + регулярний аудит + контроль доступу

- Медичні діагнози (загальні)
- Історія лікування
- Лабораторні результати
- Медичні зображення
- Рецепти та призначення
- Персональні дані пацієнтів
- Номери страховок

### 🟡 СЕРЕДНЬОЧУТЛИВІ (Tier 3 - Internal)
**Вимоги:** Базове шифрування + логування доступу

- Аудит логи
- Метадані доступу
- Неідентифіковані статистичні дані
- Технічні логи системи

### 🟢 ПУБЛІЧНІ (Tier 4 - Public)
**Вимоги:** Базовий захист від підміни

- Загальна інформація про клініку
- Розклад роботи
- Публічні статті про здоров'я
- FAQ

---

## Обсяги даних (орієнтовно)

### На 1 пацієнта:
- Текстові дані: ~100-500 KB
- Медичні зображення: 10-500 MB
- Аудит логи: ~10 KB/рік
- **Всього:** 10-500 MB на пацієнта

### На клініку (10,000 пацієнтів):
- **Загальний обсяг:** 100 GB - 5 TB
- **Щоденні зміни:** 1-10 GB
- **Backup потреби:** 300 GB - 15 TB (з версіонуванням)

---

## Законодавчі вимоги до захисту

### 🇺🇸 HIPAA (США):
- Шифрування PHI at rest та in transit
- Access controls та audit trails
- Breach notification (72 години)
- Business Associate Agreements
- Regular risk assessments

### 🇪🇺 GDPR (ЄС):
- Право на забуття
- Data portability
- Consent management
- Breach notification (72 години)
- Data Protection Impact Assessment

### 🇺🇦 Законодавство України:
- Закон "Про захист персональних даних"
- Вимоги до медичних даних
- Згода пацієнта на обробку
- Право доступу до своїх даних

---

## Висновок розділу 1

**У сервісі зберігання медичних записів майже ВСЯ інформація є чутливою!**

### Найкритичніші категорії:
1. 🔴 Паролі та credentials (100% шифрування)
2. 🔴 Діагнози та історія хвороб (HIPAA/GDPR critical)
3. 🔴 Персональні дані пацієнтів (PII)
4. 🔴 Фінансова інформація (PCI DSS)
5. 🔴 Біометричні дані (GDPR Article 9)

### Мінімальні вимоги:
- ✅ Шифрування 100% чутливих даних
- ✅ TLS 1.3 для всіх комунікацій
- ✅ Повний audit trail
- ✅ Контроль доступу (RBAC/ABAC)
- ✅ Regular security audits
- ✅ Incident response plan
- ✅ Data breach procedures

**Наслідки порушення:** Штрафи до €20M (GDPR) або $1.5M (HIPAA) + репутаційні втрати + кримінальна відповідальність

---

# 2. Можливі загрози (STRIDE аналіз)

## 🔴 S - Spoofing (Підміна ідентичності)

### Загроза S1: Підміна лікаря через викрадення облікових даних
**Опис:** Атакуючий викрадає credentials лікаря (фішинг, keylogger) і отримує доступ до системи під його виглядом, переглядає/змінює медичні записи, видає неправильні діагнози або рецепти.

**Наслідки:**
- Неправильне лікування пацієнтів → загроза життю
- Витік конфіденційної медичної інформації
- Порушення HIPAA → штрафи до $1.5M
- Втрата довіри пацієнтів

**Рівень ризику:** 🔴 КРИТИЧНИЙ (висока ймовірність + критичний вплив)

---

### Загроза S2: Підміна мікросервісу
**Опис:** Атакуючий створює фейковий мікросервіс, який видає себе за легітимний API endpoint, перехоплює запити від інших сервісів та збирає/модифікує медичні дані.

**Наслідки:**
- Man-in-the-Middle атака на рівні сервісів
- Масовий витік даних
- Порушення цілісності медичних записів

**Рівень ризику:** 🟠 ВИСОКИЙ (середня ймовірність + високий вплив)

---

### Загроза S3: Підміна пацієнта
**Опис:** Викрадення облікового запису пацієнта для доступу до чужих медичних записів, отримання рецептів на контрольовані препарати.

**Наслідки:**
- Витік персональної медичної інформації (PHI)
- Зловживання медичними послугами
- Identity theft

**Рівень ризику:** 🟠 ВИСОКИЙ (середня ймовірність + високий вплив)

---

## 🔴 T - Tampering (Підміна/зміна даних)

### Загроза T1: Модифікація медичних записів у базі даних
**Опис:** Атакуючий отримує доступ до бази даних (через SQL injection або інсайдера) і змінює діагнози, результати аналізів, видаляє інформацію про алергії, додає фальшиві записи.

**Наслідки:**
- Неправильне лікування → летальний результат
- Приховування злочинів (отруєння, медичні помилки)
- Страхове шахрайство
- Юридичні проблеми для клініки

**Рівень ризику:** 🔴 КРИТИЧНИЙ (середня ймовірність + критичний вплив)

---

### Загроза T2: Підміна даних у процесі передачі (MITM)
**Опис:** Атакуючий перехоплює незашифрований трафік і змінює рецепти (дозування ліків), результати аналізів, діагнози під час передачі між клієнтом і сервером.

**Наслідки:**
- Передозування або неправильне лікування
- Пропуск серйозних захворювань
- Смерть пацієнта

**Рівень ризику:** 🟠 ВИСОКИЙ (низька ймовірність при TLS + критичний вплив)

---

### Загроза T3: SQL Injection
**Опис:** Вразливість у web-формах або API дозволяє ін'єкцію шкідливого SQL-коду, що призводить до зміни/видалення даних у БД або bypass аутентифікації.

**Наслідки:**
- Масова зміна медичних записів
- Повне компрометування бази даних
- Витік всіх даних

**Рівень ризику:** 🔴 КРИТИЧНИЙ (середня ймовірність + критичний вплив)

---

## 🔴 R - Repudiation (Відмова від відповідальності)

### Загроза R1: Лікар відмовляється від своїх дій
**Опис:** Лікар змінює або видаляє медичний запис, але через відсутність audit trail або можливість його видалення, відмовляється від того, що робив ці зміни. Неможливо довести, хто виконав дію.

**Наслідки:**
- Юридичні позови проти клініки
- Неможливість розслідування медичних помилок
- Відсутність accountability
- Порушення HIPAA audit requirements

**Рівень ризику:** 🟠 ВИСОКИЙ (середня ймовірність + високий вплив)

---

### Загроза R2: Несанкціонований доступ без логування
**Опис:** Співробітник переглядає записи пацієнтів, але система не логує цей доступ. Немає доказів несанкціонованого перегляду даних.

**Наслідки:**
- Внутрішні витоки даних (insider threats)
- Порушення privacy пацієнтів
- Неможливість виявити та розслідувати інциденти
- Порушення HIPAA

**Рівень ризику:** 🟠 ВИСОКИЙ (висока ймовірність без логування + високий вплив)

---

## 🔴 I - Information Disclosure (Витік інформації)

### Загроза I1: SQL Injection → масовий витік бази даних
**Опис:** Через вразливість SQL injection атакуючий викачує всю базу даних з медичними записами і продає дані на dark web або використовує для шантажу.

**Наслідки:**
- Масовий витік PHI/PII (Protected Health Information)
- Штрафи HIPAA до $1.5M + GDPR до €20M
- Репутаційні втрати та можливе закриття клініки
- Кримінальна відповідальність

**Рівень ризику:** 🔴 КРИТИЧНИЙ (середня ймовірність + критичний вплив)

---

### Загроза I2: Незашифровані backup
**Опис:** Backup зберігаються без шифрування, атакуючий викрадає backup диски/стрічки або отримує доступ через скомпрометований cloud storage.

**Наслідки:**
- Витік даних за роки (включаючи видалені записи)
- Порушення GDPR "right to be forgotten"
- Масовий витік історичних PHI

**Рівень ризику:** 🔴 КРИТИЧНИЙ (середня ймовірність + критичний вплив)

---

### Загроза I3: Insider threat (внутрішня загроза)
**Опис:** Співробітник з легітимним доступом зловживає своїми правами: переглядає записи знаменитостей, родичів, знайомих; продає інформацію журналістам або конкурентам.

**Наслідки:**
- Репутаційні втрати
- Втрата довіри пацієнтів
- Юридичні позови
- Порушення privacy

**Рівень ризику:** 🟠 ВИСОКИЙ (висока ймовірність + високий вплив)

---

### Загроза I4: Витік PHI через логи
**Опис:** Логи містять незашифровані медичні дані (діагнози, імена пацієнтів), зберігаються в незахищеному місці, доступ до логів не контролюється.

**Наслідки:**
- Непрямий витік PHI
- Порушення HIPAA "minimum necessary" rule
- Витік через системи моніторингу

**Рівень ризику:** 🟡 СЕРЕДНІЙ (висока ймовірність + середній вплив)

---

## 🔴 D - Denial of Service (Відмова в обслуговуванні)

### Загроза D1: DDoS атака на критичні сервіси
**Опис:** Масована DDoS атака на API сервери або базу даних призводить до недоступності системи для лікарів та неможливості доступу до критичних медичних записів.

**Наслідки:**
- Затримка лікування → потенційна загроза життю
- Неможливість отримати результати аналізів
- Хаос в роботі клініки
- Фінансові втрати

**Рівень ризику:** 🟡 СЕРЕДНІЙ (середня ймовірність + високий вплив)

---

### Загроза D2: Ransomware атака
**Опис:** Ransomware шифрує всі медичні дані з вимогою викупу. Якщо backup теж online, вони також шифруються. Повна втрата доступу до даних пацієнтів.

**Наслідки:**
- Повна зупинка роботи клініки
- Неможливість лікування пацієнтів
- Потенційні смерті через недоступність критичної інформації
- Величезні фінансові втрати

**Рівень ризику:** 🔴 КРИТИЧНИЙ (висока ймовірність для healthcare + критичний вплив)

---

### Загроза D3: Resource exhaustion через криптографічні атаки
**Опис:** Атакуючий робить масові запити на ресурсоємні операції (Argon2 hashing, шифрування), виснажуючи CPU/Memory сервера. Сервіс перестає відповідати.

**Наслідки:**
- Відмова в обслуговуванні
- Degraded performance
- Втрата продуктивності

**Рівень ризику:** 🟡 НИЗЬКИЙ (низька ймовірність + середній вплив)

---

## 🔴 E - Elevation of Privilege (Підвищення привілеїв)

### Загроза E1: Підвищення привілеїв через вразливість RBAC
**Опис:** Медсестра або інший користувач з обмеженими правами експлуатує вразливість у системі контролю доступу та отримує права адміністратора.

**Наслідки:**
- Необмежений доступ до всіх даних пацієнтів
- Можливість видаляти аудит логи
- Створення backdoor accounts
- Повна компрометація системи

**Рівень ризику:** 🟠 ВИСОКИЙ (низька ймовірність + критичний вплив)

---

### Загроза E2: Bypass аутентифікації через JWT manipulation
**Опис:** Атакуючий маніпулює JWT токеном, експлуатує session hijacking або cookie tampering для отримання несанкціонованого доступу без валідних credentials.

**Наслідки:**
- Unauthorized access до системи
- Витік даних
- Можливість tampering даних

**Рівень ризику:** 🟠 ВИСОКИЙ (середня ймовірність + високий вплив)

---

## Матриця ризиків (Top загрози)

| ID | Загроза | Тип | Ймовірність | Вплив | Рівень ризику |
|----|---------|-----|-------------|-------|---------------|
| I1 | SQL Injection → витік БД | I | Середня | Критичний | 🔴 КРИТИЧНИЙ |
| T1 | Модифікація медичних записів | T | Середня | Критичний | 🔴 КРИТИЧНИЙ |
| D2 | Ransomware | D | Висока | Критичний | 🔴 КРИТИЧНИЙ |
| S1 | Підміна лікаря | S | Висока | Критичний | 🔴 КРИТИЧНИЙ |
| I2 | Незашифровані backup | I | Середня | Критичний | 🔴 КРИТИЧНИЙ |
| T3 | SQL Injection | T | Середня | Критичний | 🔴 КРИТИЧНИЙ |
| I3 | Insider threat | I | Висока | Високий | 🟠 ВИСОКИЙ |
| E1 | Elevation of privilege | E | Низька | Критичний | 🟠 ВИСОКИЙ |
| T2 | MITM | T | Низька | Критичний | 🟠 ВИСОКИЙ |
| S2 | Підміна мікросервісу | S | Середня | Високий | 🟠 ВИСОКИЙ |
| S3 | Підміна пацієнта | S | Середня | Високий | 🟠 ВИСОКИЙ |
| R1 | Відмова від дій | R | Середня | Високий | 🟠 ВИСОКИЙ |
| R2 | Доступ без логування | R | Висока | Високий | 🟠 ВИСОКИЙ |
| E2 | Bypass аутентифікації | E | Середня | Високий | 🟠 ВИСОКИЙ |
| D1 | DDoS | D | Середня | Високий | 🟡 СЕРЕДНІЙ |
| I4 | Витік через логи | I | Висока | Середній | 🟡 СЕРЕДНІЙ |
| D3 | Resource exhaustion | D | Низька | Середній | 🟢 НИЗЬКИЙ |

---

## Висновок розділу 2

**ТОП-5 найкритичніших загроз для медичного сервісу:**

1. **🔴 Ransomware (D2)** - може повністю паралізувати клініку та загрожувати життю пацієнтів
2. **🔴 SQL Injection → витік БД (I1)** - масовий витік PHI, штрафи до €20M
3. **🔴 Підміна лікаря (S1)** - неправильне лікування, загроза життю пацієнтів
4. **🔴 Модифікація медичних записів (T1)** - зміна діагнозів/рецептів → летальні наслідки
5. **🔴 Незашифровані backup (I2)** - витік історичних даних за роки

**Обов'язкові заходи захисту (відповідь на виявлені загрози):**
- ✅ **Шифрування:** AES-256-GCM для всіх PHI (проти I1, I2, I3, I4)
- ✅ **TLS 1.3 + mTLS:** Захист від MITM та підміни сервісів (проти T2, S2)
- ✅ **MFA:** Для всіх користувачів (проти S1, S3, E2)
- ✅ **Immutable audit logs:** Повний trail всіх дій (проти R1, R2, I3)
- ✅ **RBAC/ABAC:** Строгий контроль доступу (проти E1, I3)
- ✅ **Encrypted offline backups:** Захист від ransomware (проти D2)
- ✅ **WAF + Input validation:** Захист від SQL injection (проти I1, T1, T3)
- ✅ **Rate limiting + DDoS protection:** Захист від DoS (проти D1, D3)

---

# 3. Криптографічні механізми захисту

## 3.1 Гешування паролів — Argon2id

### Чому Argon2id:
- **Переможець Password Hashing Competition 2015** — найсучасніший алгоритм
- **Memory-hard функція** — стійкість до GPU/ASIC атак (потрібно багато RAM)
- **Hybrid режим** — комбінує Argon2i (захист від side-channel) + Argon2d (захист від GPU)
- **Рекомендовано:** OWASP, NIST, RFC 9106

### Параметри для медичного сервісу:
```yaml
password_hashing:
  algorithm: argon2id
  time_cost: 3              # Ітерацій (більше = повільніше = безпечніше)
  memory_cost: 65536        # 64 MiB пам'яті (vs 19 MiB базовий)
  parallelism: 4            # 4 паралельні потоки
  hash_length: 32           # 256 біт вихідного хешу
  salt_length: 16           # 128 біт унікальної солі для кожного пароля
  pepper: "${PEPPER_KEY}"   # Додатковий секрет з HSM/Vault
```

**Час хешування:** ~500ms (баланс між безпекою та user experience)

### Захист від загроз:
- ✅ **S1 (Підміна лікаря)** — неможливо зламати пароль brute-force
- ✅ **S3 (Підміна пацієнта)** — захист облікових записів
- ✅ **E2 (Bypass auth)** — стійкість до атак на паролі

---

## 3.2 Шифрування даних на диску — AES-256-GCM

### Чому AES-256-GCM:
- **AEAD (Authenticated Encryption with Associated Data)** — одночасно шифрування + автентичність + цілісність
- **256-біт ключ** — стійкість навіть до квантових комп'ютерів
- **Апаратна підтримка (AES-NI)** — швидке шифрування на сучасних процесорах
- **NIST затверджений** — відповідає HIPAA/GDPR/PCI DSS

### Що шифруємо:
```yaml
encryption_at_rest:
  algorithm: AES-256-GCM
  key_length: 256           # біт
  nonce_length: 96          # 12 байт для GCM (ОБОВ'ЯЗКОВО ВИПАДКОВИЙ!)
  tag_length: 128           # 16 байт authentication tag
  
  encrypted_fields:
    # Tier 1 - Критично чутливі
    - patient_ssn            # Номер соціального страхування
    - credit_card_number     # Платіжні дані
    - hiv_status             # ВІЛ-статус
    - psychiatric_diagnosis  # Психіатричні діагнози
    - genetic_data           # Генетична інформація
    
    # Tier 2 - Високочутливі (PHI/PII)
    - patient_name
    - date_of_birth
    - address
    - phone
    - email
    - diagnosis
    - treatment_history
    - prescriptions
    - lab_results
    - medical_images
```

**⚠️ КРИТИЧНО:** Nonce (IV) має бути **випадковим для кожної операції шифрування**! Fixed nonce з GCM = повна компрометація ключа.

### Envelope Encryption (двошарове шифрування):
```
Patient Data 
  → DEK (Data Encryption Key) шифрує дані швидко
  → KEK (Key Encryption Key) шифрує DEK, зберігається в KMS/HSM
```

**Переваги:**
- DEK швидко шифрує дані (AES)
- KEK захищений у HSM (ніколи не виходить назовні)
- Легка ротація ключів (перешифровуємо тільки DEK)

```yaml
envelope_encryption:
  enabled: true
  dek_algorithm: AES-256-GCM
  kek_storage: aws-kms
  dek_rotation_days: 90
  kek_rotation_days: 365
```

### Захист від загроз:
- ✅ **I1 (SQL Injection → витік БД)** — дані зашифровані навіть при компрометації БД
- ✅ **I2 (Незашифровані backup)** — backup автоматично зашифровані
- ✅ **I3 (Insider threat)** — навіть DBA не бачить plaintext без ключів

---

## 3.3 Захищена передача даних — TLS 1.3

### Чому TLS 1.3:
- **Найновіший стандарт (RFC 8446, 2018)** — виправлені вразливості попередніх версій
- **Швидший handshake** — 1-RTT замість 2-RTT (TLS 1.2)
- **Perfect Forward Secrecy** — компрометація ключа не розкриває старі сесії
- **Видалені застарілі cipher suites** — тільки безпечні алгоритми
- **Шифрування handshake** — захист метаданих

### Конфігурація:
```yaml
tls:
  min_version: "1.3"
  max_version: "1.3"
  
  cipher_suites:
    - TLS_AES_256_GCM_SHA384          # Найсильніший
    - TLS_CHACHA20_POLY1305_SHA256    # Для мобільних (без AES-NI)
    - TLS_AES_128_GCM_SHA256          # Швидший
  
  certificate:
    key_type: RSA
    key_size: 3072              # Для medical (вище стандартних 2048)
    signature_algorithm: SHA-384
    validity_days: 365
  
  hsts:                         # HTTP Strict Transport Security
    enabled: true
    max_age: 31536000           # 1 рік
    include_subdomains: true
```

### Де застосовуємо TLS 1.3:
- 🔒 **Client ↔ API Gateway** — веб/мобільні додатки
- 🔒 **API Gateway ↔ Microservices** — внутрішня комунікація
- 🔒 **Microservice ↔ Database** — запити до БД
- 🔒 **Microservice ↔ Cache/Queue** — Redis, RabbitMQ, Kafka

### Mutual TLS (mTLS) для service-to-service:
```yaml
mtls:
  enabled: true
  require_client_certificate: true
  client_cert_validation:
    verify_certificate_chain: true
    check_revocation: true      # OCSP
  certificate_rotation_days: 90
```

**mTLS переваги:**
- Обидві сторони автентифікуються сертифікатами
- Zero-trust архітектура — кожен сервіс підтверджує identity
- Захист від підміни сервісів

### Захист від загроз:
- ✅ **T2 (MITM)** — неможливий перехват та зміна даних
- ✅ **I4 (Витік при передачі)** — все зашифровано
- ✅ **S2 (Підміна мікросервісу)** — mTLS автентифікація

---

## 3.4 Підпис повідомлень між мікросервісами — HMAC-SHA256

### Чому HMAC-SHA256:
- **Швидкий** — симетричний алгоритм (vs RSA)
- **Гарантує автентичність та цілісність** — будь-яка зміна виявляється
- **Підходить для high-throughput** — мільйони повідомлень/сек
- **Простий у реалізації** — стандартна бібліотека в усіх мовах

### Використання:
```yaml
message_authentication:
  algorithm: HMAC-SHA256
  key_length: 256
  key_storage: aws-secrets-manager
  key_rotation_days: 90
  
  use_cases:
    - service_to_service_api_calls   # Між мікросервісами
    - message_queue_messages          # RabbitMQ, Kafka
    - webhook_signatures              # Зовнішні інтеграції
    - audit_log_integrity             # Захист логів від підміни
```

### Приклад:
```python
message = {"patient_id": "12345", "diagnosis": "diabetes"}
timestamp = "2025-12-08T10:30:00Z"
signature = HMAC-SHA256(message + timestamp, secret_key)

# Відправка
{
  "message": message,
  "timestamp": timestamp,
  "signature": signature
}

# Перевірка
expected_sig = HMAC-SHA256(received_message + received_timestamp, secret_key)
if signature != expected_sig:
    reject_message()
```

**Replay attack protection:**
- Timestamp window (5 хвилин) — відкидати старі повідомлення
- Nonce (одноразовий ID) — перевіряти унікальність

### Захист від загроз:
- ✅ **T1 (Модифікація даних)** — зміна виявляється через HMAC
- ✅ **R2 (Відмова від дій)** — підписане повідомлення = proof
- ✅ **S2 (Підміна сервісу)** — тільки з правильним ключем

---

## 3.5 Цифровий підпис медичних документів — RSA-PSS

### Для юридично значущих документів:

**Чому RSA-PSS:**
- **Probabilistic Signature Scheme** — безпечніше за PKCS#1 v1.5
- **Non-repudiation** — юридично валідний доказ авторства
- **Незмінність** — будь-яка зміна документа інвалідує підпис

```yaml
digital_signature:
  algorithm: RSA-PSS
  key_size: 3072              # Для медичних систем
  hash_algorithm: SHA-384
  
  signed_documents:
    - prescriptions           # Рецепти (критично!)
    - lab_reports             # Результати аналізів
    - discharge_summaries     # Виписки
    - consent_forms           # Згоди на лікування
    - medical_certificates    # Довідки
    
  signature_metadata:
    - doctor_id
    - medical_license_number
    - timestamp
    - document_hash_sha384
```

### JWT для автентифікації (RS256):
```yaml
jwt:
  algorithm: RS256            # Асиметричний (public/private key)
  key_size: 3072
  
  access_token:
    expiration: 900           # 15 хвилин
  refresh_token:
    expiration: 604800        # 7 днів
    rotation: true
```

**RS256 vs HS256:**
- RS256: тільки auth server має приватний ключ
- Мікросервіси перевіряють через публічний ключ (JWKS)
- Неможливо підробити токен без приватного ключа

### Захист від загроз:
- ✅ **R1 (Відмова від дій)** — юридично валідний підпис лікаря
- ✅ **T1 (Модифікація)** — зміна документа інвалідує підпис
- ✅ **S1 (Підміна лікаря)** — криптографічно підписані токени

---

## 3.6 Зберігання ключів — HSM / KMS / Vault

### 3.6.1 AWS KMS (Key Management Service)

**Для master encryption keys:**
```yaml
kms:
  provider: aws-kms
  fips_140_2_level: 2         # Сертифікація безпеки
  
  master_keys:
    database_encryption:
      rotation_enabled: true
      rotation_days: 365
      
    backup_encryption:
      rotation_enabled: true
      rotation_days: 365
```

**Переваги KMS:**
- ✅ Ключі **ніколи не виходять** з HSM
- ✅ Автоматична ротація
- ✅ Аудит логи (CloudTrail) — кожен доступ логується
- ✅ IAM контроль доступу

---

### 3.6.2 HashiCorp Vault

**Для application secrets:**
```yaml
vault:
  address: "https://vault.medical.internal:8200"
  
  dynamic_secrets:
    database_credentials:
      path: "database/creds/medical-rw"
      ttl: 3600               # 1 година
      renewable: true
      
  static_secrets:
    api_keys:
      path: "secret/data/integrations"
      version: 2              # Versioning
      
  transit_encryption:         # Encryption as a Service
    enabled: true
    key_name: "patient-data"
    algorithm: aes256-gcm96
```

**Переваги Vault:**
- ✅ **Dynamic secrets** — генерація на льоту, автоматичне закінчення
- ✅ **Secret versioning** — історія змін
- ✅ **Lease and renewal** — тимчасові credentials
- ✅ **Encryption as a Service** — централізоване шифрування

---

### 3.6.3 HSM (Hardware Security Module)

**Для найкритичніших ключів:**
```yaml
hsm:
  type: aws-cloudhsm
  fips_140_2_level: 3         # Tamper-resistant hardware
  
  stored_keys:
    - root_ca_private_key     # Root CA для сертифікатів
    - master_encryption_key   # KEK для envelope encryption
    - code_signing_key        # Для підпису software updates
```

**Чому HSM:**
- ✅ **FIPS 140-2 Level 3/4** — найвищий рівень захисту
- ✅ **Tamper-resistant** — фізичний захист, знищення при втручанні
- ✅ Ключі **НІКОЛИ не виходять** назовні
- ✅ Всі операції всередині HSM

---

### 3.6.4 Ротація ключів

**Автоматичний графік:**
```yaml
key_rotation:
  encryption_keys: 90_days          # KEK/DEK
  jwt_signing_keys: 180_days        # З overlap period
  database_passwords: 30_days       # Vault dynamic
  tls_certificates: 365_days        # З renewal за 30 днів
  api_keys: 90_days
```

**Процес ротації:**
1. Генерація нового ключа (KEK_new)
2. Перешифрування DEK
3. Поступова міграція даних (zero downtime)
4. Видалення старого ключа

**Чому важливо:**
- Обмежує час життя скомпрометованого ключа
- HIPAA/PCI DSS compliance вимога
- Defense in depth

---

## 3.7 Аудит криптооперацій — Immutable Logs

### Чому immutable:
- **HIPAA requirement** — 7 років зберігання
- **Forensics** — розслідування інцидентів
- **Non-repudiation** — неможливо заперечити дії
- **Tamper-proof** — неможливо змінити/видалити

```yaml
audit_logging:
  storage: aws-s3
  object_lock_mode: COMPLIANCE      # Навіть root не може видалити
  retention_years: 7                # HIPAA requirement
  
  encryption: AES-256-GCM
  signature: RSA-PSS-3072           # Кожен лог підписується
  
  logged_events:
    authentication:
      - login_success
      - login_failure
      - mfa_verification
      
    data_access:
      - patient_record_viewed
      - patient_record_modified
      - prescription_created
      - lab_result_accessed
      
    crypto_operations:
      - key_generated
      - key_rotated
      - encryption_performed
      - decryption_performed
      - signature_created
      
    administrative:
      - user_created
      - permissions_changed
      - configuration_modified
```

### Real-time alerting:
```yaml
alerts:
  - event: multiple_failed_logins
    threshold: 5
    window: 10_minutes
    action: block_ip + notify_security
    
  - event: mass_data_access
    threshold: 100_records
    window: 1_hour
    action: require_justification + alert
    
  - event: encryption_key_accessed
    action: immediate_alert_to_security
```

### Захист від загроз:
- ✅ **R1, R2 (Repudiation)** — повний trail всіх дій, неможливо заперечити
- ✅ **I3 (Insider threat)** — виявлення підозрілої активності
- ✅ **Compliance** — HIPAA audit requirements

---

## Підсумок: Покриття STRIDE загроз

| Механізм | S | T | R | I | D | E |
|----------|---|---|---|---|---|---|
| **Argon2id** | ✅ | - | - | - | - | ✅ |
| **AES-256-GCM** | - | ✅ | - | ✅ | - | - |
| **TLS 1.3 + mTLS** | ✅ | ✅ | - | ✅ | - | - |
| **HMAC-SHA256** | ✅ | ✅ | ✅ | - | - | - |
| **RSA-PSS підписи** | ✅ | ✅ | ✅ | - | - | - |
| **KMS/HSM/Vault** | - | - | - | ✅ | - | - |
| **Immutable logs** | - | - | ✅ | ✅ | - | - |
| **RBAC/ABAC** | ✅ | - | - | ✅ | - | ✅ |
| **Rate limiting** | - | - | - | - | ✅ | - |

**Легенда:**
- **S** - Spoofing
- **T** - Tampering
- **R** - Repudiation
- **I** - Information Disclosure
- **D** - Denial of Service
- **E** - Elevation of Privilege

---

## Compliance відповідність

✅ **HIPAA** — шифрування PHI, audit logs, access controls  
✅ **GDPR** — encryption at rest/transit, right to be forgotten  
✅ **PCI DSS** — strong cryptography, key management  
✅ **SOC 2** — security controls, monitoring

---

# 4. YAML-конфігурація мікросервісу

## 📄 Повна конфігурація

Детальна YAML-конфігурація мікросервісу зберігання медичних записів створена в окремому файлі:

**Файл:** [`medical_records_microservice_config.yaml`](./medical_records_microservice_config.yaml)

**Розмір:** 67 KB  
**Коментарів:** 150+  
**Розділів:** 13

---

## Структура конфігурації

### 1. JWT Authentication (RS256)
```yaml
jwt:
  algorithm: "RS256"          # Асиметричне шифрування
  key_size: 3072              # Для medical (вище стандартних 2048)
  
  access_token:
    expiration_seconds: 900   # 15 хвилин
  
  refresh_token:
    expiration_seconds: 604800  # 7 днів
    rotation_enabled: true      # Ротація при кожному використанні
```

**Пояснення:**
- **RS256** замість HS256 — тільки auth server має приватний ключ
- **3072-біт** — вища безпека для медичних даних
- **15 хвилин** access token — мінімізує час використання скомпрометованого токена
- **Ротація refresh token** — захист від replay attacks

---

### 2. Password Hashing (Argon2id)
```yaml
password_hashing:
  algorithm: "argon2id"
  time_cost: 3                # Ітерацій (вище базового)
  memory_cost_kib: 65536      # 64 MiB (захист від GPU)
  parallelism: 4              # 4 потоки
  hash_length: 32             # 256 біт
  salt_length: 16             # 128 біт унікальної солі
  
  pepper_enabled: true        # Додатковий секрет з HSM
  pepper_source: "aws-secrets-manager"
```

**Пояснення:**
- **time_cost: 3** — збільшено для критичних систем (~500ms)
- **memory_cost: 64 MiB** — робить GPU атаки економічно невигідними
- **pepper** — зберігається окремо від БД, подвійний захист

---

### 3. Data Encryption at Rest (AES-256-GCM)
```yaml
encryption_at_rest:
  algorithm: "AES-256-GCM"
  key_length: 256
  nonce_length: 96            # 12 байт для GCM
  tag_length: 128             # 16 байт authentication tag
  
  # ⚠️ КРИТИЧНО: випадковий nonce для КОЖНОЇ операції!
  nonce_generation: "crypto_random"
  nonce_reuse_check: true
  
  envelope_encryption:
    enabled: true
    dek_algorithm: "AES-256-GCM"
    kek_provider: "aws-kms"
    dek_rotation_days: 90
```

**Пояснення:**
- **GCM режим** — AEAD (шифрування + автентичність + цілісність)
- **Випадковий nonce** — fixed nonce з GCM = катастрофа!
- **Envelope encryption** — DEK шифрує дані, KEK (в KMS) шифрує DEK

---

### 4. TLS 1.3 Configuration
```yaml
encryption_in_transit:
  tls:
    min_version: "1.3"
    max_version: "1.3"
    
    cipher_suites:
      - "TLS_AES_256_GCM_SHA384"      # Найсильніший
      - "TLS_CHACHA20_POLY1305_SHA256" # Для мобільних
    
    certificate:
      key_size: 3072                   # Для medical
      signature_algorithm: "SHA-384"
    
    hsts:
      enabled: true
      max_age_seconds: 31536000        # 1 рік
```

**Пояснення:**
- **Тільки TLS 1.3** — виключає застарілі версії
- **3072-біт сертифікат** — вища безпека для healthcare
- **HSTS** — браузер завжди використовує HTTPS

---

### 5. Message Authentication (HMAC-SHA256)
```yaml
message_authentication:
  algorithm: "HMAC-SHA256"
  key_length: 256
  key_rotation_days: 90
  
  use_cases:
    - service_to_service_api_calls
    - message_queue_messages
    - webhook_signatures
    - audit_log_integrity
  
  replay_protection:
    enabled: true
    timestamp_window_seconds: 300    # 5 хвилин
    nonce_required: true
```

**Пояснення:**
- **HMAC** — швидший за RSA для міжсервісної комунікації
- **Timestamp window** — відкидає старі повідомлення (replay attack)
- **Nonce** — гарантує унікальність кожного повідомлення

---

### 6. Key Management (KMS + Vault + HSM)
```yaml
key_management:
  kms:
    provider: "aws-kms"
    
    master_keys:
      database_encryption:
        rotation_enabled: true
        rotation_period_days: 365
      
      backup_encryption:
        rotation_enabled: true
        rotation_period_days: 365
  
  vault:
    dynamic_secrets:
      database_credentials:
        ttl_seconds: 3600             # 1 година
        renewable: true
  
  hsm:
    enabled: true
    stored_keys:
      - root_ca_private_key
      - master_encryption_key
```

**Пояснення:**
- **KMS** — для master encryption keys (FIPS 140-2 Level 2)
- **Vault** — dynamic secrets (автоматично закінчуються)
- **HSM** — найкритичніші ключі (FIPS 140-2 Level 3)

---

### 7. Audit Logging (Immutable)
```yaml
audit_logging:
  immutable: true                     # Неможливо змінити/видалити
  storage: "aws-s3"
  object_lock_mode: "COMPLIANCE"      # Навіть root не може видалити
  
  logged_events:
    authentication:
      - login_success
      - login_failure
      - mfa_verification
    
    data_access:
      - patient_record_viewed
      - patient_record_modified
      - prescription_created
    
    crypto_operations:
      - key_generated
      - key_rotated
      - encryption_performed
  
  encryption: "AES-256-GCM"
  signature: "RSA-PSS-3072"
  retention_years: 7                  # HIPAA requirement
```

**Пояснення:**
- **Immutable** — HIPAA вимога, forensics
- **Object lock COMPLIANCE** — захист від видалення
- **7 років** — законодавча вимога для медичних даних
- **Шифрування + підпис логів** — захист цілісності

---

### 8. Access Control (RBAC + ABAC)
```yaml
access_control:
  rbac:
    roles:
      doctor:
        permissions:
          - read:patient_records
          - write:patient_records
          - create:prescriptions
        constraints:
          - own_patients_only
        mfa_required: true
      
      nurse:
        permissions:
          - read:patient_records
          - write:vital_signs
        constraints:
          - assigned_patients_only
      
      patient:
        permissions:
          - read:own_records
        constraints:
          - own_data_only
      
      admin:
        permissions:
          - manage:users
          - configure:system
        constraints:
          - no_patient_data_access    # Least privilege!
  
  abac:
    emergency_access:
      condition: "user.role == 'doctor' AND context.emergency == true"
      allow: "access:all_patient_records"
      audit: "detailed"
      require_justification: true
```

**Пояснення:**
- **RBAC** — базовий контроль за ролями
- **Constraints** — додаткові обмеження (own_patients_only)
- **ABAC** — для складних сценаріїв (emergency access)
- **Admin без доступу до даних** — least privilege principle

---

### 9. Security Monitoring & Alerting
```yaml
security_monitoring:
  siem:
    enabled: true
    platform: "splunk"
  
  anomaly_detection:
    enabled: true
    ml_model: "isolation_forest"
  
  alerting:
    critical:
      - name: "Multiple failed logins"
        condition: "failed_logins >= 5 in 10 minutes"
        action: "block_ip + notify_security"
      
      - name: "Mass data access"
        condition: "records_accessed >= 100 in 1 hour"
        action: "require_justification + alert"
      
      - name: "Encryption key accessed"
        action: "immediate_alert_to_security"
```

**Пояснення:**
- **SIEM** — централізований моніторинг
- **ML anomaly detection** — виявлення незвичної поведінки
- **Real-time alerts** — негайне реагування на критичні події

---

### 10. Compliance (HIPAA, GDPR, PCI DSS)
```yaml
compliance:
  hipaa:
    enabled: true
    breach_notification_deadline_hours: 72
    audit_retention_years: 6
    
  gdpr:
    enabled: true
    data_subject_rights:
      - right_to_access
      - right_to_erasure
      - right_to_portability
    
  pci_dss:
    enabled: true
    level: 1                          # Найвищий рівень
```

**Пояснення:**
- **HIPAA** — для США (медичні дані)
- **GDPR** — для ЄС (персональні дані)
- **PCI DSS** — для платіжних карток

---

### 11. Incident Response
```yaml
incident_response:
  response_plan:
    enabled: true
    
  incident_classification:
    critical:
      examples:
        - ransomware_attack
        - mass_data_breach
      response_time_minutes: 15
      
  automated_response:
    - trigger: "brute_force_detected"
      action: "block_ip_address"
    - trigger: "ransomware_indicators"
      action: "disconnect_network + snapshot_system"
```

**Пояснення:**
- **15 хвилин** на critical — негайне реагування
- **Automated response** — блокування без участі людини
- **Ransomware plan** — ізоляція + snapshot

---

### 12. Backup & Disaster Recovery
```yaml
backup_disaster_recovery:
  backup:
    strategy: "3-2-1"                 # 3 копії, 2 носії, 1 offline
    
    encryption:
      enabled: true                   # ОБОВ'ЯЗКОВО!
      algorithm: "AES-256-GCM"
    
    storage:
      primary: "aws-s3"
      secondary: "aws-glacier"
      offline: "tape_library"         # Ransomware protection
    
    retention:
      daily_backups_days: 30
      monthly_backups_years: 7
  
  disaster_recovery:
    rpo_minutes: 15                   # Recovery Point Objective
    rto_hours: 4                      # Recovery Time Objective
```

**Пояснення:**
- **3-2-1 правило** — надійність backup
- **Offline копія** — захист від ransomware
- **RPO 15 хвилин** — максимум втрачених даних
- **RTO 4 години** — час відновлення

---

### 13. Rate Limiting & DDoS Protection
```yaml
rate_limiting:
  enabled: true
  
  endpoints:
    login:
      requests_per_minute: 5
      requests_per_hour: 20
    
    api:
      requests_per_minute: 60
  
  ddos_protection:
    enabled: true
    provider: "cloudflare"
    
    waf:
      enabled: true
      rule_sets:
        - owasp_top_10
        - sql_injection_prevention
        - xss_prevention
```

**Пояснення:**
- **5 спроб login/хв** — захист від brute-force
- **WAF** — Web Application Firewall
- **OWASP Top 10** — захист від найпоширеніших атак

---

## Ключові особливості конфігурації

### ✅ Безпека:
- Всі чутливі дані шифруються (AES-256-GCM)
- TLS 1.3 для всіх комунікацій
- MFA для критичних ролей
- Immutable audit logs (7 років)

### ✅ Compliance:
- HIPAA — медичні дані США
- GDPR — персональні дані ЄС
- PCI DSS — платіжні картки
- SOC 2 — security controls

### ✅ Operational Excellence:
- Автоматична ротація ключів
- Dynamic secrets (Vault)
- Real-time monitoring
- Automated incident response

### ✅ High Availability:
- 3-2-1 backup strategy
- Hot standby (інший регіон)
- RPO: 15 хвилин
- RTO: 4 години

---


# 5. Висновок

# 5. Підсумок: Критичні vs Бажані заходи

## 🔴 Критично важливі заходи (MUST HAVE)

### Без цього система НЕ може функціонувати безпечно:

#### 1. Шифрування PHI/PII — AES-256-GCM
**Чому критично:**
- HIPAA/GDPR **законодавча вимога** — без шифрування штраф до €20M / $1.5M
- Захист від загроз I1, I2, I3 (витік даних)
- При компрометації БД дані залишаються нечитабельними

**Наслідки відсутності:**
- Порушення законодавства → закриття клініки
- Масовий витік медичних даних
- Репутаційні та фінансові втрати

---

#### 2. TLS 1.3 для всіх комунікацій
**Чому критично:**
- Захист від T2 (MITM атаки) — перехват та зміна даних у процесі передачі
- Відсутність TLS = передача паролів, діагнозів, SSN у відкритому вигляді
- Compliance requirement (HIPAA, PCI DSS)

**Наслідки відсутності:**
- Атакуючий бачить всі дані (пароль, діагноз, SSN)
- Можливість підміни даних (зміна рецептів, результатів аналізів)
- HIPAA порушення

**Де застосовувати:**
- ✅ Client ↔ Server (веб/мобільні додатки)
- ✅ Service ↔ Service (mTLS)
- ✅ Service ↔ Database
- ✅ Service ↔ Cache/Queue

---

#### 3. Argon2id для паролів
**Чому критично:**
- SHA-1, MD5, навіть SHA-256 **небезпечні** для паролів
- Захист від S1, S3 (підміна користувачів) через brute-force
- Memory-hard алгоритм — GPU/ASIC атаки неефективні

**Наслідки використання застарілих:**
```yaml
# ❌ КАТАСТРОФІЧНО НЕБЕЗПЕЧНО
password_hash = md5(password)        # Зламується за секунди
password_hash = sha256(password)     # Зламується за години
password_hash = sha256(password + "salt")  # Зламується за дні
```

**Правильно:**
```yaml
# ✅ БЕЗПЕЧНО
argon2id(password, salt, time_cost=3, memory=64MB)  # Зламується роками
```

---

#### 4. Immutable Audit Logs
**Чому критично:**
- HIPAA **вимагає** 7 років зберігання логів всіх доступів до PHI
- Захист від R1, R2 (repudiation) — доказ хто і коли виконав дію
- Виявлення I3 (insider threats) — підозріла активність

**Наслідки відсутності:**
- Неможливість розслідувати інциденти
- Відсутність доказів при юридичних позовах
- HIPAA порушення → штрафи
- Інсайдери діють безкарно

**Що логувати:**
- Всі доступи до patient records
- Зміни даних (хто, коли, що змінив)
- Автентифікація (login/logout)
- Криптооперації (генерація/ротація ключів)

---

#### 5. KMS/Vault для ключів (НЕ hardcode!)
**Чому критично:**
- Hardcoded secrets = одна компрометація коду → всі дані розкриті
- Захист від I1, I2 (витік ключів)

**❌ НІКОЛИ не робіть так:**
```python
# Hardcoded у коді
JWT_SECRET = "my-secret-key-123"
DB_PASSWORD = "admin123"
ENCRYPTION_KEY = "0123456789abcdef"
```

**✅ Правильно:**
```yaml
# Vault/KMS
JWT_SECRET = vault.get("secret/jwt-signing-key")
DB_PASSWORD = vault.get("database/creds/dynamic")  # Динамічні credentials
ENCRYPTION_KEY = kms.generate_data_key()
```

**Наслідки hardcoded secrets:**
- Git history містить секрети назавжди
- Витік коду (GitHub leak) = всі ключі скомпрометовані
- Неможливо змінити без redeploy

---

#### 6. MFA для всіх користувачів
**Чому критично:**
- Захист від S1 (підміна лікаря) навіть при зламаному паролі
- 90% успішних атак використовують вкрадені credentials
- Compliance requirement для privileged accounts

**Для кого обов'язково:**
- Лікарі (доступ до PHI)
- Медсестри
- Адміністратори (критично!)
- Фармацевти

**Методи:**
- TOTP (Google Authenticator) — мінімум
- SMS (краще ніж нічого)
- Hardware tokens (YubiKey) — для адмінів
- Biometric + PIN

---

#### 7. RBAC з Least Privilege
**Чому критично:**
- Захист від E1 (elevation of privilege), I3 (insider threats)
- Кожен користувач має **тільки необхідний мінімум** прав

**Критичні правила:**
```yaml
# ❌ ПОГАНО
admin:
  permissions: ["*"]  # Все дозволено, включно з доступом до PHI

# ✅ ДОБРЕ
admin:
  permissions:
    - manage:users
    - configure:system
  constraints:
    - no_patient_data_access  # Адмін НЕ має доступу до даних пацієнтів!
    
doctor:
  permissions:
    - read:patient_records
  constraints:
    - own_patients_only  # Тільки свої пацієнти
```

**Принцип:** Адміністратор системи ≠ доступ до медичних даних

---

#### 8. Encrypted Offline Backups
**Чому критично:**
- Захист від D2 (ransomware) — найбільша загроза для healthcare
- Online backup також шифрується ransomware
- Offline копія = єдиний спосіб відновлення

**3-2-1 правило:**
- **3** копії даних
- **2** різні типи носіїв (диск + tape)
- **1** копія offline (відключена від мережі)

**Наслідки відсутності:**
- Ransomware → втрата всіх даних
- Неможливість лікування пацієнтів
- Потенційні смерті

---

## 🟡 Бажані заходи (NICE TO HAVE)

### Покращують безпеку, але система може працювати без них:

#### 1. Hardware Security Module (HSM)
**Альтернатива:** AWS KMS (також FIPS 140-2, але Level 2 vs Level 3)

**Переваги HSM:**
- FIPS 140-2 **Level 3/4** (vs KMS Level 2)
- Tamper-resistant — фізичне знищення при втручанні
- Найвищий рівень захисту

**Недоліки:**
- Дорого ($10,000-$100,000+ за HSM)
- Складніше в управлінні
- Потрібна фізична інфраструктура

**Коли потрібен:**
- Дуже великі клініки (>100,000 пацієнтів)
- Високорегульовані середовища
- Державні медичні установи

---

#### 2. UEBA (User and Entity Behavior Analytics)
**Альтернатива:** Rule-based alerting

**Переваги:**
- ML виявлення аномалій (insider threats)
- Виявлення невідомих загроз
- Автоматична baseline побудова

**Недоліки:**
- Дорого
- Потребує expertise для налаштування
- False positives

**Приклад:**
```yaml
# Rule-based (простіше)
if records_accessed > 100 in 1_hour:
    alert("Mass data access")

# UEBA (складніше, але краще)
if user_behavior != normal_baseline:
    alert("Anomaly detected")
```

---

#### 3. Zero Trust Network Architecture
**Альтернатива:** Традиційний perimeter security (firewall)

**Переваги:**
- Краще для insider threats
- "Never trust, always verify"
- Мікросегментація

**Недоліки:**
- Складніше впровадити
- Потребує зміни архітектури
- Вища вартість

---

#### 4. Database Activity Monitoring (DAM)
**Альтернатива:** Application-level logging

**Переваги:**
- Моніторинг всіх SQL запитів у реальному часі
- Виявлення SQL injection
- Виявлення аномальних запитів

**Недоліки:**
- Performance overhead
- Додаткові витрати
- Можна замінити WAF + application logging

---

#### 5. Data Loss Prevention (DLP)
**Альтернатива:** Policy enforcement + training

**Переваги:**
- Автоматична блокування витоків (email, USB, cloud)
- Виявлення PHI у незашифрованих файлах

**Недоліки:**
- Дорого
- Багато false positives
- Можна замінити strong policies

---

#### 6. Tokenization (замість шифрування)
**Альтернатива:** Field-level encryption

**Переваги:**
- Менше PCI DSS scope (якщо токенізувати card numbers)
- Формат зберігається (можна використовувати в звітах)

**Недоліки:**
- Потребує tokenization service
- Складніше
- Encryption достатньо для більшості випадків

---

## ❌ Помилки, яких слід уникати

### 1. Hardcoded Secrets у коді
```python
# ❌ КРИТИЧНА ПОМИЛКА
JWT_SECRET = "my-secret-key-123"
DB_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"
```

**Чому небезпечно:**
- Git history зберігає секрети назавжди
- GitHub leak = всі секрети публічні
- Неможливо змінити без redeploy всіх систем

**Правильно:**
```python
# ✅
JWT_SECRET = os.getenv("JWT_SECRET")  # З змінних оточення
DB_PASSWORD = vault.get("db/creds")    # З Vault (динамічні)
```

---

### 2. Fixed IV/Nonce для шифрування
```python
# ❌ КАТАСТРОФА! Повна компрометація ключа!
iv = b'0000000000000000'  # Fixed IV
cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
ciphertext = cipher.encrypt(data)
```

**Чому катастрофічно:**
- З GCM режимом: fixed nonce = можливість **відновити ключ**!
- З CBC режимом: однакові блоки видно у ciphertext
- Два повідомлення з одним nonce → XOR дає plaintext

**Правильно:**
```python
# ✅ Випадковий nonce для КОЖНОЇ операції
nonce = os.urandom(12)  # 96 біт для GCM
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
ciphertext = cipher.encrypt(data)
# Зберігати nonce разом з ciphertext
```

---

### 3. Використання MD5/SHA-1 для паролів
```python
# ❌ ПОГАНО - зламується за секунди
password_hash = hashlib.md5(password.encode()).hexdigest()
password_hash = hashlib.sha1(password.encode()).hexdigest()

# ❌ ТАКОЖ ПОГАНО - SHA-256 швидкий, GPU атаки ефективні
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

**Правильно:**
```python
# ✅ Argon2id
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
password_hash = ph.hash(password)
```

---

### 4. Відсутність HTTPS / використання HTTP
```python
# ❌ КРИТИЧНА ПОМИЛКА
http://api.medical-records.com/patients/12345
```

**Чому небезпечно:**
- Пароль передається у plaintext
- Діагнози видно у Wireshark
- MITM атака — підміна даних

**Правильно:**
```python
# ✅ Завжди HTTPS + HSTS
https://api.medical-records.com/patients/12345
# + HSTS header щоб браузер ніколи не використовував HTTP
```

---

### 5. Логування чутливих даних
```python
# ❌ ВИТІК PHI через логи
logger.info(f"Patient {patient.name} diagnosed with {patient.diagnosis}")
logger.debug(f"SSN: {patient.ssn}, Card: {patient.credit_card}")
```

**Правильно:**
```python
# ✅ Логувати тільки ID, не PHI
logger.info(f"Patient record accessed: patient_id={patient.id}")
logger.audit(f"Diagnosis created: patient_id={patient.id}, doctor_id={doctor.id}")
```

---

### 6. SQL запити без параметризації
```python
# ❌ SQL INJECTION
query = f"SELECT * FROM patients WHERE id = {patient_id}"
db.execute(query)

# ❌ ТАКОЖ НЕБЕЗПЕЧНО
query = "SELECT * FROM patients WHERE name = '" + patient_name + "'"
```

**Правильно:**
```python
# ✅ Prepared statements / Parametrized queries
query = "SELECT * FROM patients WHERE id = ?"
db.execute(query, (patient_id,))

# ✅ Або ORM
Patient.objects.get(id=patient_id)
```

---

### 7. Відсутність rate limiting
```python
# ❌ Дозволяє brute-force
@app.route('/login', methods=['POST'])
def login():
    # Без ліміту спроб
    if check_password(username, password):
        return token
```

**Правильно:**
```python
# ✅ Rate limiting
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Максимум 5 спроб за хвилину
def login():
    if check_password(username, password):
        return token
    else:
        attempts += 1
        if attempts >= 5:
            block_ip(request.remote_addr, duration=3600)
```

---

### 8. Надмірні права доступу
```yaml
# ❌ ПОГАНО - DBA має доступ до незашифрованих даних
database_admin:
  permissions: ["*"]
  access_to: "all_databases"

# ❌ ПОГАНО - Application має admin права
app_user:
  permissions: ["CREATE", "DROP", "ALTER"]
```

**Правильно:**
```yaml
# ✅ Least privilege
database_admin:
  permissions: ["ADMIN"]
  constraints:
    - no_access_to_patient_data  # Технічне адміністрування ≠ доступ до даних

app_user:
  permissions: ["SELECT", "INSERT", "UPDATE"]  # Тільки необхідне
  tables: ["patients", "appointments"]
```

---

### 9. Незашифровані backups
```bash
# ❌ ПОГАНО - backup без шифрування
mysqldump database > backup.sql
aws s3 cp backup.sql s3://backups/
```

**Правильно:**
```bash
# ✅ Шифрування перед backup
mysqldump database | gpg --encrypt --recipient backup-key > backup.sql.gpg
aws s3 cp backup.sql.gpg s3://backups/ --sse aws:kms
```

---

### 10. Відсутність MFA для privileged accounts
```yaml
# ❌ КРИТИЧНА ПОМИЛКА - адмін без MFA
admin_account:
  username: "admin"
  password: "strong-password-123"
  mfa: false  # ❌
```

**Правильно:**
```yaml
# ✅ MFA обов'язковий для адмінів
admin_account:
  username: "admin"
  password: "strong-password-123"
  mfa: true
  mfa_method: "hardware_token"  # YubiKey
  bypass_allowed: false
```

---

## Фінальний чекліст безпеки

### Перед production запуском перевірте:

**Шифрування:**
- [ ] ✅ AES-256-GCM для всіх PHI/PII
- [ ] ✅ TLS 1.3 на всіх endpoints
- [ ] ✅ Випадковий nonce/IV для кожної операції
- [ ] ✅ Encrypted backups (включно з offline)

**Паролі та автентифікація:**
- [ ] ✅ Argon2id для паролів
- [ ] ✅ MFA для всіх користувачів
- [ ] ✅ Session timeout (15-30 хвилин)
- [ ] ✅ Rate limiting на login endpoint

**Ключі та секрети:**
- [ ] ✅ Ніяких hardcoded secrets
- [ ] ✅ Всі ключі в KMS/Vault
- [ ] ✅ Автоматична ротація (90 днів)
- [ ] ✅ Pepper для паролів у HSM/Vault

**Логування та моніторинг:**
- [ ] ✅ Immutable audit logs
- [ ] ✅ Логування всіх доступів до PHI
- [ ] ✅ Real-time alerting
- [ ] ✅ 7 років retention (HIPAA)

**Контроль доступу:**
- [ ] ✅ RBAC налаштований
- [ ] ✅ Least privilege principle
- [ ] ✅ Адміни БЕЗ доступу до PHI
- [ ] ✅ ABAC для emergency access

**Захист коду:**
- [ ] ✅ Prepared statements (NO SQL injection)
- [ ] ✅ Input validation
- [ ] ✅ Output encoding (NO XSS)
- [ ] ✅ CSRF tokens

**Compliance:**
- [ ] ✅ HIPAA checklist пройдено
- [ ] ✅ GDPR права реалізовані
- [ ] ✅ Penetration testing виконано
- [ ] ✅ Security training для персоналу

**Incident Response:**
- [ ] ✅ Incident response plan готовий
- [ ] ✅ Breach notification процедури
- [ ] ✅ Automated response rules
- [ ] ✅ Contact list актуальний

---

## Підсумок

### 🔴 ТОП-3 найважливіших:
1. **Шифрування всіх PHI** — AES-256-GCM + TLS 1.3
2. **Ніколи hardcoded secrets** — тільки KMS/Vault
3. **Immutable audit logs** — 7 років, HIPAA requirement

### 🟡 Найнебезпечніші помилки:
1. **Fixed IV/nonce з GCM** — повна компрометація ключа
2. **MD5/SHA-1 для паролів** — зламується за секунди
3. **Незашифровані backups** — найлегша ціль для ransomware

### ✅ Пам'ятайте:
> У медицині помилка в безпеці може коштувати життя пацієнта.
> Не економте на безпеці медичних даних!

---

**Дата створення:** Грудень 2025  
**Статус:** ✅ Готово до здачі  
**Compliance:** HIPAA ✅ | GDPR ✅ | PCI DSS ✅ | SOC 2 ✅
