"""Create script-free, printable HTML editions from the article source."""
import json
from html import escape
from pathlib import Path
root=Path(__file__).resolve().parent.parent
chapters=json.loads((root/'content/chapters.json').read_text())
out=root/'editions';out.mkdir(exist_ok=True)
for lang, filename in [('en','english'),('zh','chinese')]:
    title='Pocket Framework — The complete field guide' if lang=='en' else 'Pocket Framework — 完整实践指南'
    intro='Fourteen articles. One small Go application. Read in order, and run the examples as you go.' if lang=='en' else '14 篇文章，一个小型 Go 应用。建议按顺序阅读，边读边运行示例。'
    def paras(text): return ''.join('<p>'+escape(p)+'</p>' for p in text.split('\n\n'))
    html=f'''<!doctype html><html lang="{lang}"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>body{{max-width:800px;margin:50px auto;padding:0 24px;font:17px/1.9 system-ui;color:#23322e;background:#fffefa}}h1,h2,h3{{font-family:Georgia,'Songti SC',serif;line-height:1.3}}h1{{font-size:40px}}a{{color:#365c48}}article{{border-top:1px solid #ddd;margin-top:60px;padding-top:30px}}pre{{background:#edf0e8;padding:20px;overflow:auto;font:12px/1.7 monospace;white-space:pre-wrap;overflow-wrap:anywhere}}.deck{{color:#68776b;font-size:20px}}.exercise{{padding:20px;background:#f0f2e9}}.references{{font-size:13px}}@media print{{article{{break-before:page}}nav,.switch{{display:none}}body{{font-size:11pt;margin:0;max-width:none}}pre{{font-size:9pt}}}}</style><p class="switch"><a href="../index.html#/{lang}">← {'Interactive reader' if lang=='en' else '交互阅读版'}</a> · <a href="{'chinese' if lang=='en' else 'english'}.html">{'中文' if lang=='en' else 'English'}</a></p><h1>{title}</h1><p>{intro}</p><nav><ol start="0">'''
    for c in chapters: html+=f'<li><a href="#{c["id"]}">{escape(c["title"][lang])}</a></li>'
    html+='</ol></nav>'
    for c in chapters:
        html+=f'<article id="{c["id"]}"><small>{c["id"][:2]} / POCKET NOTES</small><h2>{escape(c["title"][lang])}</h2><p class="deck">{escape(c["deck"][lang])}</p>'
        for s in c['sections']:
            html+='<section><h3>'+escape(s['title'][lang])+'</h3>'+paras(s['body'][lang])
            if 'code' in s: html+='<p><small>'+escape(s['filename'])+'</small></p><pre><code>'+escape(s['code'])+'</code></pre>'
            html+='</section>'
        e=c['exercise'];html+='<aside class="exercise"><h3>'+('Try it yourself' if lang=='en' else '动手练习')+'</h3>'+paras(e['question'][lang])+'<strong>'+('Explanation' if lang=='en' else '参考解释')+'</strong>'+paras(e['answer'][lang])+'</aside><p class="references">'
        html+=' · '.join('<a href="'+r['url']+'">'+escape(r['label'])+'</a>' for r in c['references'])+'</p></article>'
    html+='</html>'
    (out/(filename+'.html')).write_text(html)
print('Built both complete printable editions.')
