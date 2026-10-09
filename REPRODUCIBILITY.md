# Reproducibility

The PRB research code/data version 1.1.0 is on `prb-submission`. Use its verified full commit identifier; do not substitute the earlier public `main` for this revision. Zenodo deposition and a DOI remain pending. A subsequently reserved DOI does not establish public archive availability. Record the actual release commit in external Zenodo metadata and release verification; do not embed a release commit inside the files that generate that same commit.

## Code/data archive workflow

The ZIP contains the 82 research payload files listed in `docs/release_files.txt` and one generated `SHA256SUMS` file. It omits all `manuscript/` and `supplement/` files, the manuscript claim ledgers and submission documents. Numerical modules whose filenames include `manuscript` remain included because they implement scientific calculations.

Extract the ZIP, enter `nonlinear_hall_valley_omission_v1.1.0`, and run:

```sh
shasum -a 256 -c SHA256SUMS
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
make test
make validate
```

`make validate` independently recomputes the existing N=256 finite-range representative against the canonical table. For a complete central-table reconstruction, run `make reproduce-core`; this is a longer existing calculation, not necessary for the representative archive smoke test. No canonical inputs are overwritten.

Use the two existing figure-generator calls documented in README.md to regenerate figures without manuscript files. `make figures`, `make paper`, `scripts/claims.py` and the standalone document-build action need the separately approved manuscript sources and are not the code/data-archive workflow. Their source is retained to support a full checkout; this omission does not prevent the numerical calculations, tests or independent figure generators from running.

The file-level manifest covers each of the 82 payload files, not itself. The ZIP's SHA-256 is supplied externally. Regenerate and verify the ZIP from the exact committed branch snapshot before archival deposition. Later DOI integration changes the snapshot and requires a new commit and rebuilt archive. Record the full commit externally, avoiding a self-referential commit identifier inside the archived files.

## Clone and reproduce the research code/data

Clone the research branch, then work from its root. Tested with Python 3.12 and the exact versions in `requirements-lock.txt`; no access to the original research directory or LaTeX installation is required. This clone excludes manuscript sources and PDFs.

```sh
git clone --branch prb-submission https://github.com/YouhanCW/nonlinear-hall-valley-omission.git
cd nonlinear-hall-valley-omission
# Verify git rev-parse HEAD against the final published commit before reproducing.
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-lock.txt
python -m pip install -e '.[test]'
make test
make validate
make reproduce-core
```

For figures, use the manuscript-independent generators in README.md. `make figures` and `make paper` apply only to a separate full checkout containing the excluded manuscript inputs; they are not clean-clone steps. Document compilation there requires `pdflatex`, `bibtex`, REVTeX 4.2 (`revtex4-2.cls` and `apsrev4-2.bst`), Latin Modern, natbib, geometry, microtype and the standard mathematics/graphics packages.

`make` uses `python3`; activate the intended virtual environment and use `make test PYTHON=python` when necessary. All targets set one BLAS/OpenMP thread. The plots use a local disposable Matplotlib cache under `build/`.

- **test**: independent Hamiltonian/Berry/symmetry/quadrature, conservation/PSD/zero modes, constant-lifetime, full/odd/Schur, frequency sign, texture covariance, mass, physical mode and checksum mutation tests. The targeted scientific audit also checks the weighted projector, contact moment closure, finite-range residual refinement, complex Hall magnitude/phase, relaxation-pole interlacing, zero-Hall denominator guards and degenerate-mode invariance. Run `python -m pytest -q -s tests/test_scientific_audit.py` to print its selected frequency/refinement summaries.
- **validate**: exact included-data hashes; 46 independent band/transport checks; an N=256 finite-range M1–M4 regression; fixed-budget dependent-point sign/budget assertions.
- **reproduce-core**: directly constructs all 3,600 principal points, 300 two-kernel rows, five representatives, four spectra, 64 mass rows and four mechanism coefficient rows. Produces 13 central tables in `build/reproduced/processed/` and a numerical comparison report. No archived source snapshot or previous calculation output is a computational input. The canonical tables are used only for comparison after reconstruction.
- **figures (full manuscript checkout only)**: regenerates all five main figures, four selected supplement figures, extended supplemental tables and the claim ledger from included canonical tables. The claim ledger requires manuscript sources and additionally reruns the six existing selected frequency/refinement tests; test dependencies are required. Other supporting control tables remain retained results and are not rerun by this target.
- **paper (full manuscript checkout only)**: runs figures, compiles main and supplement, and rejects missing inputs, overfull boxes and unresolved references/citations.
- **clean**: removes generated scratch outputs, caches and LaTeX auxiliaries. Canonical data and final figures/PDFs remain.

The comparison uses the full schema and keyed rows, absolute tolerance 1e-9 plus relative tolerance 1e-7 for floating-point cells, and exact categorical decisions. The production environment reproduces these comparisons; tiny residuals are not claimed as portable significant digits. Individual eigenvector signs/degenerate coordinates may change with LAPACK, so strict spectral-table reproduction should use the pinned environment. The physically meaningful signed sums, reconstruction identities and leakage powers are checked separately.

Canonical data have a fail-closed SHA-256 inventory in `data/manifest.json`. Deliberate scientific changes require reviewing the data, configuration, prose and manifest together; the pipeline never silently accepts new inputs. New calculations do not replace canonical files. To draw figures from a changed calculation, make an explicit reviewed data update rather than altering paths implicitly.

Only essential main calculations are rerun. The selected weak-series, convergence, certificate-cost, texture/gauge and open-circuit supporting tables carry original run and source hashes in `docs/source_provenance.json`; their figures regenerate directly from these included tables. Historical full scans and source snapshots remain in the original local scientific workspace and are unnecessary to use this release. No external archive is required.

In the full local checkout, `docs/release_verification.md` retains earlier release evidence and `PRB_Submission_Readiness.md` records current preparation. These historical/administrative records are excluded from the code/data ZIP; this archive retains `docs/validation_summary.md` and the canonical validation table as historical numerical evidence. Allow approximately 1 GB RAM and several minutes for warm numerical and document builds; dependency downloads and first font-cache construction take additional time.

Publication contact: Youhan Wanigasuriya, Department of Chemistry, Faculty of Science, University of Colombo, Colombo 00300, Sri Lanka; youhanwanigasuriya@gmail.com; ORCID https://orcid.org/0009-0005-8443-837X. No additional software license has been granted. Dependencies remain subject to their own licenses.
