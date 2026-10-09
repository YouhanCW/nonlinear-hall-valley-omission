"""Independent checks of the physical reduction and its stated domain.

Run with pytest -s to inspect the frequency/refinement summary. These tests do
not replace canonical data or require a historical research directory.
"""
import json
import numpy as np
import pytest
from scipy.linalg import eigh, eigvalsh, norm, solve
from threadpoolctl import threadpool_limits
from nonlinear_hall import core
from nonlinear_hall.mode_ablation import hierarchy
from nonlinear_hall.referee_numerics import (
    PreparedSystem, RevisionParameters, transition_parts, laplacian,
)


@pytest.fixture(autouse=True)
def single_thread():
    with threadpool_limits(limits=1):
        yield


@pytest.mark.parametrize('xi', [0., .1])
def test_physical_metric_projector_and_independent_full_space(xi):
    s = PreparedSystem(RevisionParameters(n=48, xi=xi, delta_P=.4))
    eta = .3
    _, _, defect, raw = hierarchy(s, eta)
    w = s.st['weight']; sw = np.sqrt(w)
    Ufull = np.column_stack([core.lift(u, s.st, s.p.n) for u in raw['U'].T])
    V = Ufull/sw[:, None]
    gram = V.T @ (w[:, None]*V)
    P = V @ solve(gram, V.T*w[None, :], assume_a='pos')
    r0, r1 = transition_parts(s.st, s.p)
    rate = r0 + eta*r1
    C = np.diag(rate@w) - rate*w[None, :]
    Lfull = laplacian(rate, w)
    assert norm(P@P-P) < 1e-12
    assert norm(w[:, None]*P-P.T*w[None, :]) < 1e-12
    weighted_residual = sw[:, None]*(C@V-P@C@V)
    expected = np.column_stack([core.lift(v, s.st, s.p.n) for v in raw['R'].T])
    assert norm(weighted_residual-expected) < 1e-12
    full = core.full_solution(Lfull, sw*s.st['vx'])
    assert norm(full-core.lift(raw['g'], s.st, s.p.n))/norm(full) < 1e-10
    # Independent contact moment space uses vx and partner sign, not g_A0.
    if xi == 0:
        columns = [sw*s.st[key]*(s.st['sector']==sector)
                   for sector in ['A', 'P'] for key in ['vx', 's']]
        Q, _ = np.linalg.qr(np.column_stack(columns))
        assert norm(Lfull@Q-Q@(Q.T@Lfull@Q))/norm(Lfull@Q) < 1e-12
        assert defect['rho_rel'] < 1e-12
    else:
        assert defect['rho_rel'] > 1e-3


CASES = [
    ('scalar', 10., 1.2, 0., 'gaussian'),
    ('shape', .3727593720314942, .4, 0., 'gaussian'),
    ('weak', .001, .4, .1, 'gaussian'),
    ('cancellation', .26366508987303583, .5103448275862069, .1, 'gaussian'),
    ('matched_gaussian', 1., 1.2, .05, 'gaussian'),
    ('matched_lorentzian', 1., 1.2, .05, 'lorentzian'),
]


