# A computer-assisted bound: Λ ≤ 0.107964910079

**Dale James Raymond · Research preprint · Version 1.0 · 29 October 2026**  
**Published paper and complete evidence:** [Zenodo record 23752103](https://zenodo.org/records/23752103)  
**Version-specific DOI:** [10.5281/zenodo.23752103](https://doi.org/10.5281/zenodo.23752103)

## The bound and proof package

The 63-page manuscript presents a computer-assisted proof of the unconditional bound, in the Polymath normalisation,

```text
Λ ≤ 427693072077942473661578098491 /
    3961408125713216879677197516800
  < 0.107964910079.
```

The argument combines **OpenAI's ordinary-zeta nonvanishing theorem for Re(s) > 7/8**, formalised in Lean, with the manuscript's analytic heat-flow argument and exact or directed interval computations. The external theorem is identified in [The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re(s) > 7/8](https://github.com/openai/math/blob/main/preprints/The-Quasi-Riemann-Hypothesis-September-30-2026/paper.pdf). Its [Lean source](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/lean/OAI/NumberTheory/DirichletL/Nonvanishing.lean) is pinned to commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`; the ordinary-zeta declaration is `OAI.riemannZeta_ne_zero_of_seven_eighths_lt_re`.

Appendix B directly reconstructs all **67 source chords**. The `direct-source` consumer binds all **268 operational source fields**, and the complete finite replay has **15 stages**. The exact comparison covers **221,010 arcs**, their outward rounding and joins, and the full terminal de Bruijn contraction `T + Q_T/2`.

This repository is a lightweight companion to the published deposit, following the format of the [0.116398 companion](https://github.com/Dale-Dug/de-bruijn-newman-0116398). The imported Lean theorem, written analytic argument and numerical checks have distinct verification scopes, set out in the publication and its guide.

## Research overview

Dale James Raymond · [ORCID 0009-0001-1682-8529](https://orcid.org/0009-0001-1682-8529)

- **8 September 2026:** [Phase-correlated certificates, Λ < 0.163297](https://zenodo.org/records/22626161).
- **21 September 2026:** [Correlated translated probes, Λ < 0.149396](https://zenodo.org/records/22867547).
- **10 October 2026:** [Retuned translated probes, Λ < 0.116398](https://zenodo.org/records/23272725), published with an original conditional title; see the [current mathematical status](https://github.com/Dale-Dug/de-bruijn-newman-0116398#current-mathematical-status--26-october-2026).
- **29 October 2026:** [A computer-assisted bound, Λ ≤ 0.107964910079](https://zenodo.org/records/23752103).

GitHub companions: [0.149396](https://github.com/Dale-Dug/de-bruijn-newman-0149396) · [0.116398](https://github.com/Dale-Dug/de-bruijn-newman-0116398) · [0.107964910079](https://github.com/Dale-Dug/de-bruijn-newman-0107965). The shorter repository and file names record the upward six-decimal ceiling `0.107965`.

## Read the publication

1. [Main paper](deposit/Unconditional_0107965.pdf) and [editable LaTeX](deposit/Unconditional_0107965.tex)
2. [Matched-source supplement](deposit/Matched_Source_Supplement.pdf)
3. [Verification guide](deposit/Verification_Guide.pdf) and [recorded execution receipt](deposit/Verification_Receipt.json)
4. [Complete manuscript sources](deposit/Manuscript_Sources.zip)
5. [Further Consequences](deposit/Further_Consequences.pdf), a separate note

The two historical papers are [Prior Analytic Foundations](deposit/Prior_Analytic_Foundations.pdf) and [Prior Correlated Translated Probes](deposit/Prior_Correlated_Translated_Probes.pdf). Their original bytes and notices are preserved; the current main manuscript and matched-source supplement state the argument for this edition.

## Preserved archival files and citation

All **15 files** in [`deposit/`](deposit/) are exact copies of the published release. The root [CITATION.cff](CITATION.cff) also preserves the published citation, including the preferred manuscript citation and version-specific DOI. The GitHub landing page and helper files sit outside the canonical deposit directory.

The sixteenth file, **Proof_and_Replay.zip**, remains on Zenodo. It is **201,060,812 bytes** and has SHA-256:

```text
bf5c7b3dca9e17e84e146ecc5ca0c6f671b409613088212e3f0b8a0b15f6aaf6
```

## Verify and restore the complete deposit

[Download full Proof_and_Replay.zip from Zenodo](https://zenodo.org/api/records/23752103/files/Proof_and_Replay.zip/content). The scientific inputs, consumers, arithmetic runtime and support evidence are in that archive.

The companion helpers use only Python's standard library. The commands below use **Python 3.12**, matching the documented replay runtime. First check this companion's file identities:

```sh
python3.12 -B Verify_GitHub_Files.py
```

To download the pinned archive and restore all 16 original files into a new directory outside this repository:

```sh
python3.12 -B Prepare_Replay.py --download --output ../zenodo_23752103 --verify-deposit
```

Or reuse an exact local copy without another network transfer:

```sh
python3.12 -B Prepare_Replay.py --archive /path/to/Proof_and_Replay.zip \
  --output ../zenodo_23752103 --verify-deposit
```

The helper checks every original file's size and SHA-256, preserves its filename, and runs the unchanged `Verify_Deposit.py` when `--verify-deposit` is supplied. That checker inspects archive contents, source identities, recorded replay bindings and the exact terminal arithmetic. It does not execute the fifteen mathematical stages. Existing output directories are never overwritten; a failed restoration is removed.

The restored directory must retain exactly the 16 original files for deposit verification. Extract the scientific archive into a separate directory for replay. From the directory containing the extracted `Proof_and_Replay/` folder:

```sh
python3.12 Proof_and_Replay/Lambda_Peer_Review/verify_bundle.py \
  --all --jobs 4 --work lambda-replay-output
```

Use the documented **Linux x86_64 CPython 3.12** arithmetic runtime, keep assertions enabled, and choose a fresh work directory outside `Lambda_Peer_Review/`. The bundled arithmetic versions are python-flint 0.8.0 and FLINT 3.3.1. Follow the [verification guide](deposit/Verification_Guide.pdf) for platform details, stage dependencies and the compatible-runtime option.

## Verification boundary

The published receipt records a passing fifteen-stage execution. The direct-source stage establishes the final assembly and binding identities; its prerequisite primitive, spectral, physical, arithmetic and derivative inequalities are checked by the other consumers and supported by the written argument. Global contact, localisation and the application of the initial ordinary-zeta theorem remain mathematical obligations described in the manuscript.

This GitHub preparation checks file identity and restoration of the published package. It performs no fresh fifteen-stage mathematical replay, full Lean rebuild or end-to-end Lean formalisation. Review targets and reproducibility-report guidance are in [REVIEW.md](REVIEW.md).

## Rights and provenance

The published record uses **CC BY 4.0 for author-owned publication documents**. Software, numerical data and third-party material retain their component-specific rights. See the [rights pointer](LICENSES_AND_RIGHTS.md) and the unchanged [original notice](deposit/LICENSES_AND_RIGHTS.md).

AI assistants contributed to derivations, code, exposition and internal checks; Dale James Raymond is responsible for the submission. Exact source URLs, file sizes, hashes and the scope of companion preparation are recorded in [REPOSITORY_PROVENANCE.json](REPOSITORY_PROVENANCE.json).
