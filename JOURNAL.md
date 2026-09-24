# DOSE-01

## 2026-09-23 — DOSE-01 mesurée : microscope QAOA p*=3 (K+M) 🔬
- Exact résout à p=3 (r=1.0). Bruit : pic p=3 (r=.87) puis mort (.80 à p=6). H creuse puis pompe, MI pic puis décroît. Verdict proposé : p*=3 les 2 backends. En attente validation chef.

## 2026-09-23 — DOSE-01 validée (p*=3) ; DOSE-02 mesurée : VQE-H2 seuil 3/5 exact, 0/5 bruit 🧪
- TwoLocal r=2 : exact chimique à 0.5/1.0/1.5, limite ansatz à 0.735/2.5 (~2.5mHa). Bruit : K 8-17, M 20-46 mHa (K 2x mieux). Verdict proposé. En attente validation chef.

## 2026-09-24 — DOSE-02 validée ; DOSE-03 mesurée : Rips-variété (effondrement x0.56, H1 x1/9) 🕸️
- Renouveau : données fraîches + bruit générique (plus de fixation IBM). v1 négative (blob, β1 saturé), v2 positive (variété 36pts : diamètre/H0/bottleneck ordonnés par dose). Verdict proposé. En attente validation chef.

## 2026-09-24 — TOUTES LES DOSES FINIES (04→12 d'un coup, mode enthousiaste) 😎🎉
- 04 canari S_K/S_M=1.14 prédit (calibs live). 05 ZNE x1.4 (readout ~nul, noyade au-delà). 06 répétition gagne p≤8% (d5 x54 à 2%). 07 V4 : étincelles 2/2, drift témoin 4% (P09❌→reformulée). 08 registre 12+1 prédictions. 09 lieu-du-bruit change le SIGNE (reset-prep +11% élucidé, Bell ✓). 10 split-2x → 59% (gap expliqué ×0.82). 11 r_min~r_eq, H1/r ×10 vs GR. 12 protocole réplication + badge.
- Leçons labo : seed Aer = constructeur (run() ignoré !) ; opt1 refusionne les splits ; readout corrompt les resets.

## 2026-09-24 — Sonde Mat3ra (clés user) : API OK, gap Si 0.986 eV miné (gratuit) 🔑
- Free confirmé (calcul payant, banque libre). Note : mat3ra/SONDE.md. Prochain : soumission Total Energy Si dès recharge Balance.

## 2026-09-24 — Sonde Google qsim : exact=Aer (0.726/0.727), 24q en ~1s ⚡
- Moteur QVM testé en local (gratuit). Bruit : écart de placement vs Aer (0.41 vs 0.51, documenté). Note : google-qvm/SONDE.md.

## 2026-09-24 — Visuels animés : 3 GIFs (H2 réel, Si phonon, Rabi) 🎬
- Réponse à la remarque "pas de vraies simulations visuelles" : GIFs légers
  inline README (conventions qmsolve/md_animation). Données réelles quand ça existe.
