import sys, io
p = sys.argv[1]; newf = sys.argv[2]
s = open(p, encoding='utf-8').read()
new = open(newf, encoding='utf-8').read()
start_marker = '            <div class="day-card">\n                <div class="day-header"><h3>Day 4 - '
end_marker = '    </div>\n    <footer>'
a = s.index(start_marker)
b = s.index(end_marker)
out = s[:a] + new + s[b:]
open(p, 'w', encoding='utf-8', newline='').write(out)
print('ok', a, b, len(s), len(out))
