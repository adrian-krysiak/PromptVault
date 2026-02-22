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

> **Informacja:** Ten plik będzie ewoluował. W kolejnych etapach dodam tutaj sekcje 'Quick Start', opis zmiennych środowiskowych oraz instrukcję wdrożenia (CI/CD).
