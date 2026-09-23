# DOSE-01 : Microscope QAOA — VERDICT : p* = 3 (2 backends)
MaxCut anneau 6 noeuds (optimum 6), p=1..6, angles COBYLA (2 inits), 2000 shots.
Exact : r = .750/.833/**1.000**/1.000/1.000/1.000 (résolu à p=3, H 4.67→1.00).
Bruit K : r = .724/.778/**.870**/.860/.826/.807 → pic p=3 puis RÉGRESSE.
Bruit M : r = .725/.777/**.871**/.846/.804/.790 → pic p=3 puis RÉGRESSE.
H bruit creuse à p=3 (3.32) puis remonte (4.1-4.3, pompe) ; MI pic p=3 (.82/.78)
puis décroît (.60/.55). Profondeur transp. p=3 : 284 (SWAPs : anneau sur chaîne).
**p* = 3 kingston ET marrakesh** (critère pré-enregistré : régression + <90% exact).
Note : K≈M ici (pas de facteur 1.4) — les SWAPs dominent pour les deux.
Coût : $0. Données : dose01.json. Fig : fig_dose01.png.
