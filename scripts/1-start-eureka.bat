@echo off
cd /d "%~dp0..\backend\eureka"
start "EUREKA 8761" cmd /k mvn spring-boot:run
