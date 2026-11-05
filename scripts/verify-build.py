"""Offline checks: only HTML/CSS and text extracted from specifications are read.

Uses the standard library; never opens image files or makes network requests.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
ROUTES = {
    'PG-001': '',
    'PG-002': 'betipercup/',
    'PG-004': 'betipercup/overview/',
    'PG-005': 'betipercup/rules/',
    'PG-006': 'betipercup/rules/detail/',
    'PG-007': 'betipercup/rules/survivor/',
    'PG-008': 'betipercup/rules/killer/',
    'PG-009': 'betipercup/schedule/',
}
COMING_SOON = {
    'PG-014': 'betipercup/event/',
    'PG-019': 'betipercup/notice/',
    'PG-020': 'betipercup/organizer/',
    'PG-021': 'betipercup/faq/',
    'PG-022': 'betipercup/privacy/',
}
ROUTES.update(COMING_SOON)
OUT_OF_SCOPE = {
    '/staging/betipercup/participants/',
    '/staging/betipercup/participants/recruitment/',
}

class HTML(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements = []
        self.texts = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def handle_data(self, text):
        self.texts.append(text)

    def attrs(self, tag):
        return [attrs for kind, attrs in self.elements if kind == tag]

    def count_class(self, name):
        return sum(name in attrs.get('class', '').split() for _, attrs in self.elements)

def compact(text):
    return re.sub(r'\s+', '', text)

actual = {p.relative_to(DOCS).as_posix() for p in DOCS.rglob('*.html')}
expected = {route + 'index.html' for route in ROUTES.values()}
assert actual == expected, (actual - expected, expected - actual)
assert (ROOT / 'public/.nojekyll').stat().st_size == 0
assert (DOCS / '.nojekyll').stat().st_size == 0
assert not list(DOCS.rglob('*.pdf')) and not list(DOCS.rglob('*.xlsx'))
assert not (DOCS / 'codex-input').exists()

report = {'pages': [], 'out_of_scope_links': [], 'source_text_checks': 0}
parsed = {}
for pg, route in ROUTES.items():
    html = (DOCS / route / 'index.html').read_text(encoding='utf-8')
    dom = HTML(html)
    parsed[pg] = dom
    assert dom.attrs('html')[0]['lang'] == 'ja'
    assert any(m.get('name') == 'robots' and m.get('content') == 'noindex' for m in dom.attrs('meta'))
    assert not any(m.get('property', '').startswith('og:') for m in dom.attrs('meta'))
    assert len([a for a in dom.attrs('link') if a.get('rel') in ('icon', 'apple-touch-icon')]) == 3
    for a in dom.attrs('link'):
        if a.get('rel') in ('icon', 'apple-touch-icon'):
            assert a['href'].startswith('/images-stg/')
        elif a.get('rel') == 'stylesheet':
            stylesheet = a['href'].removeprefix('/staging/')
            assert (DOCS / stylesheet).is_file(), stylesheet
    for img in dom.attrs('img'):
        assert img['src'].startswith('https://betty-roulette.github.io/images-stg/')
        assert img.get('alt') and not img.get('srcset')
    url = 'https://betty-roulette.github.io/staging/' + route
    for a in dom.attrs('a'):
        target = a['href']
        assert not target.startswith(('/', 'http', '#')), (pg, target)
        assert 'target' not in a
        resolved = urlparse(urljoin(url, target)).path
        if resolved in OUT_OF_SCOPE:
            report['out_of_scope_links'].append({'from': pg, 'to': resolved})
        else:
            assert resolved.startswith('/staging/')
            assert (DOCS / resolved.removeprefix('/staging/') / 'index.html').is_file(), (pg, target)
    if pg == 'PG-001':
        assert any(m.get('http-equiv') == 'refresh' and m.get('content') == '0;url=./betipercup/' for m in dom.attrs('meta'))
        assert not dom.attrs('header') and not dom.attrs('footer')
    else:
        assert len(dom.attrs('header')) == len(dom.attrs('footer')) == 1
        assert dom.count_class('menu') == 1
        assert dom.count_class('text-link') >= 5
        assert not any(m.get('http-equiv') == 'refresh' for m in dom.attrs('meta'))
    if pg in COMING_SOON:
        main = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.S).group(1)
        assert main.strip() == '<p>準備中</p>', pg
    report['pages'].append({'pg': pg, 'file': route + 'index.html', 'url': url, 'images': len(dom.attrs('img'))})

assert parsed['PG-002'].count_class('image-card') == 5
assert parsed['PG-004'].count_class('image-card') == 3
assert len(parsed['PG-005'].attrs('tr')) == 7
assert not parsed['PG-005'].attrs('thead')
assert parsed['PG-005'].count_class('image-card') == 3
assert parsed['PG-006'].count_class('rule-card') == 23
assert parsed['PG-006'].count_class('image-card') == 2
assert len(parsed['PG-007'].attrs('tr')) == 7
assert len(parsed['PG-007'].attrs('li')) == 8 + 17 + 10 + 4  # perks + rule bullets + menu
assert len(parsed['PG-008'].attrs('tr')) == 8
assert not parsed['PG-009'].attrs('table')
assert not any('event/schedule' in a['href'] for a in parsed['PG-009'].attrs('a'))
assert '大会結果' not in ''.join(parsed['PG-002'].texts).split('大会情報のご案内')[-1]

MAPS = [
    '①ギデオン食肉工場：ザ・ゲーム',
    '②壊滅したボルゴ：忘れ去られた遺跡',
    '③マクミラン・エステート：コールタワー',
    '④オートヘイヴン国立研究所：地下施設',
    '⑤スプリングウッド：バダム幼稚園Ⅱ（ボーナスマップ）',
]
detail = (DOCS / ROUTES['PG-006'] / 'index.html').read_text(encoding='utf-8')
maps_html = re.search(r'<ol class="maps">(.*?)</ol>', detail, re.S).group(1)
assert re.findall(r'<li>(.*?)</li>', maps_html, re.S) == MAPS
assert '2026/11/5' in ''.join(parsed['PG-002'].texts)
assert '2026/11/3' not in ''.join(parsed['PG-002'].texts)
killer = (DOCS / ROUTES['PG-008'] / 'index.html').read_text(encoding='utf-8')
assert re.search(r'>使用禁止パーク</th>\s*<td>後日記載</td>', killer)

# Compare all individual published paragraphs, list entries and table cells to
# the PDF text, when the local, non-public text extraction is available.
texts = ROOT / 'tmp/spec-text'
if texts.exists():
    for pg, route in ROUTES.items():
        if pg == 'PG-001' or pg in COMING_SOON:
            continue
        files = list(texts.glob(f'*{pg}*.txt'))
        if pg == 'PG-004':
            files = list(texts.glob('*PG-002_PG-004*.txt'))
        assert len(files) == 1, pg
        source = compact(files[0].read_text(encoding='utf-8'))
        # These Staging corrections supersede the original specification text.
        if pg == 'PG-002':
            source = source.replace('2026/11/3', '2026/11/5')
        elif pg == 'PG-006':
            source += '\n'.join(MAPS)
        elif pg == 'PG-008':
            source = source.replace('天界の証人', '後日記載')
        html = (DOCS / route / 'index.html').read_text(encoding='utf-8')
        main = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.S).group(1)
        for fragment in re.findall(r'<(?:p|li|td|th)\b[^>]*>(.*?)</(?:p|li|td|th)>', main, re.S):
            value = compact(''.join(HTML(fragment).texts))
            if value:
                assert value in source, (pg, value)
                report['source_text_checks'] += 1

config = (ROOT / 'astro.config.mjs').read_text(encoding='utf-8')
assert "site: 'https://betty-roulette.github.io'" in config
assert "base: '/staging'" in config
assert "outDir: './docs'" in config
assert 'astro:assets' not in '\n'.join(p.read_text(encoding='utf-8') for p in (ROOT / 'src').rglob('*.astro'))
print(json.dumps(report, ensure_ascii=False, indent=2))
print('PASS: HTML, routes, metadata, counts, relative links, text comparison and .nojekyll')
