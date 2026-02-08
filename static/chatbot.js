(() => {
  const API_URL = 'http://127.0.0.1:8000/chat';

  const form = document.getElementById('chat-form');
  const input = document.getElementById('query-input');
  const answerEl = document.getElementById('answer');
  const linksEl = document.getElementById('links');
  const convEl = document.getElementById('conversation');

  function appendMessage(text, who='bot') {
    const d = document.createElement('div');
    d.className = `msg ${who}`;
    d.textContent = text;
    convEl.appendChild(d);
    convEl.scrollTop = convEl.scrollHeight;
  }

  async function sendQuery(q) {
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q })
      });
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();
      return data;
    } catch (err) {
      return { error: err.message };
    }
  }

  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const q = input.value.trim();
    if (!q) return;
    appendMessage(q, 'user');
    input.value = '';
    answerEl.textContent = 'Thinking...';
    linksEl.innerHTML = '';

    const result = await sendQuery(q);
    if (result.error) {
      answerEl.textContent = `Error: ${result.error}`;
      return;
    }

    const { answer, links } = result;
    answerEl.textContent = answer || 'No answer returned.';
    linksEl.innerHTML = '';
    if (Array.isArray(links) && links.length) {
      for (const l of links) {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = l;
        a.target = '_blank';
        a.rel = 'noopener noreferrer';
        a.textContent = l;
        li.appendChild(a);
        linksEl.appendChild(li);
      }
    }
  });

})();
