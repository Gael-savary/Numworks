#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# generer_image_numworks.py — convertit une image (PNG, JPEG, base64)
# en script Python pour calculatrice NumWorks (module kandinsky).
#
# Usage PC :
#   pip install pillow
#   python generer_image_numworks.py image.png [sortie.py] [--taille 2]
#   python generer_image_numworks.py image_b64.txt sortie.py
#
# Le script genere s'envoie sur la calculatrice (USB, my.numworks.com/python)
# ou se colle dans un script de l'application Python, puis se lance.

import base64
import io
import sys
from collections import Counter

from PIL import Image

SW, SH = 320, 222
HEX = "0123456789ABCDEF"


def noire(v):
    return v


def charger_base64(nom_fichier):
    with open(nom_fichier, "r") as f:
        chiffre = "".join(f.read().split())
    return Image.open(io.BytesIO(base64.b64decode(chiffre)))


def reduire(img, dx, dy):
    copie = img.convert("RGBA")
    fond = Image.new("RGBA", copie.size, (255, 255, 255, 255))
    fond.paste(copie, mask=copie.split()[3])
    return fond.convert("RGB").resize((dx, dy), Image.LANCZOS)


def quantifier(img, n_couleurs):
    q = img.quantize(colors=n_couleurs, method=Image.MEDIANCUT, dither=0)
    pal = q.getpalette()
    couleurs = [tuple(pal[i * 3:i * 3 + 3]) for i in range(n_couleurs)]
    d = bytes(q.tobytes())
    freq = Counter(d)
    ordre = sorted(range(n_couleurs), key=lambda i: -freq.get(i, 0))
    remap = dict((a, n) for n, a in enumerate(ordre))
    couleurs = [couleurs[ordre[i]] for i in range(n_couleurs)]
    d = bytes(remap[v] for v in d)
    couleurs[0] = (255, 255, 255)
    utilises = sorted(set(d))
    remap2 = dict((a, n) for n, a in enumerate(utilises))
    d = bytes(remap2[v] for v in d)
    couleurs = [couleurs[i] for i in utilises]
    # fusion des couleurs quasi identiques (nettoyage du fond)
    netto = [couleurs[0]]
    for c in couleurs[1:]:
        ecart = (abs(netto[-1][0]-c[0]) + abs(netto[-1][1]-c[1]) + abs(netto[-1][2]-c[2])) / 3.0
        if ecart >= 24:
            netto.append(c)
    remap3 = {}
    for n, c in enumerate(couleurs):
        if n == 0:
            remap3[n] = 0
            continue
        if c in netto[1:]:
            remap3[n] = netto[1:].index(c) + 1
        else:
            meilleur = min(range(1, len(netto)),
                           key=lambda i: (abs(netto[i][0]-c[0]) + abs(netto[i][1]-c[1]) + abs(netto[i][2]-c[2])))
            remap3[n] = meilleur
    d = bytes(remap3[v] for v in d)
    return netto[:len(set(d))], d


def rle16(donnees):
    paires = []
    run = 1
    for i in range(1, len(donnees)):
        if donnees[i] == donnees[i-1] and run < 16:
            run += 1
        else:
            paires.append(HEX[donnees[i-1]] + HEX[run-1])
            run = 1
    paires.append(HEX[donnees[-1]] + HEX[run-1])
    return "".join(paires)


def generer(img, nom_script="image_numworks.py", taille_px=2, n_couleurs=4):
    largeur = min(SW // taille_px, img.size[0])
    hauteur = min(SH // taille_px, img.size[1])
    img = reduire(img, largeur, hauteur)
    couleurs, donnees = quantifier(img, n_couleurs)
    chiffre = rle16(donnees)
    morceaux = [chiffre[i:i+78] for i in range(0, len(chiffre), 78)]
    lignes = "\n".join('    "%s"' % m for m in morceaux)

    script = '''# -*- coding: utf-8 -*-
# Script genere pour NumWorks (%d x %d px affiches en %dx%d, %d couleurs, RLE).

from kandinsky import set_pixel

LARGEUR = %d
PALETTE = %r
DATA = (
%s
)

def afficher(x0=0, y0=0, t=%d):
    HEXV = "0123456789ABCDEF"
    n = 0
    for k in range(0, len(DATA), 2):
        couleur = PALETTE[HEXV.find(DATA[k])]
        for _ in range(HEXV.find(DATA[k+1]) + 1):
            x = x0 + (n %% LARGEUR) * t
            y = y0 + (n // LARGEUR) * t
            for dx in range(t):
                for dy in range(t):
                    set_pixel(x + dx, y + dy, couleur)
            n += 1

afficher()
''' % (largeur, hauteur, taille_px, taille_px, len(couleurs),
       largeur, couleurs, lignes, taille_px)

    with open(nom_script, "w") as f:
        f.write(script)
    return nom_script, len(script)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    nom = sys.argv[1]
    sortie = sys.argv[2] if len(sys.argv) > 2 else "image_numworks.py"
    t = 2
    if "--taille" in sys.argv:
        t = int(sys.argv[sys.argv.index("--taille") + 1])
    if nom.lower().endswith(".txt") or nom.lower().endswith(".b64"):
        img = charger_base64(nom)
    else:
        img = Image.open(nom)
    _, taille_octets = generer(img, sortie, taille_px=t)
    print("OK : %s (%d Ko)" % (sortie, taille_octets // 1024))


if __name__ == "__main__":
    main()
