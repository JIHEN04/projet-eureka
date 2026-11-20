/**
 * Eureka client configuration (eureka-js-client).
 *
 * The service registers itself under the name MEETING when the server starts,
 * and deregisters when the process stops. The port is read from the PORT
 * environment variable so that several instances can run side by side.
 *
 * Environment variables (all optional):
 *   PORT          port of this instance                (default 8083)
 *   EUREKA_HOST   host of the Eureka server            (default localhost)
 *   EUREKA_PORT   port of the Eureka server            (default 8761)
 *   INSTANCE_HOST host name published in Eureka        (default localhost)
 *   INSTANCE_IP   IP address published in Eureka       (default 127.0.0.1)
 */
const { Eureka } = require('eureka-js-client');

const APP_NAME = 'MEETING';

function buildConfig(env = process.env) {
  const port = parseInt(env.PORT || '8083', 10);
  const host = env.INSTANCE_HOST || 'localhost';
  const ip = env.INSTANCE_IP || '127.0.0.1';
  const baseUrl = `http://${host}:${port}`;

  return {
    instance: {
      app: APP_NAME,
      // unique id per instance: host:app:port (same format as Spring Boot clients)
      instanceId: `${host}:${APP_NAME.toLowerCase()}:${port}`,
      hostName: host,
      ipAddr: ip,
      port: { $: port, '@enabled': true },
      vipAddress: APP_NAME.toLowerCase(),
      statusPageUrl: `${baseUrl}/api/meetings/hello`,
      healthCheckUrl: `${baseUrl}/api/meetings/hello`,
      homePageUrl: baseUrl,
      dataCenterInfo: {
        '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
        name: 'MyOwn',
      },
    },
    eureka: {
      host: env.EUREKA_HOST || 'localhost',
      port: parseInt(env.EUREKA_PORT || '8761', 10),
      servicePath: '/eureka/apps/',
      maxRetries: 10,
      requestRetryDelay: 2000,
    },
  };
}

function createEurekaClient(env = process.env) {
  return new Eureka(buildConfig(env));
}

/** Registers the service and deregisters it on SIGINT / SIGTERM. */
function registerWithEureka(env = process.env) {
  const client = createEurekaClient(env);

  client.start((error) => {
    if (error) {
      console.error('Eureka registration failed:', error.message || error);
    } else {
      console.log(`Registered in Eureka as ${APP_NAME} (instance ${client.config.instance.instanceId})`);
    }
  });

  let stopping = false;
  const shutdown = (signal) => {
    if (stopping) return;
    stopping = true;
    console.log(`${signal} received, deregistering from Eureka...`);
    client.stop(() => process.exit(0));
    // safety net if Eureka does not answer
    setTimeout(() => process.exit(0), 3000).unref();
  };
  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGTERM', () => shutdown('SIGTERM'));

  return client;
}

module.exports = { APP_NAME, buildConfig, createEurekaClient, registerWithEureka };
