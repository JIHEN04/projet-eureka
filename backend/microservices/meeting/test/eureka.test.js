// Run with: npm test
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { buildConfig, APP_NAME } = require('../src/config/eureka');

test('Eureka app name is MEETING', () => {
  assert.equal(APP_NAME, 'MEETING');
  assert.equal(buildConfig({}).instance.app, 'MEETING');
});

test('default config: port 8083 and Eureka on localhost:8761', () => {
  const cfg = buildConfig({});
  assert.equal(cfg.instance.port.$, 8083);
  assert.equal(cfg.eureka.host, 'localhost');
  assert.equal(cfg.eureka.port, 8761);
});

test('the port is read from the PORT variable (several instances)', () => {
  const a = buildConfig({ PORT: '8083' });
  const b = buildConfig({ PORT: '8093' });
  assert.equal(b.instance.port.$, 8093);
  assert.notEqual(a.instance.instanceId, b.instance.instanceId);
  assert.equal(b.instance.instanceId, 'localhost:meeting:8093');
});
