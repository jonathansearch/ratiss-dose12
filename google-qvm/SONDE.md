# GOOGLE QVM / qsim — sonde (2026-09-24, gratuit, local)
- QVM = qsim (C++, AVX/FMA, OpenMP) + Cirq + bruit processeur Weber/Rainbow.
  Testé : moteur qsim via qsimcirq (pip). QVM cloud (Colab/datasets bruit Google)
  non testé (demande Colab/GCP) ; cirq.google Engine = whitelist (pas libre).
- EXACT 6q contact : qsim zz=0.7260 vs Aer 0.7273 (4000 shots) : ACCORD.
- VITESSE (CPU sandbox) : supremacy-style 20q d12 = 0.05s ; 24q d12 = 0.97s.
  Bit-order qsim : mesures packées int big-endian (q[i] = bit n-1-i).
- BRUIT p=0.02 : qsim zz=0.41 vs Aer zz=0.51. Écart = placement/définition du
  dépolarisant (with_noise vs NoiseModel), pas un bug : les modèles ne sont
  jamais identiques entre frameworks. Exact reste la référence commune.
- Verdict : OUI c'est puissant (C++ multithread, 24q ~1s CPU). Candidat
  cross-validateur exact + gros circuits. Bruit : garder Aer (calibrations).
