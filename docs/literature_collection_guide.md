# Literature Collection Guide

This guide defines what to collect for the microgravity solidification literature review and how each paper should be converted into the project schema. It is based on the existing Word draft in `/Users/rduggineni/Downloads/solidLItReview/LitArchive/Solidification Processing Under Microgravity vs.docx` and the current nine-domain wiki pipeline.

## Goal

Build a traceable corpus that explains how metallic alloy solidification changes between Earth gravity and microgravity, using Flemings' *Solidification Processing* as the theory spine. Every useful source should support at least one of these outputs:

- a narrative claim in `microgravity_solidification_wiki.md`
- a quantitative row in `1g_vs_microgravity_benchmark_table.md`
- a variable range/statistic in `variable_groups_consolidated.md`
- a gap-matrix cell in `gap_matrix.md`

Do not enter unsupported values. If a paper is useful but the numeric data still needs table or figure extraction, add the record as `qualitative` or `quantitative_partial` and include a clear `gap_flags` entry.

## Collection Workflow

1. Start with the priority reading list below.
2. For each paper, save the PDF in `data/pdfs/` if available.
3. Enter verified metadata and extracted content in `data/manual_records/*.json`.
4. Validate records:

```bash
python3 -m ilm_wiki.cli validate-records --manual-dir data/manual_records
```

5. Regenerate outputs:

```bash
python3 -m ilm_wiki.cli run --pdf-dir data/pdfs --manual-dir data/manual_records --output-dir output
```

6. Check `output/qa_report.json` for domains still below minimum source count.

## Priority Reading Order

Read these first because they define the structure of the review.

| Priority | Source Type | Why It Matters | Target Domains |
| --- | --- | --- | --- |
| 1 | ISS-EML thermophysical-property review | Broad orientation to microgravity containerless processing, property measurement, and undercooling. | D1, D5, D6 |
| 2 | ISS-EML rapid-solidification review | Connects rapid solidification, model validation, alloy classes, and additive manufacturing relevance. | D1, D5, D8, D9 |
| 3 | Akamatsu et al. DECLIC/Transparent Alloys review | Best map of ISS in situ pattern-formation experiments. | D3, D4 |
| 4 | Glicksman/Koss IDGE papers | Foundational dendrite-growth benchmark under diffusion-controlled conditions. | D3 |
| 5 | Al-Cu and Al-Si gravity-comparison papers | Direct metallic alloy comparison between 1g and reduced gravity. | D1, D2, D3, D4 |
| 6 | Immiscible Al-Bi-Sn / Al-Pb / Al-In papers | Best route into monotectic, immiscible, Marangoni, and sedimentation separation. | D4, D8 |
| 7 | Detached Bridgman reviews and semiconductor case studies | Covers crystal-quality branch and gap formation. | D7 |
| 8 | LPBF keyhole porosity papers | Provides the AM bridge for gas pores and rapid melt-pool solidification. | D8, D9 |
| 9 | Mechanical-property papers on returned space samples | Highest gap area; search deliberately and record missing evidence. | D9 |

## Inclusion Rules

Include a source when it meets one or more of these criteria:

- Reports a microgravity, reduced-gravity, drop-tube, sounding-rocket, Shuttle, ISS, Tiangong, CSS, or parabolic-flight solidification experiment.
- Provides a direct 1g vs microgravity comparison.
- Supplies ground theory needed to interpret microgravity results, especially Flemings-aligned transport, dendrite, eutectic, macrosegregation, nucleation, or porosity models.
- Reports thermophysical properties of metallic melts using microgravity/containerless methods.
- Reports returned-sample properties or defects from microgravity-solidified materials.
- Provides additive manufacturing pore/melt-pool data useful for the D8 bridge.

Exclude or defer:

- Papers with no DOI/reference trail.
- Pure simulation papers unless they validate against a microgravity experiment or provide a required benchmark model.
- Space manufacturing opinion pieces with no materials data, unless used only in the introduction or gap section.
- Duplicate conference abstracts when a peer-reviewed article exists.

## Evidence Labels

Use these consistently in `seed_literature.json` or new manual files:

| Label | Meaning |
| --- | --- |
| `review` | Synthesizes a field or program; useful for narrative but not usually table values. |
| `experiment` | Reports primary experimental data. |
| `benchmark` | Designed for model validation or direct 1g vs microgravity comparison. |
| `model` | Primarily theoretical or computational, with relevance to a measured phenomenon. |
| `technical_report` | Grey literature or mission report; use when peer-reviewed data is unavailable. |

Use these extraction statuses:

