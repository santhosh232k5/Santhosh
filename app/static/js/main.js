const api = async (url, method = 'GET', body = null, auth = true) => {
  const headers = { 'Content-Type': 'application/json' };
  const token = localStorage.getItem('token');
  if (auth && token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : null });
  return res.json();
};

const services = ["Electrical Works","Plumbing","Carpentry","Painting","Masonry","Cleaning","Appliance Repair"];
const serviceContainer = document.getElementById('services');
if (serviceContainer) {
  services.forEach(s => {
    const div = document.createElement('div');
    div.className = 'service-card';
    div.innerHTML = `<h4>${s}</h4><p>Professional ${s.toLowerCase()} experts near you.</p>`;
    serviceContainer.appendChild(div);
  });
}

document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = Object.fromEntries(new FormData(e.target).entries());
  const payload = { role: form.role, password: form.password };
  if (form.role === 'admin') payload.username = form.email; else payload.email = form.email;
  const data = await api('/api/auth/login', 'POST', payload, false);
  if (data.access_token) { localStorage.setItem('token', data.access_token); alert('Login success'); }
  else alert(data.error || 'Login failed');
});

document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = Object.fromEntries(new FormData(e.target).entries());
  alert((await api('/api/auth/register', 'POST', form, false)).message || 'Done');
});

document.getElementById('workerRegisterForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = Object.fromEntries(new FormData(e.target).entries());
  alert((await api('/api/auth/register-worker', 'POST', form, false)).message || 'Done');
});

document.getElementById('bookingForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = Object.fromEntries(new FormData(e.target).entries());
  document.getElementById('bookingOutput').textContent = JSON.stringify(await api('/api/bookings', 'POST', form), null, 2);
});

document.getElementById('loadBookings')?.addEventListener('click', async () => {
  document.getElementById('bookingOutput').textContent = JSON.stringify(await api('/api/bookings'), null, 2);
});

document.getElementById('loadWorkerDashboard')?.addEventListener('click', async () => {
  document.getElementById('workerOutput').textContent = JSON.stringify(await api('/api/workers/dashboard'), null, 2);
});

document.getElementById('loadAdminDashboard')?.addEventListener('click', async () => {
  document.getElementById('adminOutput').textContent = JSON.stringify(await api('/api/admin'), null, 2);
});

const panel = document.getElementById('chatPanel');
document.getElementById('chatToggle')?.addEventListener('click', () => panel.classList.toggle('hidden'));
document.getElementById('chatSend')?.addEventListener('click', async () => {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;
  const box = document.getElementById('chatMessages');
  box.innerHTML += `<p><b>You:</b> ${msg}</p>`;
  const data = await api('/api/chatbot', 'POST', { message: msg }, false);
  box.innerHTML += `<p><b>Bot:</b> ${data.reply || JSON.stringify(data)}</p>`;
  input.value = '';
});
