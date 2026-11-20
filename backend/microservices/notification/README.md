# notification microservice

Python / FastAPI microservice, **no database**, with Swagger documentation generated automatically.
It exposes one endpoint for now; the notification logic is a TODO for students (see [TODO.md](TODO.md)).

## Run
```bash
cd chemin\vers\notification

# 1. Créer et activer l'environnement virtuel (une seule fois)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Installer les dépendances
python -m pip install -r requirements.txt

# 3. Lancer le microservice
python -m uvicorn app.main:app --reload --port 8084   # or: python -m app.main
```
- API: http://localhost:8084/api/notifications/hello
- Swagger UI: http://localhost:8084/swagger-ui
- OpenAPI JSON: http://localhost:8084/v3/api-docs
- ReDoc: http://localhost:8084/redoc

Port `8084` (candidat = 8081, job = 8082, meeting = 8083).

## Eureka (service discovery)
The service registers itself in Eureka as **NOTIFICATION** at FastAPI startup (`lifespan`, `app/eureka.py`,
library `py-eureka-client`) and stops the Eureka client at shutdown. Start the Eureka server first (http://localhost:8761).

The port is read from the `PORT` variable. Two instances (two terminals):
```powershell
# PowerShell
$env:PORT=8084; python -m uvicorn app.main:app --port 8084
$env:PORT=8094; python -m uvicorn app.main:app --port 8094
```
```bash
# bash
PORT=8084 python -m uvicorn app.main:app --port 8084
PORT=8094 python -m uvicorn app.main:app --port 8094
```
> `PORT` (Eureka registration) and `--port` (uvicorn) must have the same value. `python -m app.main` uses `PORT` for both.

| Variable | Default | Role |
|---|---|---|
| `PORT` | 8084 | port of this instance |
| `EUREKA_SERVER` | http://localhost:8761/eureka | Eureka server URL |
| `INSTANCE_HOST` / `INSTANCE_IP` | localhost / 127.0.0.1 | address published in Eureka |
| `EUREKA_ENABLED` | true | `false` = do not register (used by the tests) |

## Endpoint
| Method | Path | Response |
|---|---|---|
| GET | /api/notifications/hello | `200 {"message": "hello I'm microservice notification"}` |

## Tests
```bash
pip install -r requirements-dev.txt
pytest
```

## Structure
```
notification/
├── app/
│   ├── main.py                    FastAPI app + Swagger config
│   ├── eureka.py                  Eureka client (register / stop)
│   ├── schemas.py                 Pydantic models (validation + Swagger schemas)
│   └── routers/notification.py    /api/notifications routes (hello + TODO)
├── tests/test_hello.py, tests/test_eureka.py, tests/conftest.py
├── TODO.md                        work for students
├── requirements.txt / requirements-dev.txt
└── pytest.ini
```
