# -*- coding: utf-8 -*-
"""VOL.14 构建脚本：index_template.html + _style_base.css → index.html（幂等）"""
import re

TPL = 'index_template.html'
CSS = '_style_base.css'
OUT = 'index.html'

base = open(CSS, encoding='utf-8').read()
# 换皮：事故台账主题（砖红主色 + 钢蓝辅色），paper 家族与语义绿保持系列一致
base = base.replace('--signal:#d96f1f', '--signal:#b5482a')
base = base.replace('rgba(217,111,31,.1)', 'rgba(181,72,42,.1)')
base = base.replace('--plum:#77588a', '--plum:#3e6e8e')
base = base.replace('rgba(119,88,138,.1)', 'rgba(62,110,142,.1)')
base = base.replace('#d96f1f', '#b5482a')

additions = '''
/* ---- VOL.14 小样专属 ---- */
.term{background:var(--code-bg);border-radius:8px;overflow:hidden;border:1px solid var(--line)}
.term-bar{display:flex;align-items:center;gap:6px;padding:7px 12px;background:rgba(255,255,255,.06);border-bottom:1px solid rgba(255,255,255,.08)}
.term-bar i{width:9px;height:9px;border-radius:50%;background:var(--line-strong);display:inline-block}
.term-bar i:first-child{background:#c75b5b}.term-bar i:nth-child(2){background:#c9a55b}.term-bar i:nth-child(3){background:#6fa876}
.term-bar span{margin-left:8px;font-family:var(--mono);font-size:11px;color:#9fb0a8;letter-spacing:.08em}
.term pre{margin:0;padding:12px 14px;font-family:var(--mono);font-size:12.5px;line-height:1.75;color:var(--code-ink);white-space:pre-wrap;min-height:96px}
.readout{display:flex;flex-wrap:wrap;gap:8px 18px;margin:12px 0;font-size:12.5px;color:var(--muted)}
.readout b{color:var(--ink);font-weight:600}
.readout b.bad{color:var(--signal)}
.d1-srcs{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:12px}
.d1-src{flex:1;min-width:150px;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;transition:.25s}
.d1-src b{display:block;font-size:12px;color:var(--ink)}
.d1-src i{display:block;font-family:var(--mono);font-size:10.5px;color:var(--muted);font-style:normal;margin:2px 0}
.d1-src em{font-style:normal;font-family:var(--mono);font-size:17px;font-weight:700;color:var(--signal)}
.d1-src.hot{border-color:var(--signal);background:var(--signal-soft);box-shadow:var(--hard-sm)}
.d1-stage{display:flex;gap:10px;margin:12px 0;flex-wrap:wrap}
.d1-box{flex:1;min-width:130px;border:1px dashed var(--line-strong);border-radius:8px;padding:10px;font-size:12px;color:var(--ink-soft);text-align:center}
.d1-box.ghostbox{border-style:solid;color:var(--ink)}
.d2-wrap{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:12px}
.d2-cap{font-family:var(--mono);font-size:10.5px;color:var(--muted);letter-spacing:.08em;margin-bottom:6px}
.d2-ledger,.d2-issuer{flex:1;min-width:200px;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.d2-tab{width:100%;min-width:0;border-collapse:collapse;font-family:var(--mono);font-size:12px}
.d2-tab td,.d2-tab th{border:1px solid var(--line);padding:4px 8px;text-align:left}
td.bad,.bad{color:var(--signal)}
.d2-num{font-family:var(--mono);font-size:34px;font-weight:700;color:var(--ink);transition:.3s}
.d2-num.swap{color:var(--signal)}
.d2-who{font-size:12px;color:var(--ink-soft);margin-top:4px}
.d3-resp{background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden;margin-bottom:12px}
.d3-head{display:flex;justify-content:space-between;align-items:center;padding:9px 14px;background:var(--paper-deep);border-bottom:1px solid var(--line);font-family:var(--mono);font-size:12px}
.d3-code{font-weight:700;color:var(--clock)}
.d3-ct{color:var(--muted);font-size:11px}
.d3-body{margin:0;padding:14px;font-family:var(--serif);font-size:14.5px;line-height:1.8;color:var(--ink)}
.d3-switches{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:6px}
.d4-wrap{display:flex;gap:16px;margin-bottom:6px;flex-wrap:wrap}
.d4-counters{min-width:150px;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 14px;text-align:center}
.d4-big{font-family:var(--mono);font-size:44px;font-weight:700;line-height:1;color:var(--signal)}
.d4-cap{font-size:11px;color:var(--muted);margin-top:4px}
.d4-sub{font-family:var(--mono);font-size:11.5px;color:var(--ink-soft);margin-top:4px}
.d4-tl{display:flex;flex-wrap:wrap;gap:3px;min-height:60px;align-content:flex-start}
.d4-tl i{width:9px;height:16px;background:var(--line-soft);border-radius:2px}
.d4-tl i.on{background:var(--signal)}
.d5-stack{display:flex;flex-direction:column;gap:6px;margin-bottom:12px}
.d5-layer{border:1px solid var(--line);border-radius:8px;padding:8px 12px;background:var(--card);display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.d5-layer.base{border-left:4px solid var(--clock)}
.d5-layer b{font-size:13px;color:var(--ink);min-width:150px}
.d5-layer span{font-family:var(--mono);font-size:11px;color:var(--ink-soft)}
.d5-layer i{margin-left:auto;font-family:var(--mono);font-style:normal;font-size:10.5px;color:var(--faint)}
.d5-layer.residue{box-shadow:inset 0 0 0 1px rgba(181,72,42,.4);background:var(--signal-soft)}
.tbl-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch}
.tbl-wrap table{min-width:560px}
@media (max-width:520px){.d2-wrap{flex-direction:column}}
'''

