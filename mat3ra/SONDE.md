# MAT3RA — sonde API (2026-09-24, clés user, jamais commitées)
- Auth : X-Account-Id (16c) + X-Auth-Token (43c) sur /api/2018-10-01. OK.
- Plan : FREE (1 projet, 10GB, workflows/matériaux illimités, banque lecture OK).
- Compute : PAYANT (recharge Balance, ~$0.12-0.20/core-h, saving ~$0.03). Pas de crédits gratuits, pas de restore.
- Minage gratuit : job "Silicon HSE Band Gap" (avYBJFsX4s8YTChyK) → gap direct 0.9863 eV @X, indirect 0.9862 eV (Γ→X), Fermi 3.39 eV, P=-1.18 kbar. Banque : Si Fd-3m a=3.867Å d=2.28, H2, P, PrN...
- Endpoints utiles : materials, materials/{id}, jobs, jobs/{id}, properties?jobId=, workflows, projects. Pas d'endpoint balance (UI uniquement).