@pytest.mark.parametrize('label,eta,delta,xi,kernel', CASES)
def test_frequency_refinement_and_relaxation_poles(label, eta, delta, xi, kernel):
    records = []
    for n in [64, 128, 256]:
        s = PreparedSystem(RevisionParameters(n=n, delta_P=delta, xi=xi, kernel=kernel))
        L = s.L0 + eta*s.K
        rates, V = eigh(L)
        assert rates[0] > 0
        for wr in [0., 1e-5, 1e-4, 1e-3, 1e-2]:
            omega = wr*s.gap
            f, levels, d, raw = hierarchy(s, eta, omega)
            spectral = (V.T@s.h) @ ((V.T@s.b)/(rates+1j*omega))
            assert abs(spectral-f['H']) < 1e-10*max(abs(f['H']), 1.)
            assert d['adjoint_identity_defect'] < 1e-10
            assert d['residual_decomposition_defect'] < 1e-11
            assert abs(d['signed_H_error']) <= d['orthogonal_adjoint_bound']+1e-11
            ritz = eigvalsh(raw['U'].T@L@raw['U'])
            assert np.all(ritz >= rates[:4]-1e-13)
            assert np.all(ritz <= rates[-4:]+1e-13)
            if xi == 0:
                assert d['rho_rel'] < 1e-12
                assert levels[2]['distribution_error'] < 1e-10
            records.append(dict(n=n,wr=wr,H=f['H'],rho_abs=d['rho_abs'],rho_rel=d['rho_rel'],
                error=levels[3]['error_H'],phase=np.angle(levels[3]['H']/f['H'],deg=True)))
    coarse = [r for r in records if r['n']==128]
    fine = [r for r in records if r['n']==256]
    for a,b in zip(coarse,fine):
        assert abs(a['H']-b['H']) < 1e-10*max(abs(b['H']),1.)
        assert abs(a['rho_abs']-b['rho_abs']) < 1e-12
        assert abs(a['rho_rel']-b['rho_rel']) < 1e-10
    print(json.dumps(dict(case=label,rho_abs=fine[0]['rho_abs'],rho_rel=fine[0]['rho_rel'],
        max_M4_relative_error=max(r['error'] for r in fine),
        max_M4_phase_error_degrees=max(abs(r['phase']) for r in fine),
        max_128_to_256_H_change=max(abs(a['H']-b['H']) for a,b in zip(coarse,fine)))))


def test_identically_zero_hall_readout_has_no_relative_accuracy_claim():
    s = PreparedSystem(RevisionParameters(n=32, m_A=0.))
    assert np.count_nonzero(s.h)==0
    with np.errstate(divide='raise', invalid='raise'):
        for omega in [0., .003]:
            f, levels, d, _ = hierarchy(s, 1., omega)
            assert f['H']==0 and f['chi_yxx']==0
            assert np.isnan(f['Q']) and np.isnan(f['Q_A'])
            for level in levels:
                assert abs(level['H']-f['H'])==0
                assert np.isnan(level['error_H'])
                assert np.isnan(level['H_error_over_H0'])
            assert np.isnan(d['dual_projection_relative'])
            assert d['signed_H_error']==0 and d['orthogonal_adjoint_bound']==0


def test_contact_tilt_reversal_and_symmetry_zero():
    responses=[]
    for tilt in [-.15, 0., .15]:
        s=PreparedSystem(RevisionParameters(n=64,t_A=tilt,xi=0))
        f,levels,_,_=hierarchy(s,.3)
        responses.append(f['H'])
        if tilt==0:
            assert abs(f['H']) < 1e-12
            assert np.isnan(f['Q']) and np.isnan(levels[3]['error_H'])
        f0,_,_,_=hierarchy(s,0.)
        assert abs(f0['H']-s.H0) < 1e-12
    assert abs(responses[0]+responses[2]) < 1e-12


def test_resolvent_high_frequency_is_an_algebraic_not_interband_prediction():
    s=PreparedSystem(RevisionParameters(n=48,xi=.1,delta_P=.4))
    L=s.L0+.3*s.K
    # Formal matrix limit only: this frequency need not be semiclassically valid.
    omega=1e4*eigvalsh(L)[-1]
    g=solve(L+1j*omega*np.eye(len(L)),s.b,assume_a='sym')
    assert norm(1j*omega*g-s.b)/norm(s.b) < 1.0001e-4
    assert abs(1j*omega*(s.h@g)-s.h@s.b) <= norm(s.h)*norm(1j*omega*g-s.b)


def test_grouped_residues_ignore_degenerate_eigenvector_rotations():
    rates=np.array([1.,1.,3.,5.]);b=np.array([1.,2.,3.,4.]);h=np.array([2.,-3.,4.,1.])
    angle=.37;Q=np.eye(4)
    Q[:2,:2]=[[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]]
    L=np.diag(rates)
    first=core.mode_groups(L,b,h)
    rotated=core.mode_groups(Q@L@Q.T,Q@b,Q@h)
    assert first[0]['multiplicity']==2
    for a,c in zip(first,rotated):
        for key in ['lambda_rate','R_L','R_H']:
            assert a[key]==pytest.approx(c[key],abs=1e-12)
