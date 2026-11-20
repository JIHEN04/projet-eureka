# eureka — serveur de découverte (Netflix Eureka)

Spring Boot 3.5 / Spring Cloud 2025.0 / Java 17. Registre de toutes les instances de microservices.

## Lancer
```bash
mvn spring-boot:run
```
Dashboard : http://localhost:8761

Au démarrage, le dashboard affiche **« No instances available »** : aucun microservice n'est encore enregistré.

## Configuration (`src/main/resources/application.properties`)
```properties
spring.application.name=eureka
server.port=8761
eureka.client.register-with-eureka=false
eureka.client.fetch-registry=false
```
- `register-with-eureka=false` : le serveur ne s'enregistre pas lui-même.
- `fetch-registry=false` : le serveur ne met pas le registre en cache local (c'est lui le registre).

## Code
`EurekaApplication.java` porte `@SpringBootApplication` + **`@EnableEurekaServer`**.

## API REST d'Eureka (utile pour Node.js / Python)
| Méthode | URL | Rôle |
|---|---|---|
| GET | `/eureka/apps` | liste de toutes les applications et instances |
| GET | `/eureka/apps/{APP}` | instances d'une application |
| POST | `/eureka/apps/{APP}` | enregistrement d'une instance |
| PUT | `/eureka/apps/{APP}/{instanceId}` | heartbeat (toutes les 30 s) |
| DELETE | `/eureka/apps/{APP}/{instanceId}` | désenregistrement |

Sans heartbeat pendant 90 s, l'instance est retirée du registre.
