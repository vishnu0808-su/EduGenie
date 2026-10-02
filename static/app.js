const task = document.getElementById('task');
const inputText = document.getElementById('inputText');
const submitBtn = document.getElementById('submitBtn');
const result = document.getElementById('result');
const status = document.getElementById('status');
const copyBtn = document.getElementById('copyBtn');

const taskMeta = {
  qa: { endpoint: '/qa', label: 'question', placeholder: 'Example: Which is the largest ocean? Explain briefly.' },
  explain: { endpoint: '/explain', label: 'concept', placeholder: 'Example: Explain the Pythagoras theorem in simple words.' },
  quiz: { endpoint: '/quiz', label: 'topic or passage', placeholder: 'Example: Photosynthesis: plants use light energy to make food...' },
  summarize: { endpoint: '/summarize', label: 'passage', placeholder: 'Paste the educational passage you want summarized.' },
  learn: { endpoint: '/learn/recommendations', label: 'topic', placeholder: 'Example: SQL from beginner to advanced.' }
};

task.addEventListener('change', () => {
  inputText.placeholder = taskMeta[task.value].placeholder;
  result.textContent = 'Your AI-generated result will appear here.';
  result.className = 'result muted';
  copyBtn.disabled = true;
});

function escapeHtml(value) {
  return String(value).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

function renderQuiz(quiz) {
  return quiz.map((q, i) => `
    <article class="quiz-item">
      <h3>${i + 1}. ${escapeHtml(q.question)}</h3>
      ${q.options.map(option => `<div class="option ${option === q.correct_answer ? 'correct' : ''}">${escapeHtml(option)}</div>`).join('')}
      <div class="explanation"><strong>Answer:</strong> ${escapeHtml(q.correct_answer)}<br>${escapeHtml(q.explanation)}</div>
    </article>
  `).join('');
}

submitBtn.addEventListener('click', async () => {
  const text = inputText.value.trim();
  if (!text) {
    status.textContent = `Please enter a ${taskMeta[task.value].label}.`;
    return;
  }

  submitBtn.disabled = true;
  copyBtn.disabled = true;
  status.textContent = 'Generating...';
  result.textContent = '';
  result.className = 'result';

  try {
    const response = await fetch(taskMeta[task.value].endpoint, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(task.value === 'qa' ? {question: text} : {text})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed.');

    if (task.value === 'quiz') {
      result.innerHTML = renderQuiz(data.result);
    } else {
      result.textContent = data.result;
    }
    copyBtn.disabled = false;
    status.textContent = 'Done.';
  } catch (error) {
    result.textContent = error.message;
    status.textContent = 'Something went wrong.';
  } finally {
    submitBtn.disabled = false;
  }
});

copyBtn.addEventListener('click', async () => {
  const text = result.innerText.trim();
  if (!text) return;
  await navigator.clipboard.writeText(text);
  status.textContent = 'Copied to clipboard.';
});