| Status | When To Use |
| --- | --- |
| `metadata_only` | Citation is known, but no claim or variable has been extracted yet. |
| `qualitative` | Claims are extracted, but no numeric values are entered. |
| `quantitative_partial` | Some numeric values are entered, but tables/figures are still incomplete. |
| `quantitative_complete` | All domain-relevant numeric values available in the paper have been extracted. |

## Domain Collection Requirements

### D1 - Alloy Systems & Processing Routes

Collect one record per distinct experiment or alloy/facility combination.

Required content:

- alloy system and composition
- platform: ISS, Shuttle, Tiangong, CSS, TEXUS, MASER, FOTON, parabolic flight, drop tube, drop shaft
- facility: ISS-EML, DECLIC-DSI, Transparent Alloys, MEPHISTO, CETSOL, MICAST, AGHF, TEMPUS, PFMI
- solidification technique: Bridgman, directional solidification, electromagnetic levitation, electrostatic levitation, float-zone, containerless, drop-tube solidification
- sample dimensions and mission duration if reported
- year, mission, and processing route

Useful search strings:

- `"ISS EML metallic alloy solidification"`
- `"CETSOL MICAST Al Cu microgravity directional solidification"`
- `"TEMPUS electromagnetic levitation undercooled alloy space"`
- `"Tiangong microgravity solidification Al Bi Sn"`
- `"TEXUS MASER directional solidification alloy"`

### D2 - Fluid Flow, Convection, and Macrosegregation

Prioritize papers with explicit 1g vs microgravity segregation comparison.

Extract:

- macrosegregation profile or index
- solute concentration profiles along axial and radial directions
- convection velocity if measured or inferred
- Rayleigh, Grashof, Marangoni, Peclet, or Schmidt numbers
- gravity term or porous-medium/Darcy model used
- whether flow is buoyancy-driven, shrinkage-driven, Marangoni-driven, or g-jitter-driven

Key theoretical anchors:

- Flemings Ch. 7 macrosegregation
- Mehrabian-Keane-Flemings interdendritic flow
- Tiller/BPS solute redistribution
- thermosolutal convection and mushy-zone permeability

### D3 - Dendritic and Cellular Solidification

This is the core microstructure domain. Separate transparent analogs from metallic alloys.

Extract:

- primary dendrite arm spacing, `lambda1_um`
- secondary dendrite arm spacing, `lambda2_um`
- dendrite tip radius and tip velocity
- undercooling
- thermal gradient `G_K_per_m`
- growth velocity `V_um_per_s`
- cooling rate
- CET threshold or CET position
- model comparison: LGK, KGT, Ivantsov, Hunt, phase-field, cellular automata

Flag:

- `transparent_analog_not_metal_alloy`
- `no_1g_benchmark`
- `figure_digitization_required`

### D4 - Eutectic, Peritectic, Polyphase, and Immiscible Systems

Split eutectic/peritectic pattern formation from monotectic/immiscible phase separation.

Extract:

- phase type: eutectic, peritectic, monotectic, immiscible
- lamellar/rod spacing
- Jackson-Hunt comparison, especially `lambda^2 V`
- phase morphology: lamellar, rod, anomalous, core-shell, dispersed droplets
- droplet size distribution
- coarsening rate
- sedimentation vs Marangoni interpretation
- wettability/contact angle if reported

Use microgravity papers to separate gravity sedimentation from Marangoni motion.

### D5 - Nucleation, Undercooling, and Interface Kinetics

Focus on containerless processing and undercooled melt cycles.

Extract:

- maximum undercooling
- nucleation temperature distribution
- nucleation mechanism: homogeneous, heterogeneous, surface, impurity, wall/contact
- recalescence velocity or interface velocity
- metastable phases
- number of cycles and atmosphere/vacuum condition
- stirring or shear-rate condition for EML experiments

Flag curves that need digitization:

- `velocity_undercooling_curve_requires_digitization`
- `nucleation_distribution_requires_digitization`

### D6 - Thermophysical Properties, Heat Flow, and Plane-Front Stability

This domain should become a property database.

Extract:

- density
- viscosity
- surface tension
- specific heat
- thermal conductivity
- thermal diffusivity
- emissivity
- electrical resistivity if linked to liquid structure
- temperature range
- measurement method: oscillating drop, AC calorimetry, pyrometry, optical density, inductive density
- uncertainty values

For plane-front stability:

- critical velocity
- constitutional supercooling threshold
- `G/V`
- whether the boundary layer matched BPS/Tiller theory

### D7 - Detached Bridgman and Semiconductor Crystal Quality

