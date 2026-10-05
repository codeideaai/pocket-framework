// Enhance native Quarto pages; article text and language links work without JS.
(() => {
  const en = document.querySelector('meta[name="pocket-english"]')?.content;
  const zh = document.querySelector('meta[name="pocket-chinese"]')?.content;
  document.querySelectorAll('.navbar a').forEach(link => {
    const label = link.textContent.trim();
    if (label === 'English' && en) link.href = en;
    if (label === '中文' && zh) link.href = zh;
  });
  // Keep links saved from the former hash-based reader useful.
  const legacy = location.hash.match(/^#\/(en|zh)(?:\/([a-z0-9-]+))?$/);
  if (legacy && /\/(?:index\.html)?$/.test(location.pathname)) {
    const ids = ['00-start','01-request','02-routing','03-response','04-input','05-middleware','06-cancellation','07-storage','08-tests','09-lifecycle','10-persistence','11-workflow','12-browser','13-finish'];
    if (legacy[2] && ids.includes(legacy[2])) location.replace(`${legacy[1]}/${legacy[2]}.html`);
    else if (legacy[1] === 'zh') location.replace('zh.html');
  }
  const id = document.querySelector('meta[name="pocket-chapter"]')?.content;
  if (!id) return;
  const chinese = document.documentElement.lang.startsWith('zh');
  let completed = [];
  try { const value = JSON.parse(localStorage.getItem('pocket-completed') || '[]'); if (Array.isArray(value)) completed = value; } catch {}
  const box = document.createElement('div'); box.className = 'reading-progress';
  const button = document.createElement('button'); button.type = 'button'; button.className = 'btn btn-outline-primary';
  const status = document.createElement('small'); status.setAttribute('role', 'status');
  function update() { const done = completed.includes(id); button.setAttribute('aria-pressed', String(done)); button.textContent = chinese ? (done ? '✓ 已读完' : '标记为已读') : (done ? '✓ Completed' : 'Mark as complete'); }
  update();
  button.addEventListener('click', () => {
    completed = completed.includes(id) ? completed.filter(x => x !== id) : [...completed, id]; update();
    try { localStorage.setItem('pocket-completed', JSON.stringify(completed)); status.textContent = chinese ? '进度已保存在当前浏览器。' : 'Progress saved in this browser.'; }
    catch { status.textContent = chinese ? '本次会话已记录；浏览器存储不可用。' : 'Recorded for this session; browser storage is unavailable.'; }
  });
  box.append(button, status); document.querySelector('main').append(box);
})();
