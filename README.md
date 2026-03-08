# PromptVault - Adrian Krysiak (94706)

Projekt natywnej aplikacji chmurowej realizowany w architekturze 3-warstwowej.

## Deklaracja Architektury (Mapowanie Azure)

Ten projekt został zaplanowany z myślą o usługach PaaS (Platform as a Service) w chmurze Azure.

| Warstwa | Komponent Lokalny | Usługa Azure |
| :--- | :--- | :--- |
| **Presentation** | React 19 (Vite) | Azure Static Web Apps |
| **Application** | API (Python 3.13 / Django DRF) | Azure App Service |
| **Data** | PostgreSQL (Dev) | Azure Database for PostgreSQL |
| **Storage** | Lokalny system plików | Azure Blob Storage |

## 🏗 Status Projektu i Dokumentacja

* [x] **Artefakt 1:** Zaplanowano strukturę folderów i diagram C4 (dostępny w `/docs`).
* [X] **Artefakt 2:** Środowisko wielokontenerowe uruchomione lokalnie (Docker Compose).
* [X] **Artefakt 3:** Utworzono Frontend w podstawowej wersji
* [] **Artefakt 4:** Backend

> **Informacja:** Ten plik będzie ewoluował. W kolejnych etapach dodam tutaj sekcje 'Quick Start', opis zmiennych środowiskowych oraz instrukcję wdrożenia (CI/CD).

## Quick Start (Docker Compose)

Uruchamiaj polecenia z katalogu glownego projektu (`PromptVault/`).

1. Start kontenerow:

```bash
make up
```

2. Migracje Django:

```bash
make init
```

3. Utworzenie konta admina:

```bash
make admin
```

4. Adresy w przegladarce:

```text
Frontend: http://localhost:8080
Backend API: http://localhost:8081/api/prompts/
Panel admina: http://localhost:8081/admin/
```

Dodatkowe skroty:

```bash
make logs   # podglad logow
make down   # zatrzymanie kontenerow
make urls   # wyswietlenie adresow
make reset  # restart + migracje od zera (usuwa wolumen bazy)
```
