import re

trailer_map = {
    'GREENLAND: MIGRATION': 'vz-g2meF2zY',
    'HOW TO TRAIN YOUR DRAGON': 'yH2s1B4Yngc',
    'DEN OF THIEVES 2': 'h2O_XgJ5JpE',
    'PLANE': 'M25zXBIUVr0',
    'KANDAHAR': '1cWw-FIt7lM',
    'LAST SEEN ALIVE': '7Tf2q07P1U8',
    'COPSHOP': 'y_bTq2B01QY',
    'GREENLAND': 'vz-g2meF2zY',
    'ANGEL HAS FALLEN': 'XF8zHGoHn2U',
    'HTTYD: THE HIDDEN WORLD': 'SkcucKDrbOI',
    'DEN OF THIEVES': 'WZkEjDEK90I',
    'HUNTER KILLER': 'mnP_z3pqmCU',
    'THE VANISHING': '5wVpxx08f0E',
    'GEOSTORM': 'V7e4_iNpsM8',
    'LONDON HAS FALLEN': '3AsOdX7NcJs',
    'GODS OF EGYPT': 'IJBnK2wNQSo',
    'A FAMILY MAN': 'j3Qv5J6O2_w',
    '300: RISE OF AN EMPIRE': 'jGEERBDelH8',
    'OLYMPUS HAS FALLEN': 'ar-Wa8RiwB0',
    'CHASING MAVERICKS': '_k0_zO1q2q0',
    'MACHINE GUN PREACHER': 'O4k0l3eG03s',
    'THE BOUNTY HUNTER': 'x_KxR68hWiw',
    'LAW ABIDING CITIZEN': 'LX6kVRsdXW4',
    'GAMER': 'P2g94xQmtHw',
    'THE UGLY TRUTH': 'xL1Fp-i1O04',
    'ROCKNROLLA': 'TqJ0q0uL4mY',
    'NIM\'S ISLAND': 'GZgV2Z29u5A',
    '300': 'UrIbxk7idYA',
    'P.S. I LOVE YOU': 'CZzW6_hR068',
    'PHANTOM OF THE OPERA': '44w6elsTpuc',
    'DEAR FRANKIE': 'A0vH2O_1q9I',
    'LARA CROFT TOMB RAIDER': 'v2P0rC2qXq8',
    'REIGN OF FIRE': '8X5z_N_yKKE'
}

with open('films.html', 'r') as f:
    content = f.read()

# We need to find <div class="film-card"> and inject data-trailer="..." based on the <h4> tag inside it.
def replace_card(match):
    full_match = match.group(0)
    title_match = re.search(r'<h4>(.*?)</h4>', full_match)
    if title_match:
        title = title_match.group(1).strip()
        # manual fallback for variations
        if 'LARA CROFT' in title: title = 'LARA CROFT TOMB RAIDER'
        trailer_id = trailer_map.get(title, 'vz-g2meF2zY') # Default to greenland
        # Replace <div class="film-card"> with <div class="film-card" data-trailer="ID">
        return full_match.replace('<div class="film-card">', f'<div class="film-card" data-trailer="{trailer_id}">')
    return full_match

new_content = re.sub(r'<div class="film-card">.*?</div>\s*</div>', replace_card, content, flags=re.DOTALL)

with open('films.html', 'w') as f:
    f.write(new_content)
