# Урок 9: Анализ open-source компонентов и зависимостей

## Что добавлено в этом уроке

| Файл | Описание |
|------|---------|
| `vulnerable-app/requirements.txt` | Файл зависимостей Python с известными CVE |

## Структура проекта

```
github_project/
├── docker-compose.yml
├── Jenkinsfile
├── fp-analysis.md
├── hotspot-review.md
├── quality-gate.json
├── setup-check.sh
├── setup-quality-gate.sh
├── scan.sh
├── sonar-project.properties
├── frontend/
│   ├── app.js
│   └── sonar-project.properties
└── vulnerable-app/
    ├── app.py
    ├── requirements.txt
    └── utils.py
```

## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd github_project
   ```

2. Проверьте предварительные требования:
   ```bash
   bash setup-check.sh
   ```

3. Запустите SonarQube:
   ```bash
   docker compose up -d
   ```

4. Откройте SonarQube в браузере:
   ```
   http://localhost:9000
   ```

5. Установите Quality Gate:
   ```bash
   bash setup-quality-gate.sh
   ```

6. Выполните сканирование проекта:
   ```bash
   bash scan.sh
   ```

## Эволюция проекта

| Урок | Название | Новые файлы |
|------|----------|------------|
| 1 | Введение в SonarQube и его роль в безопасности | docker-compose.yml, setup-check.sh, sonar-project.properties, vulnerable-app/app.py |
| 2 | Быстрый старт: установка SonarQube и локальное сканирование | scan.sh, vulnerable-app/utils.py |
| 3 | Основы SAST, OWASP Top 10 и Secure SDLC | (без новых файлов) |
| 4 | Интеграция SonarQube с CI/CD (GitLab, Jenkins) | Jenkinsfile |
| 5 | Кастомизация Quality Gate, правил и работа с замечаниями | quality-gate.json, setup-quality-gate.sh |
| 6 | False Positive / False Negative: системный подход | fp-analysis.md |
| 7 | Security Hotspots и митигация уязвимостей | hotspot-review.md |
| 8 | Анализ разных языков и фреймворков | frontend/app.js, frontend/sonar-project.properties |
| 9 | Анализ open-source компонентов и зависимостей | vulnerable-app/requirements.txt |

## Требования

- **Docker** и Docker Compose
- **Оперативная память**: минимум 4GB, рекомендуется 8GB
- **Свободное место на диске**: минимум 5GB
- **Порт 9000** должен быть свободен для SonarQube

## Описание компонентов

### vulnerable-app/requirements.txt
Файл зависимостей Python проекта, содержащий версии пакетов с известными CVE (Common Vulnerabilities and Exposures) для демонстрации возможностей SonarQube в анализе уязвимостей в open-source компонентах.
