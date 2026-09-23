#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""DOSE-02 : microscope VQE-H2 (dissociation, exact vs bruit K/M, seuil 1.6mHa)."""
import json, os
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import TwoLocal
from qiskit.quantum_info import Statevector, DensityMatrix
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import JordanWignerMapper
import warnings; warnings.filterwarnings('ignore')
REPS, DISTS = 2, [0.5, 0.735, 1.0, 1.5, 2.5]
service = QiskitRuntimeService(channel='ibm_quantum_platform', token=os.environ['IBM_TOKEN'])
NM = {t: NoiseModel.from_backend(service.backend(n)) for t, n in (('K', 'ibm_kingston'), ('M', 'ibm_marrakesh'))}
BE = {t: service.backend(n) for t, n in (('K', 'ibm_kingston'), ('M', 'ibm_marrakesh'))}
mapper = JordanWignerMapper()
OUT = {}
print('d_An | E0_exact | E_vqe | err_ex(mHa) | E_K errK | E_M errM | depth_K/M')
for dist in DISTS:
    prob = PySCFDriver(atom=f'H 0 0 0; H 0 0 {dist}', basis='sto3g').run()
    Hjw = mapper.map(prob.hamiltonian.second_q_op())
    Hmat = Hjw.to_matrix(sparse=False)
    E0 = float(np.linalg.eigvalsh(Hmat)[0])
    ans = TwoLocal(4, 'ry', 'cz', reps=REPS)
    def cost(th):
        psi = Statevector.from_instruction(ans.assign_parameters(th)).data
        return float(np.real(np.vdot(psi, Hmat @ psi)))
    best = min((minimize(cost, x0=x0, method='COBYLA', options={'maxiter': 500})
                for x0 in ([np.zeros(ans.num_parameters)] + [np.random.RandomState(7 + i).uniform(-1, 1, ans.num_parameters) for i in range(4)])), key=lambda r: r.fun)
    Evqe = float(best.fun)
    row = {'E0': round(E0, 6), 'Evqe': round(Evqe, 6)}
    line = f'{dist:5.2f} | {E0:.5f} | {Evqe:.5f} | {(Evqe - E0) * 1000:6.2f}'
    for t in ('K', 'M'):
        tb = transpile(ans.assign_parameters(best.x), backend=BE[t], optimization_level=1)
        ti = transpile(ans.assign_parameters(best.x), basis_gates=['rz', 'sx', 'x', 'cz'], optimization_level=1)
        ti.save_density_matrix()
        sim = AerSimulator(method='density_matrix', noise_model=NM[t])
        rho = DensityMatrix(sim.run(ti).result().data(0)['density_matrix']).data
        En = float(np.real(np.trace(rho @ Hmat)))
        row[t] = round(En, 6)
        line += f' | {En:.5f} {(En - E0) * 1000:7.2f}'
    row['depth'] = {t: transpile(ans.assign_parameters(best.x), backend=BE[t], optimization_level=1).depth() for t in ('K', 'M')}
    OUT[str(dist)] = row
    print(line + f" | {row['depth']['K']}/{row['depth']['M']}")
json.dump(OUT, open('/home/user/ratiss-dose12/dose-02-vqe/dose02.json', 'w'), indent=0)
print('[dose02] ok')
