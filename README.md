# Hall-silent valleys in anomalous-velocity nonlinear Hall transport

A conducting valley can have zero direct Berry-curvature Hall weight while still changing the Hall response through collisions. This repository accompanies **When Can Hall-Silent Valleys Be Neglected in Anomalous-Velocity Nonlinear Hall Transport?**

## Author and publication status

**Youhan Wanigasuriya** (sole and corresponding author)

Department of Chemistry, Faculty of Science, University of Colombo, Colombo 00300, Sri Lanka

Email: youhanwanigasuriya@gmail.com

ORCID: [0009-0005-8443-837X](https://orcid.org/0009-0005-8443-837X)

Target: **Physical Review B, Regular Article**. The version 1.1.0 research code/data snapshot is on `prb-submission`. The existing public `main` contains the earlier revision. No journal submission or manuscript preprint deposit has occurred.

Version **1.1.0** is the existing software version retained for this research snapshot. Identify the exact revision with its full Git commit hash; no GitHub release or tag is assigned. A Zenodo DOI remains pending. [Citation metadata](CITATION.cff) accompanies the code/data package. In the author's full local checkout, PRB_Submission_Readiness.md and ZENODO_Release_Metadata.md record submission and archive preparation; these administrative documents are excluded from the code/data branch and ZIP.

This research received no external funding. The author declares no competing interests. No additional individuals or institutions are acknowledged.

## Rights

No additional software license is granted by the author for this preparation. Public visibility does not itself grant permission to reuse the research code. Third-party dependencies retain their own licenses and notices. No new repository license or rights grant is included.

## Main result

Exact sector elimination and an ordered physical mode hierarchy separate active current, active valley distortion, passive current and passive valley polarization. Contact disorder closes on this space. Finite-range leakage has an observable-dependent effect. On the specified 3,510-point positive-coupling DC map, four modes reproduce the Hall response within 0.36%; safe omission of the entire passive sector is a separate, tolerance-dependent decision.

## Repository contents

- `src/nonlinear_hall/`: model, independent numerical checks, physical projection and figures.
- `tests/`, `scripts/`, `config/`: automated tests, portable entry points and explicit final settings.
- `data/processed/`, `validation/`: one canonical copy of each retained table and concise validation summaries.
- `figures/main/`, `figures/supplement/`: final vector figures and previews.
- Author's full local checkout only: `manuscript/`, `supplement/` contain LaTeX sources and compiled PDFs; they are excluded from the code/data branch and ZIP pending separate distribution approval.
- `docs/`: numerical conventions, provenance, retained validation summaries and the exact code/data inventory.

The branch's tracked snapshot contains exactly the files listed in [docs/release_files.txt](docs/release_files.txt). The research ZIP contains those same files plus a generated SHA256SUMS file. Both exclude manuscript/supplement sources and PDFs, claim ledgers quoting manuscript text, cover letters and submission records. Those files remain intact in the author's local checkout. This exclusion does not remove earlier files from public `main` or Git history. Public distribution of the revised manuscript is a separate author decision; a software/data deposit is not permission to publish the paper.

## Installation

For the ZIP, extract it and work from its single top-level directory; verify `SHA256SUMS` before installation and skip the two Git commands below. For GitHub, clone `prb-submission`; cloning the default `main` retrieves the earlier version.

Use Python 3.12 for the pinned environment. Other Python versions compatible with the package may produce small numerical differences.

```sh
git clone --branch prb-submission https://github.com/YouhanCW/nonlinear-hall-valley-omission.git
cd nonlinear-hall-valley-omission
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
```

LaTeX is unnecessary for the code/data archive. Building documents in a separately approved full checkout requires `pdflatex`, `bibtex`, REVTeX 4.2 (`revtex4-2.cls` and `apsrev4-2.bst`), and the packages listed in the document preambles.

## Quick validation

```sh
make test
make validate
```

Validation verifies dataset hashes, runs independent physics checks, and recomputes a finite-range representative at the production angular resolution.

## Reproduce main results

```sh
make reproduce-core
```

This recomputes the 3,600-point principal map, two-kernel ablation, invariant and spectral residuals, fixed-budget decisions, four representative mechanism coefficients and finite-mass controls. It compares all 13 central tables numerically with the included canonical data. New results go to ignored `build/reproduced/`; canonical inputs are never silently replaced. Eigenvector coordinates can depend on the numerical environment; use the pinned environment for the strict table comparison.

## Reproduce figures

All five main and four supplementary figures and their input data are included. To regenerate them from the code/data ZIP, use the existing generators in an extracted working copy:

```sh
PYTHONPATH=src MPLCONFIGDIR=build/matplotlib python - <<'PYCODE'
from pathlib import Path
from nonlinear_hall.mode_ablation_figures import make_figures
from nonlinear_hall.supporting_figures import make_supporting_figures
make_figures(Path('.'))
make_supporting_figures(Path('.'))
PYCODE
```

The original `make figures` target is for the full manuscript checkout: it additionally builds supplemental TeX tables and a claim ledger that reads manuscript text. Those manuscript inputs are deliberately absent from this code/data archive. The computational figure generators above do not require them.

## Build manuscript (full checkout only)

Manuscript sources and PDFs require separate distribution approval and are not in this branch's tracked snapshot or the code/data ZIP. The following target applies only when those sources are separately present.

```sh
make paper
```

The build verifies data, regenerates figures/tables and compiles both documents, rejecting missing inputs, unresolved references and overfull boxes. `make clean` removes disposable builds, caches and LaTeX auxiliary files, retaining final figures and PDFs.

## Data

[DATA_MANIFEST.md](DATA_MANIFEST.md) lists every included dataset and checksum. [REPRODUCIBILITY.md](REPRODUCIBILITY.md) gives the clean-clone workflow. The full checkout also retains a manuscript claim ledger, excluded from this archive because it quotes manuscript text. Canonical physical analysis: `20260919T021436Z-40be24e6`.

## Scientific scope and limitations

The calculation covers the anomalous-velocity channel in a homogeneous, zero-temperature, phenomenological four-valley model with reversible Born scattering and restricted disorder ensembles. It does not calculate all nonlinear Hall channels, predict quantitative SnTe transport, establish universal error thresholds, or provide a complete experimental device signal. Scalar/shape pieces are projection diagnostics, not separately measurable microscopic currents.
