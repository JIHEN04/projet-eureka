const app = require('./app');
const { registerWithEureka } = require('./config/eureka');

// The port comes from the PORT environment variable so several instances can run:
//   PORT=8083 npm start   and   PORT=8093 npm start
const PORT = process.env.PORT || 8083;

app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);

  // Register in Eureka once the server is listening (can be disabled: EUREKA_ENABLED=false)
  if (process.env.EUREKA_ENABLED !== 'false') {
    registerWithEureka();
  }
});
