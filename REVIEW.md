# Independent review and reproducibility reports

## Mathematical and computational scope

The [Version 1.0 publication](https://zenodo.org/records/23752103) presents the computer-assisted bound **Λ ≤ 427693072077942473661578098491/3961408125713216879677197516800 < 0.107964910079**. Its initial strip uses OpenAI's ordinary-zeta nonvanishing theorem for Re(s) > 7/8, with the cited Lean source pinned to `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`.

The complete argument combines that external theorem, written analytic estimates and fifteen finite computational stages. The numerical replay and source-identity checks have their stated scopes; the published receipt is execution evidence and does not constitute external journal peer review or an end-to-end formalisation of the manuscript.

Useful review targets include:

1. The use of the ordinary-zeta theorem, the heat-flow normalisation and the initial squared-height bound `9/16`.
2. Finite-head localisation, attainment of a positive-time highest contact and the treatment of repeated nonreal contacts.
3. Appendix B's reconstruction of all 67 source chords and the binding of all 268 operational fields to their primitive, spectral, physical, arithmetic and derivative inputs.
4. The continuous-domain kernel inequalities, complete own-pair subtraction, future cutoffs and unbounded parameter ranges.
5. All 221,010 exact comparison arcs, outward rounding, joins and the complete terminal contraction `T + Q_T/2`.
6. The corrected `11/12` Gaussian remainder and the relationship between the current argument and the unchanged historical papers.

## Reproducibility reports

Include the version-specific DOI **10.5281/zenodo.23752103**, the file or commit identity, operating system, architecture, Python and arithmetic-library versions, exact command and earliest failing check. State which stages were executed and retain their output. The bundled replay profile is Linux x86_64 CPython 3.12 with python-flint 0.8.0 and FLINT 3.3.1.

Keep Python assertions enabled, use a new work directory outside the immutable evidence directory, and do not replace an unresolved interval sign with ordinary floating-point arithmetic. A report of all fifteen stages should identify every stage and its input/runtime identities.

For mathematical objections, identify the exact published section or assertion and distinguish an incorrect conclusion, an insufficient proof and a proof-to-code discrepancy. Proposed corrections should identify the affected version and preserve the archival files.

## Companion preparation

The GitHub companion preserves the fifteen mirrored publication files byte for byte and pins the remaining scientific ZIP by size and SHA-256. Its helpers check the companion manifest and restore the exact sixteen-file deposit into a new directory. The optional original deposit verifier checks archive identities, recorded replay bindings and the exact terminal arithmetic.

These preparation checks do not rerun the fifteen mathematical consumers or rebuild Lean. Their outcome and scope are recorded in [REPOSITORY_PROVENANCE.json](REPOSITORY_PROVENANCE.json); the published [Verification_Receipt.json](deposit/Verification_Receipt.json) retains the separate evidence for its recorded execution.
