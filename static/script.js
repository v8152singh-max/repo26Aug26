async function show(text){
  const out = document.getElementById('output');
  out.textContent = text;
}

document.getElementById('btn-calc').addEventListener('click', async () => {
  const sleep = parseFloat(document.getElementById('sleep').value) || 0.2;
  show('Running /calculate...');
  const res = await fetch('/calculate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({sleep})
  });
  const data = await res.json();
  show(JSON.stringify(data, null, 2));
});

document.getElementById('btn-dash').addEventListener('click', async () => {
  const user = document.getElementById('user').value || 'guest';
  show('Calling /dashboard...');
  const res = await fetch(`/dashboard?user=${encodeURIComponent(user)}`);
  const text = await res.text();
  show(`status: ${res.status}\n\n${text}`);
});

document.getElementById('btn-emp').addEventListener('click', async () => {
  const salary = parseInt(document.getElementById('salary').value) || 50000;
  show('Fetching /employee...');
  const res = await fetch(`/employee?salary=${salary}`);
  const data = await res.json();
  show(JSON.stringify(data, null, 2));
});

document.getElementById('btn-greet').addEventListener('click', async () => {
  show('Fetching /greet...');
  const res = await fetch('/greet');
  const data = await res.json();
  show(JSON.stringify(data, null, 2));
});
