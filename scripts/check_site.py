"""Check output completeness and internal file links after a Quarto render."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / '_site'
class Links(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        for key in ('href','src'):
            if key in a: self.links.append(a[key])
expected=[SITE/'index.html',SITE/'zh.html',SITE/'editions/english.html',SITE/'editions/chinese.html']
for language in ('en','zh'):
    sources=sorted((ROOT/language).glob('*.qmd'))
    assert len(sources)==14, f'Expected 14 {language} articles'
    expected += [SITE/language/(p.stem+'.html') for p in sources]
errors=[]
for path in expected:
    if not path.exists(): errors.append(f'Missing {path}'); continue
    parser=Links();parser.feed(path.read_text())
    for href in parser.links:
        u=urlsplit(href)
        if u.scheme or u.netloc or not u.path: continue
        name=unquote(u.path)
        if name.startswith('/pocket-framework/'): target=SITE/name.removeprefix('/pocket-framework/')
        elif name.startswith('/'): target=SITE/name.lstrip('/')
        else: target=path.parent/name
        if target.is_dir(): target=target/'index.html'
        if not target.exists(): errors.append(f'{path.relative_to(SITE)}: {href}')
assert not errors, '\n'.join(errors)
print(f'PASS: {len(expected)} pages and all internal file links/resources.')
