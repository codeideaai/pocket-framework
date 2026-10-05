'use strict';
const chapters = window.CHAPTERS;
const $ = id => document.getElementById(id);
const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const storage = {
  get(key, fallback) { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } },
  set(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); return true; } catch { return false; } }
};
const saved = storage.get('pocket-completed', []);
const completed = new Set(Array.isArray(saved) ? saved.filter(id => chapters.some(c => c.id === id)) : []);
const translations = {
 en: {
  edition:'A FIELD GUIDE · GO EDITION', overview:'The field guide', search:'Find a lesson…', searchLabel:'Search article titles and text', contents:'THE LEARNING PATH', progress:'Your progress', progressHint:'One small step at a time.', menu:'Menu',
  eyebrow:'FROM FIRST REQUEST TO YOUR OWN FRAMEWORK', headline:'Small steps.<br>Your own <em>framework.</em>', introduction:'A practical guide to building a little web framework in Go. Start with one request. Finish with a notebook service you can explain, line by line.', start:'Start the journey', resume:'Continue reading', promise:'Beginner friendly. Built to be understood.',
  browser:'Your browser', browserSub:'A question, sent over HTTP', framework:'Your framework', frameworkSub:'Route → validate → respond', notebook:'Your notebook', notebookSub:'One small, useful application', flowTitle:'THE BIG PICTURE', request:'request', response:'handler', flowEnd:'Small enough to understand. Real enough to use.',
  fact1:'hands-on articles', fact2:'languages, one journey', fact3:'external Go dependencies', path:'A path, not a pile of tutorials.', pathSub:'LEARN → BUILD → UNDERSTAND',
  groups:['01 / First connections','02 / A useful core','03 / Make it dependable','04 / Put it together'], groupTitles:['Meet the request','Build the small pieces','Trust what you built','Make it your own'], groupDescriptions:['From your first server to a consistent JSON response.','Input, middleware, cancellation, and a home for your data.','Tests, process lifecycle, storage design, and everyday tools.','A browser client, access boundaries, and your next release.'], groupLink:'Explore this part',
  noteTitle:'Learn by following one small application.', note:'The series uses Pocket Notes throughout. Core examples are complete Go programs; optional database, cache, and account work is clearly labeled as extension design. No framework experience needed.',
  footer:'POCKET FRAMEWORK / A hands-on learning series', printEnglish:'English edition', printChinese:'中文版', code:'Example source',
  article:'ARTICLE', minutes:'min read', level:'Beginner', onPage:'IN THIS ARTICLE', exercise:'YOUR TURN', exerciseTitle:'Try it yourself', answer:'Reveal the explanation', references:'Further reading', copy:'Copy', copied:'Copied', copyError:'Copy unavailable. Select and copy the code directly.', noResults:'No matching articles. Try “JSON”, “storage”, or “HTTP”.', mark:'Mark as complete', marked:'Completed', saved:'Saved in this browser.', notSaved:'Progress works for this session; browser storage is unavailable.', previous:'← PREVIOUS', next:'NEXT →', back:'Back to the field guide', finish:'You have reached the final article.', print:'Print article', unknown:'That article was not found. Showing the field guide.',
 },
 zh: {
  edition:'动手实践指南 · GO 专题', overview:'系列导读', search:'查找文章…', searchLabel:'搜索文章标题和正文', contents:'学习路线', progress:'你的阅读进度', progressHint:'每次前进一步。', menu:'目录',
  eyebrow:'从第一个请求，到自己的小框架', headline:'一步一步，<br>写出自己的<em>框架。</em>', introduction:'一套适合初学者的 Go Web 框架实践文章。从一个请求开始，最后做出一个你能逐行解释的笔记服务。', start:'开始学习', resume:'继续阅读', promise:'面向小白，每一步都讲清楚。',
  browser:'你的浏览器', browserSub:'通过 HTTP 发出请求', framework:'你的小框架', frameworkSub:'路由 → 校验 → 响应', notebook:'你的笔记服务', notebookSub:'一个小而完整的应用', flowTitle:'我们要搭建什么', request:'请求', response:'处理', flowEnd:'足够小，读得懂；能运行，看得到。',
  fact1:'篇动手实践文章', fact2:'种语言，同一条学习路线', fact3:'个 Go 外部依赖', path:'循序渐进，不是教程堆砌。', pathSub:'学习 → 实践 → 理解',
  groups:['01 / 建立连接','02 / 实现核心','03 / 让行为可靠','04 / 串成完整应用'], groupTitles:['认识一次请求','搭好基础部件','让代码值得信赖','把知识变成作品'], groupDescriptions:['从第一个服务器，走到一致的 JSON 响应。','输入校验、中间件、取消机制与数据存储。','测试、进程生命周期、存储设计和日常工具。','浏览器客户端、访问边界与下一次发布。'], groupLink:'进入这一部分',
  noteTitle:'用同一个小应用，把知识连起来。', note:'整个系列围绕 Pocket Notes 展开。核心示例提供完整 Go 程序；数据库、缓存和账户等可选内容会明确标注为扩展设计。不需要已有框架经验。',
  footer:'POCKET FRAMEWORK / 从理解到实践', printEnglish:'English 完整版', printChinese:'中文完整版', code:'示例源码',
  article:'第', minutes:'分钟阅读', level:'入门', onPage:'本篇内容', exercise:'动手练习', exerciseTitle:'现在，自己试一试', answer:'展开参考解释', references:'延伸阅读', copy:'复制', copied:'已复制', copyError:'暂时无法复制，请直接选中代码复制。', noResults:'没有找到文章。试试“JSON”“存储”或“HTTP”。', mark:'标记为已读', marked:'已读完', saved:'进度保存在当前浏览器。', notSaved:'本次会话会保留进度；浏览器存储暂不可用。', previous:'← 上一篇', next:'下一篇 →', back:'返回系列导读', finish:'你已经读到最后一篇。', print:'打印本篇', unknown:'未找到该文章，已显示系列导读。',
 }
};
let lang = 'en', current = null, query = '', toastTimer;
let scrollRestore = null;
function t(key) { return translations[lang][key]; }
function href(id, language=lang) { return '#/'+language+(id?'/'+id:''); }
function paragraphs(text) { return text.split(/\n\s*\n/).map(p=>`<p>${escapeHTML(p)}</p>`).join(''); }
function toast(text) { $('toast').textContent=text; $('toast').classList.add('show'); clearTimeout(toastTimer); toastTimer=setTimeout(()=>$('toast').classList.remove('show'),2500); }
function setMenu(open) { $('sidebar').classList.toggle('open',open); $('menuToggle').setAttribute('aria-expanded',String(open)); }
function readRoute() {
 const parts=location.hash.replace(/^#\/?/,'').split('/');
 lang=parts[0]==='zh'?'zh':'en';
 current=chapters.find(c=>c.id===parts[1])||null;
 if(parts[1]&&!current) toast(t('unknown'));
 if(current)storage.set('pocket-last',current.id);
}
function updateShell() {
 document.documentElement.lang=lang==='zh'?'zh-CN':'en';
 document.querySelector('.brand').href=href();
 $('overviewLink').href=href();
 $('overviewLabel').textContent=t('overview'); $('edition').textContent=t('edition');
 $('search').placeholder=t('search'); $('search').setAttribute('aria-label',t('searchLabel'));
 $('contentsLabel').textContent=t('contents'); $('progressLabel').textContent=t('progress'); $('progressHint').textContent=t('progressHint');
 $('menuToggle').querySelector('span').textContent=t('menu');
 $('progress').setAttribute('aria-label',t('progress')); $('chapterNav').setAttribute('aria-label',t('contents'));
 document.querySelectorAll('[data-lang]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.lang===lang)));
 $('progressCount').textContent=`${completed.size} / ${chapters.length}`; $('progress').value=completed.size;
 renderNav();
}
function renderNav() {
 const filtered=chapters.filter(c=>!query||[c.title.en,c.title.zh,c.deck.en,c.deck.zh,...c.sections.flatMap(s=>[s.body.en,s.body.zh])].join(' ').toLowerCase().includes(query));
 let lastGroup=-1;
 $('chapterNav').innerHTML=filtered.map(c=>{
  let group='';if(c.part!==lastGroup){group=`<div class="nav-group-label">${t('groups')[c.part]}</div>`;lastGroup=c.part;}
  return group+`<a class="chapter-link" href="${href(c.id)}" ${current?.id===c.id?'aria-current="page"':''}><span class="number">${c.id.slice(0,2)}</span><span>${escapeHTML(c.title[lang])}</span>${completed.has(c.id)?'<span class="done-dot" aria-label="'+t('marked')+'">✓</span>':''}</a>`;
 }).join('')||`<p class="empty">${t('noResults')}</p>`;
}
function footer() { return `<footer class="page-footer"><span>${t('footer')}</span><div><a href="editions/english.html">${t('printEnglish')}</a> · <a href="editions/chinese.html">${t('printChinese')}</a> · <a href="examples/notebook/mini/mini.go">${t('code')}</a></div></footer>`; }
function renderHome() {
 const last=storage.get('pocket-last',null), resume=chapters.some(c=>c.id===last);
 document.title='Pocket Framework — '+(lang==='en'?'Build it. Understand it.':'一步一步，写出自己的框架');
 $('main').innerHTML=`<section class="home-hero"><div><div class="eyebrow">${t('eyebrow')}</div><h1>${t('headline')}</h1><p class="hero-copy">${t('introduction')}</p><a class="primary" href="${href(resume?last:chapters[0].id)}">${t(resume?'resume':'start')}<span>↗</span></a><div class="hero-sub"><span class="tiny-line"></span>${t('promise')}</div></div><div class="flow-card" role="img" aria-label="${lang==='en'?'A browser request travels through your framework to the notebook application.':'浏览器请求经过框架，到达笔记应用。'}"><div class="flow-top"><span>${t('flowTitle')}</span><i></i></div><div class="flow-node"><span class="icon">↗</span><div><strong>${t('browser')}</strong><small>${t('browserSub')}</small></div></div><div class="flow-arrow">↓ <span>HTTP ${t('request')}</span></div><div class="flow-node highlight"><span class="icon">{ }</span><div><strong>${t('framework')}</strong><small>${t('frameworkSub')}</small></div></div><div class="flow-arrow">↓ <span>${t('response')}</span></div><div class="flow-node"><span class="icon">≡</span><div><strong>${t('notebook')}</strong><small>${t('notebookSub')}</small></div></div><div class="flow-caption">${t('flowEnd')}</div></div></section>
 <section class="facts" aria-label="${lang==='en'?'Series at a glance':'系列概览'}"><div class="fact"><strong>14</strong><span>${t('fact1')}</span></div><div class="fact"><strong>02</strong><span>${t('fact2')}</span></div><div class="fact"><strong>00</strong><span>${t('fact3')}</span></div></section>
 <div class="section-heading"><h2>${t('path')}</h2><span>${t('pathSub')}</span></div><div class="path-grid">${[0,1,2,3].map(part=>{const group=chapters.filter(c=>c.part===part);return `<a class="path-card" href="${href(group[0].id)}"><div class="card-top"><span>PART ${String(part+1).padStart(2,'0')}</span><span>${group[0].id.slice(0,2)} — ${group.at(-1).id.slice(0,2)}</span></div><h3>${t('groupTitles')[part]}</h3><p>${t('groupDescriptions')[part]}</p><span class="card-link">${t('groupLink')} ↗</span></a>`}).join('')}</div><aside class="study-note"><p><strong>${t('noteTitle')}</strong></p><p>${t('note')}</p></aside>${footer()}`;
}
function renderArticle() {
 const c=current,index=chapters.indexOf(c); document.title=c.title[lang]+' — Pocket Framework';
 $('main').innerHTML=`<div class="breadcrumb"><a href="${href()}">${t('overview')}</a><span>/</span><span>${t('groups')[c.part].split(' / ')[1]}</span><span>/</span><span>${c.id.slice(0,2)}</span></div><header class="article-header"><div class="eyebrow">${t('article')} ${c.id.slice(0,2)} ${lang==='zh'?'篇 / POCKET NOTES':'/ POCKET NOTES'}</div><h1>${escapeHTML(c.title[lang])}</h1><p class="article-deck">${escapeHTML(c.deck[lang])}</p><div class="article-meta"><span>${c.minutes} ${t('minutes')}</span><span class="pill">${t('level')}</span><span>Go 1.22+</span><button class="print-btn" id="printArticle">${t('print')} ↗</button></div></header><div class="article-layout"><article class="article-body">${c.sections.map((s,i)=>`<section class="article-section" id="section-${i}"><h2>${escapeHTML(s.title[lang])}</h2>${paragraphs(s.body[lang])}${s.code?`<div class="code-block"><div class="code-header"><span>${escapeHTML(localizeFilename(s.filename))}</span><button class="copy-btn" data-copy="${i}" aria-label="${t('copy')} ${escapeHTML(s.filename)}">${t('copy')}</button></div><pre><code>${escapeHTML(s.code)}</code></pre></div>`:''}</section>`).join('')}<section class="exercise" id="exercise"><div class="eyebrow">${t('exercise')}</div><h3>${t('exerciseTitle')}</h3><p>${escapeHTML(c.exercise.question[lang])}</p><details><summary>${t('answer')}</summary><p>${escapeHTML(c.exercise.answer[lang])}</p></details></section><section class="references"><h3>${t('references')}</h3>${c.references.map(r=>`<a href="${r.url}" target="_blank" rel="noopener noreferrer">${escapeHTML(r.label)} ↗</a>`).join('')}</section><div class="completion"><button class="complete-button" id="completeArticle" aria-pressed="${completed.has(c.id)}">${completed.has(c.id)?'✓ '+t('marked'):t('mark')}</button><small id="storageMessage">${t('saved')}</small></div><nav class="article-pagination" aria-label="${lang==='en'?'Article navigation':'文章导航'}">${index>0?`<a href="${href(chapters[index-1].id)}"><small>${t('previous')}</small>${escapeHTML(chapters[index-1].title[lang])}</a>`:`<a href="${href()}"><small>${t('previous')}</small>${t('back')}</a>`}${index<chapters.length-1?`<a class="next" href="${href(chapters[index+1].id)}"><small>${t('next')}</small>${escapeHTML(chapters[index+1].title[lang])}</a>`:`<a class="next" href="${href()}"><small>✓</small>${t('finish')}</a>`}</nav></article><aside class="toc"><div class="toc-label">${t('onPage')}</div>${c.sections.map((s,i)=>`<a href="#section-${i}" data-section="section-${i}">${escapeHTML(s.title[lang])}</a>`).join('')}<a href="#exercise" data-section="exercise">${t('exercise')}</a></aside></div>${footer()}`;
 $('completeArticle').addEventListener('click',()=>{
  if(completed.has(c.id))completed.delete(c.id);else completed.add(c.id);
  const persisted=storage.set('pocket-completed',[...completed]);
  $('completeArticle').setAttribute('aria-pressed',String(completed.has(c.id)));$('completeArticle').textContent=completed.has(c.id)?'✓ '+t('marked'):t('mark');
  $('storageMessage').textContent=t(persisted?'saved':'notSaved');updateShell();
 });
 $('printArticle').addEventListener('click',()=>window.print());
 $('main').querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
  const text=c.sections[Number(button.dataset.copy)].code;
  try {await copyText(text);button.textContent=t('copied');setTimeout(()=>button.textContent=t('copy'),1600);}catch{toast(t('copyError'));}
 }));
 $('main').querySelectorAll('[data-section]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();$(link.dataset.section).scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}));
}
function localizeFilename(name) {
 if(lang==='en')return name;
 return name.replace('Design excerpt · not part of the runnable memory example','设计示意 · 不属于可运行内存示例').replace('complete file','完整文件').replace('setup excerpt','初始化片段').replace('excerpt inside run','run 函数内的片段').replace('excerpt','片段').replace('Optional addition','可选添加').replace('inside newApp in app.go','app.go 的 newApp 内').replace('Standalone experiment','独立实验').replace('Design excerpt · not part of the runnable memory example','设计示意 · 不属于可运行内存示例').replace('rendering pattern','显示逻辑').replace('Second terminal','另一个终端').replace('Terminal','终端').replace('run one command at a time','每次运行一条命令');
}
async function copyText(text) {
 if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);return;}
 const area=document.createElement('textarea');area.value=text;area.style.cssText='position:fixed;left:-9999px';document.body.append(area);area.select();const success=document.execCommand('copy');area.remove();if(!success)throw new Error('copy');
}
function render() {
 readRoute();updateShell();if(current)renderArticle();else renderHome();setMenu(false);
 if(scrollRestore){const state=scrollRestore;scrollRestore=null;requestAnimationFrame(()=>{if(state.section){const node=$(state.section);if(node)window.scrollTo(0,node.offsetTop+state.offset);}else window.scrollTo(0,state.y);});}
 else {window.scrollTo(0,0);$('main').focus({preventScroll:true});}
}
document.querySelector('.skip').addEventListener('click',event=>{event.preventDefault();$('main').focus();$('main').scrollIntoView();});
$('search').addEventListener('input',event=>{query=event.target.value.trim().toLowerCase();renderNav();});
$('menuToggle').addEventListener('click',()=>setMenu(!$('sidebar').classList.contains('open')));
$('chapterNav').addEventListener('click',event=>{if(event.target.closest('a'))setMenu(false);});
document.querySelectorAll('[data-lang]').forEach(button=>button.addEventListener('click',()=>{
 if(button.dataset.lang===lang)return;
 const sections=[...document.querySelectorAll('.article-section,.exercise')];
 const visible=sections.filter(s=>s.getBoundingClientRect().top<140).at(-1);
 scrollRestore=visible?{section:visible.id,offset:window.scrollY-visible.offsetTop}:{y:window.scrollY};
 location.hash=href(current?.id,button.dataset.lang);
}));
document.addEventListener('keydown',event=>{
 const editing=/INPUT|TEXTAREA|SELECT/.test(event.target.tagName)||event.target.isContentEditable;
 if(event.key==='/'&&!editing){event.preventDefault();if(innerWidth<=680)setMenu(true);$('search').focus();}
 if(event.key==='Escape'){if(query){query='';$('search').value='';renderNav();}$('search').blur();setMenu(false);}
});
document.addEventListener('click',event=>{if(innerWidth<=680&&!event.target.closest('.sidebar,.menu-toggle')&&$('sidebar').classList.contains('open'))setMenu(false);});
window.addEventListener('hashchange',render);
render();
