# Licences, rights and attribution

**Dale James Raymond | Version 1.0 | 29 October 2026**  
DOI: [10.5281/zenodo.23752103](https://doi.org/10.5281/zenodo.23752103)

## Author-owned publication documents

The main manuscript, current source supplement, consequences note, verification guide and author-owned publication documentation retain the agreed [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) scope. Version 1.0 includes the direct-source appendix and the recorded publication revisions.

The two `Prior_*.pdf` files retain the attribution and rights of the author's earlier deposit, [10.5281/zenodo.23272725](https://doi.org/10.5281/zenodo.23272725). Their bytes are unchanged. Historical texts remain identifiable as historical; the current manuscript and matched-source supplement state the argument governing this edition.

## Code, numerical data and archive contents

The documentation licence does not relicense software, numerical data, binaries or third-party works. Existing component notices remain in force. No blanket software licence is assigned to previously unlicensed author-written code, including newly added verification code. Rights not expressly licensed remain with their respective holders. The top-level software type in `CITATION.cff` describes the package and does not impose a licence on every embedded file.

This edition supersedes referee edition 3 of 28 October 2026; the numerical plan, source table and comparison history are unchanged; Appendix B adds the direct source reconstruction. The original fourteen scientific consumers, numerical inputs and arithmetic runtime are preserved. The manuscript, replay driver and bundle verifier are revised, and a direct-source consumer is added. The original files and declared transformations are preserved under `Proof_and_Replay/Release_Support/reconstruction/`. The current manifests identify the delivered bytes; historical manifests identify their earlier editions.

## Arithmetic runtime and corresponding source

The bundled runtime comprises python-flint 0.8.0, FLINT 3.3.1, GMP 6.3.0 and MPFR 4.2.2. The applicable MIT and LGPL notices are retained. Exact-version upstream source distributions, the python-flint build recipe, full GPL version 3 and LGPL version 3 licence texts, and source URLs and hashes accompany the binaries under `Proof_and_Replay/Release_Support/third_party_sources/`.

The preserved runtime payload was compared with its corresponding official PyPI wheel in the earlier provenance record. The runtime provenance record does not establish a fresh source build or byte-for-byte reproduction of the wheel from source. The replay accepts a compatible alternative arithmetic installation through `--runtime`. Nothing in the documentation licence restricts modification, debugging or other rights granted by the applicable software licences.

## External theorem sources and contextual references

The retained OpenAI theorem sources, Mathlib-related material and applicable compatibility-patch sources retain their Apache-2.0 notices. Their licence texts and provenance are included. OpenAI's ordinary-zeta nonvanishing theorem is an identified external mathematical input; inclusion does not imply OpenAI's review or endorsement of the final Lambda argument.

The public derivative continues to exclude four contextual copies for which a general redistribution grant was not established:

1. The cited Polymath heat-flow article PDF, arXiv:1904.12438v2.
2. The cited Platt-Trudgian verification-height article PDF, arXiv:2004.09765v1.
3. The external verifier's `lean_build_report.md`.
4. The external verifier's `QRHCheck.lean` comparator source.

Exact titles, pinned URLs, sizes and hashes are recorded in `Release_Support/third_party_sources/EXTERNAL_REFERENCE_LOCATIONS.json` and `EXCLUDED_REFERENCE_FILES.json` inside the proof archive. These exclusions remove no numerical replay input or scientific consumer. The attributed factual axiom output and the author's `RootZetaChallenge.lean` remain included. No general licence is asserted for the external verifier's repository.

## Attribution and review scope

The manuscript bibliography identifies the mathematical sources. AI assistants contributed to derivations, code, exposition and internal checks; Dale James Raymond remains the named author responsible for the submission. Internal audits, guard tests and finite replay receipts have their stated scopes and are not external journal referee reports.

This package claims neither a fresh full Lean rebuild nor an end-to-end formalisation of the complete Lambda proof. No affiliation, funding, journal acceptance or third-party endorsement is supplied or inferred. No standalone font files are distributed.
