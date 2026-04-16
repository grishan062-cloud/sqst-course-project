# Урок 4: Интеграция SonarQube с CI/CD (GitLab, Jenkins)

## Что добавлено в этом уроке

| Файл | Описание |
|------|---------|
| `Jenkinsfile` | Конфигурация Jenkins pipeline для автоматизированного сканирования |

## Структура проекта

```
github_project/
├── docker-compose.yml
├── Jenkinsfile
├── setup-check.sh
├── scan.sh
├── sonar-project.properties
└── vulnerable-app/
    ├── app.py
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

5. Выполните сканирование проекта:
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

## Требования

- **Docker** и Docker Compose
- **Оперативная память**: минимум 4GB, рекомендуется 8GB
- **Свободное место на диске**: минимум 5GB
- **Порт 9000** должен быть свободен для SonarQube
- **Jenkins** или **GitLab CI** для использования pipeline конфигураций

## Описание компонентов

### Jenkinsfile
Декларативная Jenkins pipeline для автоматизированного запуска сканирования SonarQube при каждом коммите, с интеграцией в CI/CD процесс.
