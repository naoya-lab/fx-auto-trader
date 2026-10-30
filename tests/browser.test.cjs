const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

function app() {
  const html = fs.readFileSync(new URL('../index.html', `file://${__filename}`), 'utf8');
  const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
  const nodes = new Map();
  const defaults = { fast: '1', slow: '2', pip: '1', spread: '1', slippage: '.5', units: '10' };
  const get = id => {
    if (!nodes.has(id)) nodes.set(id, { value: defaults[id] || '', textContent: '', innerHTML: '', addEventListener() {} });
    return nodes.get(id);
  };
  const context = vm.createContext({ document: { getElementById: get } });
  vm.runInContext(script, context);
  const closes = [3, 2, 1, 4, 5, 1, 1];
  get('csv').value = 'timestamp,open,high,low,close\n' + closes.map((n, i) =>
    `${i === 4 ? '<img src=x onerror=alert(1)>' : 'day-' + i},${n},${n},${n},${n}`).join('\n');
  return { get, run: () => vm.runInContext('run()', context) };
}

test('CSV timestamps are displayed as text instead of executable HTML', () => {
  const { get, run } = app();
  run();
  assert.equal(get('error').textContent, '');
  assert.ok(get('trades').innerHTML.includes('&lt;img src=x onerror=alert(1)&gt;'));
  assert.ok(!get('trades').innerHTML.includes('<img'));
});

test('nonfinite browser costs produce a validation error instead of a result', () => {
  for (const id of ['spread', 'slippage']) {
    for (const value of ['NaN', 'Infinity', '-Infinity']) {
      const { get, run } = app();
      get(id).value = value;
      run();
      assert.match(get('error').textContent, /コスト/);
    }
  }
});