html = open(TPL, encoding='utf-8').read()
# base 自带 <style>…</style> 标签：剥掉外壳，追加样式必须放回同一块内
assert base.startswith('<style>') and base.rstrip().endswith('</style>'), 'base 外壳异常'
base_inner = base[len('<style>'):base.rfind('</style>')]
html = html.replace('{{STYLE}}', '<style>' + base_inner + additions + '\n</style>')
assert html.split('</head>')[0].count('.d5-stack{') == 1, '追加样式必须位于 head 的 style 块内'

favicon = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 '
           'viewBox=%220 0 24 24%22%3E%3Crect x=%224%22 y=%223%22 width=%2216%22 height=%2218%22 rx=%221.5%22 '
           'fill=%22%23faf9f3%22 stroke=%22%23333e48%22/%3E%3Ccircle cx=%229%22 cy=%229%22 r=%222.4%22 '
           'fill=%22%23b5482a%22/%3E%3C/svg%3E"/>')
html = html.replace('<meta name="viewport"', favicon + '\n<meta name="viewport"', 1)

# 五张章节插图
figs = [
    ('← .tools 本地 openclaw，启动器拉起</pre></div>', 'ch1',
     '单眼折纸鸟站在两台款式不同的电话总机之间，几十根电线缠成一个大结，鸟一手各握一个插头',
     '两台总机，两种说法：分裂不是谁犯错，是没人指认权威'),
    ('completed_at_ms: NULL                ← 永远等不到收尾的一行</pre></div>', 'ch2',
     '单眼折纸鸟在昏暗档案室举着台灯，抽出一份没有盖章的牛皮纸卷宗，旁边卷宗盖着红章',
     '档案室里那行没盖章的记录：盖章的人再也没回来'),
    ('CreationDate : 2026-11-14 8:15:43</pre></div>', 'ch3',
     '发号窗口里折纸鸟工作人员把方形号牌递给窗外一只拟人化公文包，旁边长椅上一台落灰的旧机器',
     '发号窗不问来历：6240 今天归公文包了'),
    ('—— api.kunyou.asia 经网关返回的 assistant 正文，HTTP 200 · elapsedMs≈6271 · text/event-stream</div>', 'ch4',
     '传送带上的包裹穿过亮着绿灯的闸机，包裹里露出一封带红色墨线的拒绝信，折纸鸟安检员用放大镜查看',
     '绿灯放行的包裹里，装着一封拒绝信'),
    ('      <tr><td><b>2026-11-14 09:21</b></td><td><b>31 发</b></td><td><b>206 秒</b></td><td><b>2.8–21.3 秒</b></td></tr>\n    </table>', 'ch5',
     '折纸鸟面无表情地把硬币一枚枚投进售货机，出货口掉出空纸盒，地上硬币堆成插着小旗的山',
     '空盒子堆成了山，投币的手没有停'),
]
for anchor, name, alt, cap in figs:
    assert html.count(anchor) == 1, f'锚点异常: {name} ({html.count(anchor)})'
    fig = (f'\n    <div class="fig"><div class="frame"><img src="assets/art/{name}.webp" alt="{alt}" '
           f'width="1152" height="832" loading="lazy" style="width:100%;border:1px solid var(--line)"/>'
           f'</div><figcaption><span><b>FIG. {name[1]}</b> {cap}</span><span>INK &amp; GOUACHE / 2026</span></figcaption></div>')
    html = html.replace(anchor, anchor + fig, 1)

# 四张内容表包 tbl-wrap
html = re.sub(r'<table class="tbl">([\s\S]*?)</table>',
              lambda m: '<div class="tbl-wrap"><table class="tbl">' + m.group(1) + '</table></div>', html)

# d4 重置时有界开关归位
html = html.replace(
    """    document.getElementById('d4-mode').textContent='无限重试（实录）';
  });
  render();""",
    """    document.getElementById('d4-mode').textContent='无限重试（实录）';
    document.getElementById('d4-bounded').checked=false;
  });
  render();""", 1)

open(OUT, 'w', encoding='utf-8').write(html)
checks = {
    'masthead': html.count('<header class="wrap masthead">'),
    'hero': html.count('<section class="wrap hero">'),
    'h1': html.count('<h1>'),
    'chapters': html.count('<section class="chapter"'),
    'demos': html.count('class="demo"'),
    'figs': html.count('class="fig"'),
    'tbl-wraps': html.count('tbl-wrap'),
    'stats': html.count('class="wrap stats"'),
}
print(checks)
assert checks['masthead'] == 1 and checks['hero'] == 1 and checks['h1'] == 1
assert checks['chapters'] == 6 and checks['demos'] == 5 and checks['figs'] == 5
assert checks['tbl-wraps'] == 6 and checks['stats'] == 1
print('build OK ->', OUT, len(html), 'chars')
