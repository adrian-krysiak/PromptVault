# PromptVault - Adrian Krysiak (94706)

Projekt natywnej aplikacji chmurowej realizowany w architekturze 3-warstwowej.

## Deklaracja Architektury (Mapowanie Azure)

Ten projekt został zaplanowany z myślą o usługach PaaS (Platform as a Service) w chmurze Azure.

| Warstwa | Komponent Lokalny | Usługa Azure |
| :--- | :--- | :--- |
| **Presentation** | React 19 (Vite) + Nginx | Azure Static Web Apps / App Service |
| **Application** | API (Python 3.13 / Django DRF + Gunicorn) | Azure App Service |
| **Data** | PostgreSQL 18 | Azure Database for PostgreSQL |
| **Storage** | Lokalny system plików | Azure Blob Storage |
| **Reverse Proxy** | Nginx | Azure Application Gateway / Front Door |

## 🏗 Status Projektu i Dokumentacja

* [x] **Artefakt 1:** Zaplanowano strukturę folderów i diagram C4 (dostępny w `/docs`).
* [x] **Artefakt 2:** Środowisko wielokontenerowe uruchomione lokalnie (Docker Compose).
* [x] **Artefakt 3:** Utworzono Frontend w podstawowej wersji
* [x] **Artefakt 4:** Utworzono Backend w podstawowej wersji


## 🚀 Architektura Produkcyjna

Aplikacja została przygotowana z myślą o wdrożeniu produkcyjnym:

```
┌─────────────────────────────────────┐
│         Nginx (Port 80)             │  ← Reverse Proxy + Load Balancer
└─────────────────────────────────────┘
              │
              ├──→ Frontend (React/Vite) - Port 80 (internal)
              ├──→ Backend (Django/Gunicorn) - Port 8081 (internal)  
              └──→ PostgreSQL - Port 5432
```

**Komponenty produkcyjne:**
- ✅ **Nginx** - Reverse proxy, obsługa routingu, static files
- ✅ **Gunicorn** - WSGI server dla Django (4 workers, timeout 120s)
- ✅ **Django** - REST API z walidacją błędów
- ✅ **React** - SPA z szczegółową obsługą błędów HTTP
- ✅ **PostgreSQL** - Relacyjna baza danych

## Quick Start (Docker Compose)

Uruchamiaj polecenia z katalogu głównego projektu (`PromptVault/`).

### Środowisko Deweloperskie (z Makefile):

1. Start kontenerów:

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

4. Adresy w przeglądarce:

```text
Frontend: http://localhost:8080
Backend API: http://localhost:8081/api/prompts/
Panel admina: http://localhost:8081/admin/
```

Dodatkowe skróty:

```bash
make logs   # podgląd logów
make down   # zatrzymanie kontenerów
make urls   # wyświetlenie adresów
make reset  # restart + migracje od zera (usuwa wolumen bazy)
```
