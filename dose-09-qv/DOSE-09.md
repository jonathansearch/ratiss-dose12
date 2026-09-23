# DOSE-09 : scalaire vs courbes — VERDICT : le lieu du bruit change le SIGNE
Cellule 2L λ-sweep, même budget 2% (3 seeds constructeur — leçon : le seed run()
d'Aer est IGNORÉ silencieusement, utiliser le constructeur).
- Portes 2% : 0.206→0.050 (×0.24, tue). Readout 2% : 0.206→0.228 (×1.11 ?!).
- Éludication : +11% = CORRUPTION DE PREP (6 resets d'initialize + readout).
  Preuve : circuit sans-reset → 0.224→0.201 (×0.90 = dilution théorique ✓).
  Bell témoin : 1.0→0.931 (théorie 0.922 ✓).
**Un seul chiffre (budget, QV-like) ne prédit ni l'amplitude ni le SIGNE.**
Coût : $0. Données : dose09.json (+test témoin Bell). Fig : fig_dose09.png.
