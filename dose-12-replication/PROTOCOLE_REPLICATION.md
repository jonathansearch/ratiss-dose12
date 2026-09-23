# DOSE-12 : PROTOCOLE DE RÉPLICATION (badge : protocole prêt)
## Environnement
`pip install qiskit qiskit-aer qiskit-ibm-runtime qiskit-nature pyscf ripser persim scipy`
(seeds fixées : 7 ; pas de QPU, pas de quota ; calibrations = publiques).
## Valeurs attendues (tolérance ±10% sauf Seeds exactes)
- dose01 : p*=3 (K+M), r_bruit(p3)=.87±.02, H creuse 3.3 puis pompe.
- dose02 : exact chimique 3/5 (0.5/1.0/1.5) ; bruit K 8-17 / M 20-46 mHa.
- dose03 : diam .41/.35/.23 ; H1-persist .063/.012/.007 ; bottleneck H0 .023/.043.
- moisson2 (JSON publics) : zz K .09/.14/.16/.21/.20/.22/.22, Page pic .78 @λ0.8.
- dose04 : S_K>S_M (valeurs du jour, ordre robuste).
## Badge
[![replication](https://img.shields.io/badge/replication-protocol_ready-blue)](dose-12-replication/PROTOCOLE_REPLICATION.md)
1 réplication externe documentée (issue/PR) = badge vert.
