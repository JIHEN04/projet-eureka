@echo off
set BASE=%~dp0..\backend\microservices
start "CANDIDAT 8091" cmd /k "cd /d %BASE%\candidat && mvn spring-boot:run -Dspring-boot.run.arguments=--server.port=8091"
start "MEETING 8093" cmd /k "cd /d %BASE%\meeting && set PORT=8093&& npm start"
start "NOTIFICATION 8094" cmd /k "cd /d %BASE%\notification && set PORT=8094&& uvicorn app.main:app --port 8094"
