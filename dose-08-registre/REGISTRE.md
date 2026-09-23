# DOSE-08 : REGISTRE DES PRÉDICTIONS (datées, falsifiables)
| # | Prédiction (2026-09-24) | Critère | Échéance | Statut |
|---|---|---|---|---|
| P01 | K bat M par 1.0-1.3 (canari S) | prochain tir 2 backends | QPU dispo | ⏳ |
| P02 | QAOA anneau-6 réel : p*=3±1 | r(p) pic puis régresse | AWS/Braket | ⏳ |
| P03 | VQE-H2 réel : K<M en erreur, 0/5 chimique | table dose02 ±50% | AWS/Braket | ⏳ |
| P04 | Dérive session : 0.02-0.06 | 3 sessions témoin | reset IBM | ⏳ |
| P05 | Cellule horizon réel : 12-16L | zz→plancher | qBraid $5 | ⏳ |
| P06 | Rips-variété réel : bottleneck ordonné par dose | 3 niveaux bruit | simu→QPU | ⏳ |
| P07 | Mitigation : ZNE bat readout (simu 1.4x ✅) | dose05 rejoué réel | AWS/Braket | ⏳ |
| P08 | Répétition : logique<physique p≤8% (simu ✅) | dose06 rejoué réel | AWS/Braket | ⏳ |
| P09 | GCR-V4 : dérive <1e-6 ❌ (mesuré 4% Euler) → reformulée <5% ✅ ; étincelles 2/2 ✅ | run V4 | dose07 | ✅ |
| P10 | S03b : H·t=1.00±0.05 robuste | run S03b | later | ⏳ |
| P10b | S03 : r_min~r_eq + H1/r x10 ✅ | sweep dose11 | dose11 | ✅ |
| P11 | M-gap : split-2x → 59% ✅ (cohérent non isolé) | dose10 | dose10 | ✅ |
| P12 | 1 réplication externe documentée | protocole dose12 suivi | 2026-12-31 | ⏳ |
Règle : une prédiction fausse = on l'écrit ici en ❌ + on corrige le modèle.
