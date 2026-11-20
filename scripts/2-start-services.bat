@echo off
set BASE=%~dp0..\backend\microservices
start "CANDIDAT 8081" cmd /k "cd /d %BASE%\candidat && mvn spring-boot:run"
start "JOB 8082" cmd /k "cd /d %BASE%\job && mvn spring-boot:run"
start "CANDIDATURE 8085" cmd /k "cd /d %BASE%\canditature && mvn spring-boot:run"
start "MEETING 8083" cmd /k "cd /d %BASE%\meeting && npm install && set PORT=8083&& npm start"
start "NOTIFICATION 8084" cmd /k "cd /d %BASE%\notification && pip install -r requirements.txt && set PORT=8084&& uvicorn app.main:app --port 8084"
