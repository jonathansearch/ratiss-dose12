# DOSE-02 : Microscope VQE-H2 — VERDICT : seuil chimique exact 3/5, bruit 0/5
H2 STO-3G (4q Jordan-Wigner), TwoLocal ry-cz reps=2, COBYLA 5 inits x500.
Énergies ÉLECTRONIQUES (sans répulsion nucléaire, comparaisons relatives OK).
| d (Å) | E0 | err exact | err K | err M |
|---|---|---|---|---|
| 0.50 | -2.11351 | 0.12 ✓ | 17.2 | 45.6 |
| 0.735 | -1.85728 | 2.55 ✗ | 14.5 | 37.1 |
| 1.00 | -1.63033 | 0.00 ✓ | 10.2 | 27.1 |
| 1.50 | -1.35093 | 0.00 ✓ | 7.7 | 19.8 |
| 2.50 | -1.14773 | 2.54 ✗ | 9.0 | 20.7 |
(mHa ; seuil chimique 1.6 mHa)
- Exact : 3/5 (0.5/1.0/1.5 à ~0). 0.735 et 2.5 à ~2.5 mHa = LIMITE D'EXPRESSIVITÉ
  reps=2 (5 inits convergent pareil, pas un minimum local).
- Bruit : 0/5 partout (K 8-17 mHa, M 20-46 mHa). **K ≈ 2x mieux que M** (même
  hiérarchie que la cellule : facteur backend confirmé sur un autre algo).
- Profondeurs transpilées ~54-57 (2q/4q peu profond → la mort vient du bruit
  de lecture+portes, pas des SWAPs : contraste avec QAOA).
Coût : $0. Données : dose02.json. Fig : fig_dose02.png.