Collect both microgravity discovery papers and ground reproductions because detachment is a mechanism, not just a platform.

Extract:

- material: GaAs, InSb, GaSb, GeSi, CdTe, Si, Ge
- crucible material
- ampoule geometry
- gap width
- contact angle
- growth angle
- pressure differential
- thermal gradient and growth rate
- etch pit density
- dislocation density
- XRD rocking-curve FWHM
- resistivity uniformity
- impurity segregation profile

Flag missing property metrics:

- `EPD_missing`
- `rocking_curve_missing`
- `gap_width_only_no_quality_data`

### D8 - Gas Porosity, Bubble Behaviour, and AM Bridge

Keep two separate evidence streams: microgravity pores/bubbles and additive manufacturing keyholes.

Microgravity extraction:

- pore volume fraction
- mean pore diameter
- pore morphology
- gas concentration, especially hydrogen in aluminum
- bubble rise or migration velocity
- Marangoni migration if reported
- shrinkage cavity behavior

AM bridge extraction:

- AM process: LPBF, DED, EBM
- alloy
- pore type: keyhole, lack-of-fusion, gas, shrinkage
- porosity fraction
- pore diameter
- laser power, scan speed, spot size
- cooling rate
- keyhole frequency or collapse mechanism
- whether gravity is negligible by rapid timescale argument

### D9 - Processing-Structure-Property and Mechanical Data

This is the biggest gap. Search deliberately for returned-sample mechanical testing.

Extract:

- grain size
- UTS
- yield strength
- elongation
- hardness
- fatigue limit
- creep rate
- Young's modulus
- fracture mode
- whether the same alloy has both microstructure and mechanical data

Use `gap_flags` aggressively:

- `mechanical_property_data_absent`
- `sample_too_small_for_tensile_testing`
- `only_hardness_reported`
- `no_1g_property_benchmark`

## Benchmark Pairing Rules

Only enter a benchmark row when both values are traceable.

Use `benchmark_match_type`:

- `intra_study`: same paper compares 1g and microgravity.
- `inter_study`: values come from different papers but same alloy/composition and similar process conditions.
- `none`: no benchmark pair yet.

For inter-study pairing, record why the pair is acceptable:

- composition match
- `G` within +/-10%
- `V` within +/-10%
- same thermal gradient class if exact value is unavailable
- same facility type or comparable processing route

If conditions do not match, do not force a benchmark. Add a gap flag instead.

## Required Manual Record Fields

Every useful paper should have:

- `domain`
- `citation.title`
- `citation.authors`
- `citation.year`
- `citation.journal`
- `citation.doi` or `citation.reference`
- `alloy`
- `composition`
- `platform`
- `facility`
- `review_summary`
- `key_findings`
- `theory_alignment`
- `extraction_status`
- `evidence_level`
- `variables`
- `gap_flags`
- `flemings_alignment`

## File Organization

Use this layout:

```text
data/
  pdfs/
    D3_Glicksman_1994_PRL.pdf
    D4_Jiang_2019_AlBiSn.pdf
  manual_records/
    seed_literature.json
    D1_processing_routes.json
    D2_macrosegregation.json
    D3_dendrites.json
    D4_polyphase.json
    D5_nucleation.json
    D6_properties.json
    D7_detached_bridgman.json
    D8_porosity_am_bridge.json
    D9_mechanical_properties.json
```

Keep PDFs named by domain, first author, year, and topic. Do not rely on downloaded filenames.

## Quality Checklist Before Adding a Record

- DOI or full reference is present.
- Source type is labeled.
- Claims are directly supported by the paper.
- Numeric values include units in the variable key.
- 1g and microgravity values are not mixed unless benchmark type is labeled.
- Missing data is represented as a gap flag, not invented.
- Transparent analogs are labeled separately from metallic alloys.
- Review papers are not treated as primary quantitative datasets unless they reproduce a table with citation.
- The record validates with `validate-records`.
- The regenerated wiki section still reads coherently.

## High-Priority Gaps To Fill Next

1. Direct 1g vs microgravity dendrite spacing data for metallic Al-Cu and Al-Si alloys.
2. Quantitative macrosegregation profiles for Al-Ni, Al-Cu, and Al-Si experiments.
3. Thermophysical-property tables for specific ISS-EML alloys with uncertainty values.
4. Detached Bridgman crystal-quality metrics: EPD, dislocation density, XRD FWHM.
5. Quantitative pore-size distributions in microgravity metallic solidification.
6. Mechanical properties of microgravity-solidified returned samples.
7. Matched AM cooling-rate and pore metrics for the D8 bridge.

