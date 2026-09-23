# DOSE-03 : Rips topologique — VERDICT : la variété dose→réponse mesure l'effondrement
Données 100% FRAÎCHES, bruit GÉNÉRIQUE (dépolarisant + readout, pas de backend IBM).
## v1 (négative, honnête) : Rips brut sur bitstrings = aveugle
- GHZ-6 : h0_merge 3.0 (pur, q=0.01) → 1.0 (bruité) : sépare, OK en sonde.
- MAIS cellule λ-sweep : h0=h1=1.0 PARTOUT (blob unique, zz 0.01→0.25 invisible).
- β1-Hamming : 1.0 PARTOUT (saturé, dynamique nulle) → confirmé mauvais (v1).
## v2 (positive) : Rips sur la VARIÉTÉ dose→réponse (36 pts : 9λ × 4nl, Hellinger)
| carte | diamètre | H0 persist | H1 persist | H1 max |
|---|---|---|---|---|
| exacte | 0.408 | 1.731 | 0.063 (6 barres) | 0.027 |
| bruit faible | 0.351 | 1.553 | 0.012 (3) | 0.007 |
| bruit fort | 0.230 | 1.193 | 0.007 (4) | 0.005 |
- Effondrement : diamètre ×0.56, H0 ×0.69, H1 ×1/9 (boucles effacées).
- Bottleneck exact-vs-bruit : H0 0.023 (faible) → 0.043 (fort) : ORDONNÉ par dose.
- H1 faible en absolu (0.063) : signal doux, pas un mur — dit honnêtement.
**Verdict : Rips-variété quantifie la mort là où β1 sature et Rips-bitstring voit
un blob. Le détecteur du ticket RIPS = (diamètre, H0-persist, bottleneck).**
Coût : $0. Données : dose03.json (matrices H incluses). Fig : fig_dose03.png.
