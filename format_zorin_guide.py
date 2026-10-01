from collections import Counter
from pathlib import Path
import re
import unicodedata


def slug(title):
    return ''.join(c for c in title.lower() if c in ' -_' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')


def deepen(text, levels=1):
    lines = []
    fenced = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith('```'):
            fenced = not fenced
        if not fenced and re.match(r'#{2,5} ', line):
            line = '#' * levels + line
        lines.append(line)
    assert not fenced
    return ''.join(lines)


path = Path('00_B_Installacio_Zorin_OS.md')
before = path.read_bytes()
original = before.decode('utf-8').replace('\r\n', '\n')
headings = list(re.finditer(r'^## (.+)$', original, re.M))
blocks = {}
for index, match in enumerate(headings):
    end = headings[index + 1].start() if index + 1 < len(headings) else len(original)
    blocks[match[1]] = original[match.start():end].strip().removesuffix('---').rstrip()
intro = original[:headings[0].start()].rstrip()

phases = re.findall(r'^\| ([^|]+) \| (\d+(?:–\d+)?) \| ([^|]+) \|$', blocks['Itinerari de treball'], re.M)
assert len(phases) == 5
phase_descriptions = [
    "Obtén la ISO oficial i comprova'n la integritat abans d'utilitzar-la.",
    "Crea una màquina independent i revisa els recursos, el disc, la ISO i la xarxa NAT.",
    "Completa la instal·lació i comprova que Zorin arrenca des del disc virtual.",
    "Comprova el sistema, instal·la les actualitzacions i identifica la configuració de xarxa.",
    "Desa una base recuperable, revisa els resultats i recull les evidències de la preparació.",
]

route = '<a id="itinerari-de-treball"></a>\n\n## Ruta de treball\n\n| Fase | Apartats | Què aconseguiràs? |\n|---|---|---|\n'
toc = ['## Índex', '', '- **Preparació:** [Objectius i resultats esperats](#objectius-i-resultats-esperats) · [Resultat final](#resultat-final-esperat) · [Convencions](#convencions-de-la-guia) · [Requisits previs](#requisits-previs)']
body = []
titles = {int(title.split('.')[0]): title for title in blocks if re.match(r'^\d+\. ', title)}
for number, (name, span, outcome) in enumerate(phases, 1):
    route += f'| **[Fase {number}. {name}](#fase-{number})** | {span} | {outcome} |\n'
    bounds = list(map(int, span.split('–')))
    section_range = range(bounds[0], bounds[-1] + 1)
    links = [f'[{titles[n]}](#{slug(titles[n])})' for n in section_range]
    toc.append(f'- **[Fase {number} — {name}](#fase-{number}):** ' + ' · '.join(links))
    body.append(f'---\n\n<a id="fase-{number}"></a>\n\n## Fase {number}. {name}\n\n{phase_descriptions[number - 1]}')
    body.extend(deepen(blocks[titles[n]]) for n in section_range)

# Keep final checks, evidence and reflection with the last phase, inside section 12.
for title in ['Comprovació final', 'Evidències recomanades', 'Preguntes de reflexió']:
    body.append(deepen(blocks[title], 2))
toc[-1] += ' · [Comprovació final](#comprovació-final) · [Evidències](#evidències-recomanades) · [Reflexió](#preguntes-de-reflexió)'

reference_titles = ['Preparació per a la pràctica de DHCP amb Kea', 'Resolució d’incidències'.replace('’', "'"), 'Fonts de consulta']
reference = '\n\n'.join(deepen(blocks[title]) for title in reference_titles)
toc.append('- **Consulta i ajuda:** ' + ' · '.join(f'[{title}](#{slug(title)})' for title in reference_titles))

objectives = blocks["Què has d'aconseguir"].split('\n\n', 1)[1]
requirements = deepen(blocks['Abans de començar']).replace('### Abans de començar', '### Requisits previs', 1)
preparation = ("## Preparació\n\n<a id=\"què-has-daconseguir\"></a>\n\n### Objectius i resultats esperats\n\n" + objectives
    + '\n\n' + deepen(blocks['Resultat final esperat'], 2)
    + "\n\n### Convencions de la guia\n\nSegueix els apartats en ordre i compara cada resultat amb el **resultat esperat** abans de continuar. Adapta les rutes, els noms i les interfícies dels exemples a la teva màquina.\n\nEls comentaris HTML que comencen per `CAPTURA` indiquen les evidències que cal preparar. Es veuen quan edites el Markdown, però no en la vista de lectura.\n\n<a id=\"abans-de-començar\"></a>\n\n"
    + requirements)
route += "\n> [!TIP]\n> La primera vegada, segueix els apartats en ordre. Si reprens la pràctica, consulta l'**objectiu** i el **resultat esperat** de cada apartat per saber des d'on continuar."
result = (intro + '\n\n' + route + '\n\n' + '\n'.join(toc)
    + '\n\n---\n\n' + preparation + '\n\n' + '\n\n'.join(body)
    + '\n\n---\n\n## Consulta i ajuda\n\n' + reference + '\n')

# Verify content preservation against the actual file read at the start.
def content(text):
    return Counter(line for line in text.splitlines() if line.strip() and not line.startswith(('#', '<a ', '---')))
old_content = '\n\n'.join(block for title, block in blocks.items() if title not in ['Itinerari de treball', 'Índex'])
missing = content(intro + '\n\n' + old_content) - content(result)
assert not missing, missing
code_pattern = r'^ *```[^\n]*\n.*?^ *```[ \t]*$'
assert re.findall(code_pattern, original, re.M | re.S) == re.findall(code_pattern, result, re.M | re.S)
assert re.findall(r'<!--.*?-->', original, re.S) == re.findall(r'<!--.*?-->', result, re.S)
assert re.findall(r'!\[[^\n]*', original) == re.findall(r'!\[[^\n]*', result)
result_headings = re.findall(r'^(#{1,6}) (.+)$', result, re.M)
assert sum(level == '#' for level, _ in result_headings) == 1
for previous, current in zip(result_headings, result_headings[1:]):
    assert len(current[0]) <= len(previous[0]) + 1, current
anchors = {slug(title) for _, title in result_headings} | set(re.findall(r'<a id="([^"]+)"', result))
assert not {slug(match[1]) for match in re.finditer(r'^#{1,6} (.+)$', original, re.M)} - anchors
assert not set(re.findall(r'\]\(#([^)]+)\)', result)) - anchors
assert list(map(int, re.findall(r'^### (\d+)\. ', result, re.M))) == list(range(1, 13))
assert len(re.findall(r'^## Fase \d+\.', result, re.M)) == 5
assert len(re.findall(r'^> \*\*Objectiu:', result, re.M)) == 12
assert len(re.findall(r'^> \*\*Resultat esperat:', result, re.M)) == 12
assert path.read_bytes() == before, 'El document ha canviat durant la revisió.'
newline = '\r\n' if b'\r\n' in before else '\n'
path.write_bytes(result.replace('\n', newline).encode('utf-8'))
print('Zorin: 5 fases i 12 apartats. Contingut, blocs de codi, comentaris, imatges i ancoratges originals conservats; índex i jerarquia comprovats.')
