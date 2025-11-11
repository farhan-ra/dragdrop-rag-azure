const chatContainer = document.getElementById('chat-container');
const inputField = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

async function sendMessage() {
  const userText = inputField.value.trim();
  if (!userText) return;

  appendMessage('user', userText);
  inputField.value = '';

  const response = await fetch('/chat/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: userText })
  });

  const data = await response.json();
  const msgDiv = appendMessage('assistant', data.reply || 'No response.');

  if (data.sources && data.sources.length > 0) {
    const toggle = document.createElement('div');
    toggle.className = 'toggle-btn';
    toggle.innerText = 'Show sources';
    const srcDiv = document.createElement('div');
    srcDiv.className = 'sources';

    srcDiv.innerHTML = data.sources.map(s => {
      if (typeof s === 'string') return `<div>${s}</div>`;
      const title = s.title || 'Source';
      const url = s.url ? `<a href="${s.url}" target="_blank">${title}</a>` : `<strong>${title}</strong>`;
      const snippet = s.content ? `<p>${s.content}</p>` : '';
      return `<div>${url}${snippet}</div>`;
    }).join('');

    toggle.addEventListener('click', () => {
      srcDiv.style.display = srcDiv.style.display === 'none' ? 'block' : 'none';
      toggle.innerText = srcDiv.style.display === 'none' ? 'Show sources' : 'Hide sources';
    });

    msgDiv.appendChild(toggle);
    msgDiv.appendChild(srcDiv);
  }
}

function appendMessage(role, text) {
  const msg = document.createElement('div');
  msg.className = `${role} message`;
  msg.textContent = text;
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  return msg;
}

sendBtn.addEventListener('click', sendMessage);
inputField.addEventListener('keydown', e => {
  if (e.key === 'Enter') sendMessage();
});
