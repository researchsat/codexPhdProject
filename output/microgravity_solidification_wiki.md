# Microgravity Metal Alloy Solidification - Literature Wiki

## Table of Contents
- [D1. Alloy Systems & Solidification Processing Routes](#d1-alloy-systems--solidification-processing-routes)
- [D2. Fluid Flow, Convection, and Macrosegregation](#d2-fluid-flow-convection-and-macrosegregation)
- [D3. Dendritic and Cellular Solidification](#d3-dendritic-and-cellular-solidification)
- [D4. Eutectic, Peritectic, Polyphase & Immiscible Systems](#d4-eutectic-peritectic-polyphase--immiscible-systems)
- [D5. Nucleation, Undercooling, and Interface Kinetics](#d5-nucleation-undercooling-and-interface-kinetics)
- [D6. Thermophysical Properties, Heat Flow & Plane-Front Solidification](#d6-thermophysical-properties-heat-flow--plane-front-solidification)
- [D7. Detached Bridgman and Semiconductor Crystal Quality](#d7-detached-bridgman-and-semiconductor-crystal-quality)
- [D8. Gas Porosity, Bubble Behaviour & Additive Manufacturing Bridge](#d8-gas-porosity-bubble-behaviour--additive-manufacturing-bridge)
- [D9. Processing-Structure-Property & Mechanical Data](#d9-processing-structure-property--mechanical-data)
- [10. Cross-Domain Variable Groups](#10-cross-domain-variable-groups)
- [11. Literature Gap Analysis](#11-literature-gap-analysis)

## D1. Alloy Systems & Solidification Processing Routes

Flemings alignment: Processing routes, Ch.1 heat and solute conservation.

ISS-EML is the central processing route for containerless metallic-alloy rapid solidification in the current corpus. The review frames space levitation as a benchmark environment for alloy thermodynamics, nucleation and growth, heat and mass transfer, interface dynamics, microstructure evolution, and defect formation. The Al-Si and Al-Cu comparison gives the wiki a recent metallic-alloy benchmark in which the same study contrasts gravity and microgravity directional solidification.

### Key Findings

- Containerless ISS-EML experiments decouple crucible interaction from melt processing and support controlled-convection studies. (10.1038/s41526-023-00310-2)
- The rapid-solidification program explicitly links space experiments to model validation for industrial casting, atomization, welding, and additive manufacturing. (10.1038/s41526-023-00310-2)
- Dendrite arm spacing, eutectic content, grain size, and compositional distribution differ between gravity and microgravity. (10.1038/s41526-024-00454-9)
- The sign and density of the segregating solute affect how gravity changes the directional-solidification outcome. (10.1038/s41526-024-00454-9)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 2 traceable non-example sources found; minimum is 15.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Multiple metallic alloy classes | ISS | ISS-EML | qualitative | review | solidification_technique=electromagnetic levitation; containerless rapid solidification; platform_class=long-duration orbital microgravity | 10.1038/s41526-023-00310-2 | review_source_no_single_alloy_table; missing_target_fields:alloy_system,cooling_rate_K_per_s,G_K_per_m,V_um_per_s,G_over_V,sample_geometry,microgravity_duration,experiment_year,mission |
| Al-Si; Al-Cu | Drop tube | 50-m-high drop tube | qualitative | experiment | drop_tube_height_m=50; solidification_technique=directional solidification | 10.1038/s41526-024-00454-9 | requires_table_extraction_for_DAS_and_composition_profiles; missing_target_fields:alloy_system,cooling_rate_K_per_s,G_K_per_m,V_um_per_s,G_over_V,sample_geometry,microgravity_duration,experiment_year,mission |

### Theory Alignment

- Maps to Flemings heat/solute conservation and growth-kinetics chapters because ISS-EML is used to isolate thermal, solutal, and flow terms that are otherwise coupled by gravity.
- Directly supports Flemings-style coupling between solute redistribution, density gradients, thermosolutal convection, and dendritic morphology.

### Citations

- Matson, D. M., Battezzati, L., Galenko, P. K., et al. (2023). Electromagnetic levitation containerless processing of metallic materials in microgravity: rapid solidification. npj Microgravity, 9, 65. https://doi.org/10.1038/s41526-023-00310-2
- Zhang, G., Luo, X., Li, Y., et al. (2024). Comparative study of gravity effects in directional solidification of Al-3.5 wt.% Si and Al-10 wt.% Cu alloys. npj Microgravity, 10, 114. https://doi.org/10.1038/s41526-024-00454-9

## D2. Fluid Flow, Convection, and Macrosegregation

Flemings alignment: Ch.1 heat and solute conservation, Ch.7 macrosegregation theory.

For flow and macrosegregation, this paper is important because it treats gravity effects as solute-dependent rather than as a simple on/off convection switch.

### Key Findings

- Thermosolutal convection arises from temperature and concentration gradients in the melt under ground gravity. (10.1038/s41526-024-00454-9)
- Gravity effects differed between Al-Si and Al-Cu because Si and Cu have different density and redistribution behavior in aluminum. (10.1038/s41526-024-00454-9)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 1 traceable non-example sources found; minimum is 12.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Al-Si; Al-Cu | Drop tube | 50-m-high drop tube | qualitative | experiment | drop_tube_height_m=50 | 10.1038/s41526-024-00454-9 | macrosegregation_profile_values_need_manual_table_extraction; missing_target_fields:segregation_coefficient_k,macrosegregation_index,convection_velocity_m_per_s,Ma,Ra,Gr |

### Theory Alignment

- Supports Flemings Ch.7 macrosegregation framing: convection changes solute transport, but the direction of the effect depends on alloy thermodynamics and density contrast.

### Citations

- Zhang, G., Luo, X., Li, Y., et al. (2024). Comparative study of gravity effects in directional solidification of Al-3.5 wt.% Si and Al-10 wt.% Cu alloys. npj Microgravity, 10, 114. https://doi.org/10.1038/s41526-024-00454-9

## D3. Dendritic and Cellular Solidification

Flemings alignment: Ch.3 dendrite spacing, Ch.5 growth kinetics.

The Glicksman microgravity dendrite experiment remains a foundational benchmark for diffusion-controlled dendritic growth because it measured tip velocity without normal buoyancy-driven convection. This paper converts ISS dendrite observations into a validation case for numerical models, making it useful for the wiki's benchmark and model-validation thread. The ISS CETSOL Al-Cu experiments are direct metallic benchmarks for columnar and equiaxed dendritic growth under diffusive conditions.

### Key Findings

- Microgravity dendrite velocity data agreed with Ivantsov-type diffusion analysis over the reported undercooling range. (10.1103/PhysRevLett.73.573)
- Ground convection can perturb dendrite kinetics even at modest undercooling. (10.1103/PhysRevLett.73.573)
- ISS microgravity remelting and directional solidification produced constrained diffusive dendritic growth. (10.1016/j.actaastro.2020.05.059)
- Cellular automata and phase-field simulations were compared against measured dendrite tip velocity. (10.1016/j.actaastro.2020.05.059)
- Grain-refined Al-Cu samples were directionally solidified on the ISS to study columnar growth, equiaxed growth, and the columnar-to-equiaxed transition. (10.1016/j.mtla.2024.102171)
- The experiment reports thermal characterization at liquidus, solidus, and eutectic front positions. (10.1016/j.mtla.2024.102171)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 3 traceable non-example sources found; minimum is 15.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Succinonitrile model alloy | Space Shuttle Columbia |  | quantitative_partial | benchmark | undercooling_min_K=0.05; undercooling_max_K=1.5 | 10.1103/PhysRevLett.73.573 | transparent_analog_not_metal_alloy; missing_target_fields:lambda1_um,lambda2_um,dendrite_tip_radius_um,dendrite_tip_velocity_um_per_s,undercooling_K |
| Succinonitrile-water model alloy | ISS | PFMI | qualitative | benchmark | model_comparison=cellular automata and phase-field | 10.1016/j.actaastro.2020.05.059 | transparent_analog_not_metal_alloy; tip_velocity_values_need_table_extraction; missing_target_fields:lambda1_um,lambda2_um,dendrite_tip_radius_um,dendrite_tip_velocity_um_per_s,undercooling_K |
| Al-Cu | ISS | ESA gradient furnace | qualitative | benchmark | solidification_technique=directional solidification; composition_count=3 | 10.1016/j.mtla.2024.102171 | G_V_cooling_rate_values_need_table_extraction; missing_target_fields:lambda1_um,lambda2_um,dendrite_tip_radius_um,dendrite_tip_velocity_um_per_s,undercooling_K |

### Theory Alignment

- Anchors Flemings growth-kinetics discussion in the Ivantsov diffusion solution and dendrite tip selection.
- Connects Flemings dendrite-growth theory to modern phase-field and cellular-automata validation.
- Feeds the Flemings CET discussion by linking G, V, cooling rate, and grain structure in a metallic alloy.

### Citations

- CETSOL team. (2024). Structures in grain-refined directionally solidified hypoeutectic Al-Cu alloys: Benchmark experiments under microgravity on-board the International Space Station. Materialia. https://doi.org/10.1016/j.mtla.2024.102171
- Glicksman, M. E., Koss, M. B., & Winsa, E. A. (1994). Dendritic growth velocities in microgravity. Physical Review Letters, 73, 573-576. https://doi.org/10.1103/PhysRevLett.73.573
- Kao, A., Pericleous, K., Shevchenko, N., et al. (2020). Dendritic solidification of Succinonitrile-0.24 wt% water alloy: A comparison with microgravity experiments for validating dendrite tip velocity. Acta Astronautica, 175, 163-173. https://doi.org/10.1016/j.actaastro.2020.05.059

## D4. Eutectic, Peritectic, Polyphase & Immiscible Systems

Flemings alignment: Ch.4 eutectic growth, Ch.6 polyphase reactions.

The Tiangong 2 Al-Bi-Sn study is a modern immiscible-alloy case where microgravity was used to suppress buoyancy-driven phase separation and produce a more dispersed structure. The Al-Pb drop-shaft study provides a useful quantitative benchmark because the reported microgravity sample had a lower cooling rate but a more homogeneous lead-particle distribution than the normal-gravity sample.

### Key Findings

- Directional solidification under microgravity produced a well-dispersed microstructure. (10.1038/s41526-019-0086-z)
- The reported sample matrix showed equiaxed morphology and no visible gas cavity or pinhole. (10.1038/s41526-019-0086-z)
- The normal-gravity sample showed sedimentation of large lead-rich particles at the sample bottom. (10.1016/j.matlet.2004.03.027)
- The microgravity sample showed comparatively homogeneous lead-particle distribution despite the lower cooling rate. (10.1016/j.matlet.2004.03.027)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 2 traceable non-example sources found; minimum is 12.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Al-Bi-Sn | Tiangong 2 |  | qualitative | experiment | phase_type=immiscible; visible_gas_cavity_observed=False | 10.1038/s41526-019-0086-z | droplet_size_distribution_needs_manual_extraction; missing_target_fields:lamellar_spacing_um,phase_morphology,droplet_size_um,coarsening_rate_um3_per_s |
| Al-Pb | Drop shaft | 1000-m drop shaft | quantitative_partial | experiment | phase_type=monotectic; cooling_rate_K_per_s_1g=130; cooling_rate_K_per_s_microgravity=70 | 10.1016/j.matlet.2004.03.027 | particle_size_distribution_needs_manual_extraction; missing_target_fields:lamellar_spacing_um,phase_morphology,droplet_size_um,coarsening_rate_um3_per_s |

### Theory Alignment

- Aligns with Flemings multiphase-solidification chapters by isolating liquid-liquid decomposition, droplet migration, and final phase morphology from sedimentation.
- Supports the distinction between thermal history and density-driven phase segregation in monotectic alloys.

### Citations

- Jiang, H., Li, S., Zhang, L., et al. (2019). Effect of microgravity on the solidification of aluminum-bismuth-tin immiscible alloys. npj Microgravity, 5, 26. https://doi.org/10.1038/s41526-019-0086-z
- Yasuda, H., Ohnaka, I., Kawasaki, K., et al. (2004). Solidification of hyper-monotectic Al-Pb alloy under microgravity using a 1000-m drop shaft. Materials Letters, 58, 2548-2552. https://doi.org/10.1016/j.matlet.2004.03.027

## D5. Nucleation, Undercooling, and Interface Kinetics

Flemings alignment: Ch.9 nucleation, Ch.9 interface kinetics.

The Al-Ni ISS-EML work is a focused interface-kinetics case where recalescence velocity does not monotonically increase with undercooling over part of the accessible range. For nucleation and undercooling, the rapid-solidification review ties ISS-EML experiments to phase selection, metastable phases, and convection-controlled nucleation.

### Key Findings

- Al-Ni alloys processed on the ISS showed anomalous velocity-undercooling behavior. (10.1007/s12217-021-09911-6)
- The paper models recalescence velocity trends measured in electromagnetically levitated samples. (10.1007/s12217-021-09911-6)
- ISS-EML supports studies of the influence of convection on nucleation and metastable phase selection. (10.1038/s41526-023-00310-2)
- The facility enables different stirring conditions by decoupling heating and positioning fields. (10.1038/s41526-023-00310-2)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 2 traceable non-example sources found; minimum is 12.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Al-Ni | ISS | ISS-EML | qualitative | model | solidification_technique=electromagnetic levitation; model_comparison=velocity-undercooling model | 10.1007/s12217-021-09911-6 | velocity_undercooling_curve_requires_digitization; missing_target_fields:maximum_undercooling_K,nucleation_temperature_K,nucleation_mechanism,nucleation_rate_m3_s,interface_velocity_m_per_s |
| Metallic glasses; Al-based alloys; Fe-Cr-Ni steels | ISS | ISS-EML | qualitative | review | solidification_technique=containerless undercooling | 10.1038/s41526-023-00310-2 | program_review_requires_linked_primary_experiments; missing_target_fields:maximum_undercooling_K,nucleation_temperature_K,nucleation_mechanism,nucleation_rate_m3_s,interface_velocity_m_per_s |

### Theory Alignment

- Extends Flemings Ch.9 by showing that interface kinetics in undercooled alloy melts can require solute- and phase-selection-aware models.
- Supports classical and coupled-flux nucleation discussions where undercooling, viscosity, interfacial energy, and stirring enter the nucleation rate.

### Citations

- Matson, D. M., Battezzati, L., Galenko, P. K., et al. (2023). Electromagnetic levitation containerless processing of metallic materials in microgravity: rapid solidification. npj Microgravity, 9, 65. https://doi.org/10.1038/s41526-023-00310-2
- Mullis, A. M. (2021). A model for the anomalous velocity-undercooling behaviour of levitated Al-Ni alloys on-board the International Space Station. Microgravity Science and Technology, 33, 70. https://doi.org/10.1007/s12217-021-09911-6

## D6. Thermophysical Properties, Heat Flow & Plane-Front Solidification

Flemings alignment: Ch.1 heat flow, Ch.2 plane fronts, Ch.8 stability.

The thermophysical-property review supplies the property schema for liquid metallic melts: surface tension, viscosity, density, specific heat, thermal conductivity, emissivity, and electrical resistivity. This early EML paper establishes why undercooled metallic-melt properties were targeted for microgravity measurement before the ISS-EML era.

### Key Findings

- Microgravity reduces levitation-force-driven flow and improves droplet sphericity, which improves thermophysical-property measurement precision. (10.1038/s41526-023-00281-4)
- ISS duration enables equilibrium measurements such as AC calorimetry that are difficult in short-duration reduced-gravity platforms. (10.1038/s41526-023-00281-4)
- The proposed method obtains surface tension and viscosity from oscillation frequency and damping of levitated molten samples. (10.1016/0273-1177(91)90294-T)
- The target state is the undercooled melt, which is difficult to access by conventional techniques. (10.1016/0273-1177(91)90294-T)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 2 traceable non-example sources found; minimum is 12.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Multiple metallic melts | ISS | ISS-EML | qualitative | review | measurement_techniques=oscillating drop; optical/inductive density; AC calorimetry; sample_mass_g_typical=1.0 | 10.1038/s41526-023-00281-4 | individual_alloy_property_tables_need_primary_extraction; missing_target_fields:thermal_conductivity_W_mK,specific_heat_J_kgK,density_kg_m3,viscosity_mPa_s,surface_tension_N_m |
| Undercooled metallic melts | Microgravity platform proposed | Electromagnetic levitation | qualitative | technical_report | measured_properties=viscosity; surface tension | 10.1016/0273-1177(91)90294-T | proposal_or_short_paper_not_full_property_dataset; missing_target_fields:thermal_conductivity_W_mK,specific_heat_J_kgK,density_kg_m3,viscosity_mPa_s,surface_tension_N_m |

### Theory Alignment

- Supplies the material-property inputs needed for Flemings heat-flow, convection, stability, and dendrite-spacing models.
- Connects thermophysical measurement to nucleation and undercooled-melt solidification models.

### Citations

- Egry, I., Fecht, H.-J., & Hoyer, W. (1991). The measurement of thermophysical properties in microgravity using electromagnetic levitation. Advances in Space Research, 11, 263-266. https://doi.org/10.1016/0273-1177(91)90294-T
- Mohr, M., Dong, Y., Bracker, G. P., et al. (2023). Electromagnetic levitation containerless processing of metallic materials in microgravity: thermophysical properties. npj Microgravity, 9, 34. https://doi.org/10.1038/s41526-023-00281-4

## D7. Detached Bridgman and Semiconductor Crystal Quality

Flemings alignment: Ch.2 directional solidification, Ch.9 interface kinetics.

Detached Bridgman growth is included as a distinct domain because microgravity experiments revealed that crucible contact can be interrupted by a stable gap, reducing mechanical stress during cooling. The GeSi detached-growth paper provides a semiconductor crystal case where applied pressure differential is used to promote detached Bridgman growth.

### Key Findings

- Detached growth separates the crystal from the crucible wall by a gap on the order of 10-100 um. (10.1557/mrs2009.74)
- The method is relevant to lowering thermal and mechanical stress in semiconductor crystal growth. (10.1557/mrs2009.74)
- Pressure-difference control was used to reproducibly grow mostly detached GeSi crystals. (10.1016/S0022-0248(01)02199-6)
- The study connects detachment to hydrostatic-pressure balance and crucible geometry. (10.1016/S0022-0248(01)02199-6)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 2 traceable non-example sources found; minimum is 12.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Semiconductor crystals | Microgravity and ground Bridgman | Bridgman/VGF | quantitative_partial | review | gap_width_min_um=10; gap_width_max_um=100 | 10.1557/mrs2009.74 | crystal_quality_metrics_need_primary_experiment_records; missing_target_fields:growth_rate_mm_h,thermal_gradient_K_cm,gap_width_um,contact_angle_deg,etch_pit_density_cm2 |
| GeSi | Ground Bridgman with microgravity-relevant detachment control | Vertical Bridgman | quantitative_partial | experiment | x_min=0; x_max=0.12; crucible_material=pyrolytic boron nitride | 10.1016/S0022-0248(01)02199-6 | EPD_and_XRD_quality_values_need_full_text_extraction; missing_target_fields:growth_rate_mm_h,thermal_gradient_K_cm,gap_width_um,contact_angle_deg,etch_pit_density_cm2 |

### Theory Alignment

- Links Flemings plane-front and nucleation/interface concepts to capillarity, wetting, meniscus stability, and defect generation.
- Supports the meniscus and pressure-balance part of detached Bridgman theory.

### Citations

- Croll, A., & Volz, M. P. (2009). Detached Bridgman growth-A standard crystal growth method with a new twist. MRS Bulletin, 34, 245-250. https://doi.org/10.1557/mrs2009.74
- Volz, M. P., Croll, A., Szofran, F. R., et al. (2002). Bridgman growth of detached GeSi crystals. Journal of Crystal Growth, 237-239, 1844-1848. https://doi.org/10.1016/S0022-0248(01)02199-6

## D8. Gas Porosity, Bubble Behaviour & Additive Manufacturing Bridge

Flemings alignment: Ch.10 defects, Additive manufacturing bridge.

The Al-Bi-Sn paper contributes to the porosity domain because it explicitly reports the absence of visible gas cavities or pinholes in the returned microgravity sample. This AM bridge record supplies the pore-formation mechanism side of the D8 comparison: keyhole collapse traps gas during rapid melt-pool solidification. This paper gives quantitative bridge values for AM: LPBF operates at high laser power density, scan speeds of order 0.05-4 m/s, and cooling rates around 10^4-10^6 K/s.

### Key Findings

- No visible gas cavity or pinhole was reported in the Tiangong 2 microgravity sample. (10.1038/s41526-019-0086-z)
- The result separates droplet/phase-dispersion behavior from classic gas-porosity measurements. (10.1038/s41526-019-0086-z)
- In situ X-ray imaging showed pores forming when deep keyhole depressions rapidly form and collapse. (10.1038/s41467-019-10009-2)
- The paper links laser scan transients to trapped gas pores and liquid-solid interface dynamics. (10.1038/s41467-019-10009-2)
- Keyhole porosity can initiate in transition as well as unstable keyhole regimes. (10.1038/s41467-022-28694-x)
- Keyhole fluctuations were reported at 2.5-10 kHz under high power-velocity conditions. (10.1038/s41467-022-28694-x)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 3 traceable non-example sources found; minimum is 20.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Al-Bi-Sn | Tiangong 2 |  | qualitative | experiment | visible_gas_cavity_observed=False | 10.1038/s41526-019-0086-z | pore_size_distribution_not_reported_in_seed_record; missing_target_fields:pore_volume_fraction_pct,mean_pore_diameter_um,bubble_rise_velocity_m_per_s,AM_process,pore_type |
| Metal LPBF alloys | Ground synchrotron experiment | In situ X-ray imaging | qualitative | experiment | AM_process=LPBF; pore_type=keyhole; solidification_context=rapid laser melt pool | 10.1038/s41467-019-10009-2 | not_microgravity; AM_bridge_record; missing_target_fields:pore_volume_fraction_pct,mean_pore_diameter_um,bubble_rise_velocity_m_per_s |
| Metal LPBF alloys | Ground synchrotron experiment | In situ X-ray imaging | quantitative_partial | experiment | AM_process=LPBF; pore_type=keyhole; keyhole_fluctuation_min_kHz=2.5; keyhole_fluctuation_max_kHz=10.0; laser_power_min_W=100; laser_power_max_W=1000; scan_speed_min_m_per_s=0.05; scan_speed_max_m_per_s=4.0; cooling_rate_min_K_per_s=10000; cooling_rate_max_K_per_s=1000000 | 10.1038/s41467-022-28694-x | not_microgravity; AM_bridge_record; missing_target_fields:pore_volume_fraction_pct,mean_pore_diameter_um,bubble_rise_velocity_m_per_s |

### Theory Alignment

- Relevant to Flemings defect discussions, but the paper is stronger for immiscible phase morphology than for quantitative gas-pore kinetics.
- Provides a high-cooling-rate defect analogue for Flemings Ch.10, while gravity is secondary to recoil pressure, capillarity, vaporization, and rapid solidification.
- Useful for comparing gravity-suppressed casting flows with rapid-solidification AM where vapor recoil, surface tension, and short timescale dominate.

### Citations

- Huang, Y., Fleming, T. G., Clark, S. J., et al. (2022). Keyhole fluctuation and pore formation mechanisms during laser powder bed fusion additive manufacturing. Nature Communications, 13, 1170. https://doi.org/10.1038/s41467-022-28694-x
- Jiang, H., Li, S., Zhang, L., et al. (2019). Effect of microgravity on the solidification of aluminum-bismuth-tin immiscible alloys. npj Microgravity, 5, 26. https://doi.org/10.1038/s41526-019-0086-z
- Martin, A. A., Calta, N. P., Khairallah, S. A., et al. (2019). Dynamics of pore formation during laser powder bed fusion additive manufacturing. Nature Communications, 10, 1987. https://doi.org/10.1038/s41467-019-10009-2

## D9. Processing-Structure-Property & Mechanical Data

Flemings alignment: Ch.10 properties and defects.

The current seed corpus confirms a persistent processing-structure-property gap: microgravity work is rich in process physics and microstructure, but mechanical property datasets on returned microgravity-solidified specimens are sparse in the seeded sources.

### Key Findings

- ISS-EML review connects process control and microstructure to downstream mechanical-property optimization, but it is not itself a mechanical test dataset. (10.1038/s41526-023-00310-2)
- The highest-priority D9 task is to pair returned-specimen microstructure with tensile, hardness, fatigue, or creep data. (10.1038/s41526-023-00310-2)

The table below lists traceable records currently ingested for this domain. The system flags the section for retry when the source count is below the configured threshold.

QA flags: Only 1 traceable non-example sources found; minimum is 12.

| alloy | platform | facility | status | evidence | variables | citation | gaps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Multiple metallic alloy classes | ISS | ISS-EML | qualitative | review |  | 10.1038/s41526-023-00310-2 | mechanical_property_data_absent; needs_returned_specimen_property_sources; missing_target_fields:grain_size_um,yield_strength_MPa,UTS_MPa,elongation_pct,hardness,fatigue_limit_MPa |

### Theory Alignment

- Maps to Flemings Ch.10 by identifying the missing final link from process variables and defects to mechanical response.

### Citations

- Matson, D. M., Battezzati, L., Galenko, P. K., et al. (2023). Electromagnetic levitation containerless processing of metallic materials in microgravity: rapid solidification. npj Microgravity, 9, 65. https://doi.org/10.1038/s41526-023-00310-2

## 10. Cross-Domain Variable Groups

The analysis agent groups extracted values into process, material, microstructure, thermophysical, mechanical, and dimensionless-number categories. Empty rows indicate that no validated quantitative value has been ingested yet.
### A_Process Variables

No validated rows yet.

### B_Material Variables

No validated rows yet.

### C_Microstructure Variables

No validated rows yet.

### D_Thermophysical Variables

No validated rows yet.

### E_Mechanical Variables

No validated rows yet.

### F_Dimensionless Numbers

No validated rows yet.

## 11. Literature Gap Analysis

Pipeline status: `human_review_required`. Domains requiring expanded search or human curation: D1, D2, D3, D4, D5, D6, D7, D8, D9.
