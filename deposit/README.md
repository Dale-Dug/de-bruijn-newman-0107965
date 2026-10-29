# A computer-assisted bound for the de Bruijn-Newman constant

**Dale James Raymond | Version 1.0 | 29 October 2026**  
Version: `1.0`  
ORCID: [0009-0001-1682-8529](https://orcid.org/0009-0001-1682-8529)  
DOI: [10.5281/zenodo.23752103](https://doi.org/10.5281/zenodo.23752103)

## The manuscript and its result

Start with `Unconditional_0107965.pdf`. In the Polymath normalisation, the manuscript presents the computer-assisted bound

```text
Lambda <= 427693072077942473661578098491 /
          3961408125713216879677197516800
       < 0.107964910079.
```

The argument combines OpenAI's ordinary-zeta nonvanishing theorem for `Re(s) > 7/8`, formalised in Lean, with the manuscript's analytic heat-flow argument and exact or directed interval computations. The endpoint includes the complete terminal de Bruijn contraction `T + Q_T/2`. The shorter filename records the upward six-decimal ceiling `0.107965`.

Appendix B, Theorem B.1, now derives all 67 physical source chords from their native moments, finite coefficient capacities, arithmetic payments, physical refunds and derivative functionals. The additional `direct-source` consumer reconstructs all 268 operational source fields and explicitly binds the actual scalar main terms and final derivative operators. The matched-source supplement explains those dependencies and the verification guide gives the supported commands.

## Identity of this edition

This edition supersedes referee edition 3 of 28 October 2026; the numerical plan, source table and comparison history are unchanged; Appendix B adds the direct source reconstruction.

The original 14 scientific consumers are retained byte for byte. The replay driver and bundle verifier are updated, and the new direct-source consumer adds a fifteenth stage. The referee-edition-3 manuscript and the source-change record are preserved under `Proof_and_Replay/Release_Support/reconstruction/`. The two historical `Prior_*.pdf` files remain unchanged.

This research preprint is accompanied by its sources and computational evidence. The manuscript and verification guide state the mathematical and computational verification scopes.

## Public file inventory

Keep these sixteen files together.

| File | Purpose |
| --- | --- |
| `Unconditional_0107965.pdf` | Current main proof and analytic appendices |
| `Unconditional_0107965.tex` | Matching standalone main LaTeX source |
| `Matched_Source_Supplement.pdf` | Exact source construction, functional identities and dependencies |
| `Further_Consequences.pdf` | Deductions from the stated terminal-strip conclusion |
| `Verification_Guide.pdf` | Integrity, mathematical replay and document-build instructions |
| `Prior_Analytic_Foundations.pdf` | Unchanged historical foundations paper |
| `Prior_Correlated_Translated_Probes.pdf` | Unchanged historical translated-probe paper |
| `Manuscript_Sources.zip` | Current document sources, build instructions and prior sources |
| `Proof_and_Replay.zip` | Scientific inputs, consumers, runtime, provenance and review evidence |
| `README.md` | This entry point |
| `CITATION.cff` | Package citation and preferred manuscript citation |
| `LICENSES_AND_RIGHTS.md` | Component-specific rights and attribution |
| `Release_Manifest.json` | Release identity and fourteen public payload identities |
| `Verification_Receipt.json` | Verification status and evidence for this exact edition |
| `Verify_Deposit.py` | Delivered-file, archive and identity checks |
| `SHA256SUMS.txt` | SHA-256 hashes of the other fifteen files |

## Check the delivered files

From the directory containing the sixteen public files:

```sh
python3 Verify_Deposit.py
```

The deposit verifier checks delivered identities and archive consistency. An integrity pass establishes that the described files are present and agree with the release specification. It does not execute every mathematical consumer or establish the written analytic arguments. The manifest covers fourteen payloads; `SHA256SUMS.txt` also covers the manifest. Neither file attempts a circular self-hash.

## Replay all fifteen finite stages

Extract `Proof_and_Replay.zip`. From the directory containing `Proof_and_Replay/`, using the supplied Linux x86_64 CPython 3.12 arithmetic runtime:

```sh
python3.12 Proof_and_Replay/Lambda_Peer_Review/verify_bundle.py \
  --all --jobs 4 --work lambda-replay-output
```

Use a fresh work directory outside `Lambda_Peer_Review/` and keep Python assertions enabled. The bundled arithmetic runtime is python-flint 0.8.0 with FLINT 3.3.1. The inner replay guide describes platform requirements and the `--runtime` option for a compatible replacement. The supported finite replay uses the extracted inputs and does not require the author's former workspace or online accounts.

The required stages are `native`, `activation`, `spectral`, `affine`, `heads28`, `heads39`, `wall`, `overlays`, `kernel`, `arcs`, `compact-arcs`, `interfaces`, `physical-debit-map`, `arithmetic-credit-map` and `direct-source`. The driver schedules their dependency groups. A complete run must report all fifteen stages.

For the lighter inventory and exact endpoint calculation:

```sh
python3 Proof_and_Replay/Lambda_Peer_Review/verify_bundle.py --endpoint
```

That command does not verify the source, continuous kernels or every comparison arc. `Verification_Receipt.json` governs the recorded execution status of this exact release, including the inputs, runtime, stage results and evidence locations. Historical fourteen-stage receipts apply to their own earlier source and are not evidence of a fifteen-stage execution.

## Mathematical assurance and provenance

The package contains all 67 source/kernel rows and the full comparison flow. The direct-source stage proves the final assembly and binding identities. Its primitive, spectral, arithmetic, physical and jet inequalities remain obligations of the separate consumers and written arguments. The complete proof also requires the global contact argument and the cited initial ordinary-zeta theorem.

The imported OpenAI Lean source is pinned to commit `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. This release does not claim a new full Lean build or an end-to-end Lean formalisation of the Lambda theorem. Negative guard tests have the limited scope stated in their reports.

The corrected Rodgers-Tao reference is *Forum of Mathematics, Pi* **8** (2020), e6, DOI [10.1017/fmp.2020.6](https://doi.org/10.1017/fmp.2020.6). Related prior works are [10.5281/zenodo.23272725](https://doi.org/10.5281/zenodo.23272725), [10.5281/zenodo.22867547](https://doi.org/10.5281/zenodo.22867547) and [10.5281/zenodo.22626161](https://doi.org/10.5281/zenodo.22626161). They identify separate publications, not this record's DOI.

Author-owned publication documents retain the agreed CC BY 4.0 scope. Software, numerical data and third-party material retain their applicable component-specific rights. Four contextual reference copies remain excluded from the public archive; exact citations, URLs and hashes identify them. Their exclusion removes no numerical replay dependency. See `LICENSES_AND_RIGHTS.md` for the complete scope.
