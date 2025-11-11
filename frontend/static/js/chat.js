const chatContainer = document.getElementById('chat-container');
const inputField = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');

// Drag & Drop setup
dropzone.addEventListener('click', () => fileInput.click());

dropzone.addEventListener('dragover', e => {
  e.preventDefault();
  dropzone.classList.add('dragging');
});

dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragging'));

dropzone.addEventListener('drop', e => {
  e.preventDefault();
  dropzone.classList.remove('dragging');
  handleFileUpload(e.dataTransfer.files[0]);
});

fileInput.addEventListener('change', e => {
  handleFileUpload(e.target.files[0]);
});

async function handleFileUpload(file) {
  if (!file) return;
  dropzone.textContent = `Uploading ${file.name}...`;
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch('/upload_pdf', { method: 'POST', body: formData });
  const data = await res.json();
  dropzone.textContent = `✅ Uploaded ${file.name} (${data.chunks_added} chunks)`;
}

// Chat message sending
sendBtn.addEventListener('click', sendMessage);
inputField.addEventListener('keydown', e => e.key === 'Enter' && sendMessage());

async function sendMessage() {
  const userText = inputField.value.trim();
  if (!userText) return;
  appendMessage('user', userText);
  inputField.value = '';

  const formData = new FormData();
  formData.append('message', userText);

  const res = await fetch('/chat_message', { method: 'POST', body: formData });
  const data = await res.json();
  appendMessage('assistant', data.reply);
}

function appendMessage(role, text) {
  const msgWrapper = document.createElement('div');
  msgWrapper.classList.add('message', role);
  msgWrapper.textContent = text;
  chatContainer.appendChild(msgWrapper);

  if (role === 'assistant') {
    let i = 0;
    const interval = setInterval(() => {
      msg.textContent = text.slice(0, i++);
      if (i > text.length) clearInterval(interval);
    }, 15);
  } else {
    msg.textContent = text;
  }  

  chatContainer.scrollTop = chatContainer.scrollHeight;
}
