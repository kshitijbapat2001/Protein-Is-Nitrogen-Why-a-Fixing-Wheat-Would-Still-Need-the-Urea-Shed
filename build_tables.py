"""Tables 1-2. Run: python3 build_tables.py"""

from __future__ import annotations

import csv
import os
import re

OUTDIR = "../tables"

SOURCES = (
    "Angus et al. (2015) Crop Pasture Sci 66:523-552; "
    "Giordano et al. (2023) Field Crops Res 290:108740; "
    "Grain Trade Australia (2025) Wheat trading standards 2025/26; "
    "Ladha et al. (2016) Sci Rep 6:19355; "
    "Rogers & Oldroyd (2014) J Exp Bot 65:1939-1946; "
    "Shcherbak et al. (2014) PNAS 111:9199-9204; "
    "Veresoglou & Menexes (2010) Plant Soil 337:469-480"
)

N_TO_PROTEIN_FACTOR = 5.7
REFERENCE_YIELD_T_HA = 4.0
WHEAT_GRADES = [("APH2", 13.0), ("H2", 11.5), ("APW1", 10.5)]
TGT_LO = 25.0
TGT_HI = 50.0


def grain_n_removed(yield_t_ha, protein_pc):
    return yield_t_ha * 1000.0 * (protein_pc / 100.0) / N_TO_PROTEIN_FACTOR


APH2_N = grain_n_removed(REFERENCE_YIELD_T_HA, WHEAT_GRADES[0][1])

TABLE1_HEADER = ["Domain", "Stakeholder", "Quantified stake", "Position"]

TABLE1 = [
    ["Food", "Growers delivering milling grades",
     f"At {REFERENCE_YIELD_T_HA:.0f} t ha-1 an APH2 crop removes {APH2_N:.0f} kg "
     f"N ha-1 in grain; the {TGT_LO:.0f}-{TGT_HI:.0f} kg N ha-1 target covers "
     f"{TGT_LO / APH2_N * 100:.0f}-{TGT_HI / APH2_N * 100:.0f}% of it "
     "(Grain Trade Australia, 2025; Rogers & Oldroyd, 2014)",
     "Conditional; only if the grade stays reachable"],

    ["Food", "Bulk handlers and classifiers",
     "Grade is assigned on nitrogen x 5.7 at receival, so protein variability "
     "becomes blending and segregation cost (Grain Trade Australia, 2025)",
     "Resistant; bears a cost it does not cause"],

    ["Food", "Millers and export buyers",
     "HB4, the only approved transgenic wheat trait, is cleared in 10 countries "
     "but grown in 2 (ISAAA, 2025)",
     "Resistant; acceptance is separate from approval"],

    ["Food", "Smallholders on feed and domestic grades",
     "Fertiliser use in Africa averages about 22 kg ha-1 against 94 in Latin "
     "America and 177 in Asia, and feed grades carry no protein floor "
     "(Food and Agriculture Organization [FAO], 2024; Grain Trade "
     "Australia, 2025)",
     "Strongest demand; the natural first market"],

    ["Food", "Trait developers",
     "Bread wheat is a 17 Gb allohexaploid with 3 homoeologues per gene and "
     "1.5-51% transformation efficiency (IWGSC, 2018; Debernardi et al., "
     "2020)",
     "Cautious; wheat is the hardest cereal to engineer"],

    ["Fibre", "Grain legume growers",
     "Wheat yields 1.2 t ha-1 more after grain legumes and 0.5 t ha-1 more "
     "after oats, so 0.7 t ha-1 is the nitrogen component (Angus et al., "
     "2015)",
     "Opposed; the trait substitutes for half their value"],

    ["Fibre", "Straw and biomaterials processors",
     "Wheat straw has a C:N of 80-100:1 or higher, well above the 25:1 "
     "immobilisation threshold (García-Ruiz et al., 2019)",
     "Watchful; residue chemistry, not nitrogen, is their variable"],

    ["Fuel", "Ammonia manufacturers",
     "185 Mt NH3 produced annually, 98% from natural gas (Smith et al., 2020); "
     "wheat takes about 18% of manufactured reactive nitrogen (Ladha et "
     "al., 2016)",
     "Opposed; faces demand erosion, not a cost shock"],

    ["Fuel", "Climate and inventory agencies",
     "Inside wheat's 90-135 kg N ha-1 window, substitution abates 0.91-1.08 "
     "times the constant-factor estimate (Shcherbak et al., 2014)",
     "Conditional on measurement; no premium for wheat"],
]

TABLE2_HEADER = ["Action", "Go / no-go gate", "Expected consequence",
                 "Leading indicator"]

TABLE2 = [
    ["A1. Fund wheat transformation capability before funding a wheat fixation "
     "trait",
     "Genotype-independent transformation at or above 20% efficiency in three "
     "commercial cultivars by 2031 (IWGSC, 2018; Debernardi et al., 2020)",
     "Either wheat becomes able to carry the trait, or the budget moves to the "
     "microbial route with no further sunk cost",
     "Transformation efficiency reported per cultivar"],

    ["A2. Verify the microbial route in wheat independently, since it is the "
     "only route with wheat evidence",
     "A multi-site trial, not vendor-run, beating +8.9% grain yield and "
     "delivering 20 kg N ha-1 or more, with protein reported (Veresoglou & "
     "Menexes, 2010; Fox et al., 2016)",
     "A deployable 20-45 kg N ha-1 input this decade, or an early and cheap "
     "negative result",
     "Measured N delivered and delivered protein, independently run"],

    ["A3. Specify the trait as baseload nitrogen and keep the tactical "
     "late-season window",
     "Design must leave a late window able to move delivered protein by at "
     "least one grade step (Bogard et al., 2010; Giordano et al., 2023)",
     "Growers retain grade control, so the trait is adoptable rather than a "
     "price risk",
     "Share of adopters still reaching their target grade"],

    ["A4. Launch into feed and domestic grades first, with royalty-free "
     "licensing fixed at filing",
     "First release confined to grades with no protein floor, in countries "
     "applying under 25 kg N ha-1 (FAO, 2024; Grain Trade Australia, 2025)",
     "The envelope is sufficient on its own where it is deployed, and the "
     "benefit reaches growers who cannot pay for fertiliser",
     "Hectares adopted in no-floor grades, and licence terms at filing"],

    ["A5. Correct the accounting before any claim is made",
     "Rate-dependent N2O factors in Tier 2 inventories, no nonlinearity premium "
     "credited to wheat, and the break crop priced separately from nitrogen "
     "(Shcherbak et al., 2014; Angus et al., 2015)",
     "Abatement claims survive audit, and the 0.5 t ha-1 break value is not "
     "lost to a nitrogen-only appraisal",
     "Emission factor basis used, and legume area retained"],
]

_TYPESET = [
    ("N2O", "N₂O"),
    ("CO2e", "CO₂e"),
    ("CO2", "CO₂"),
    ("NH3", "NH₃"),
    ("ha-1", "ha⁻¹"),
    ("yr-1", "yr⁻¹"),
    (" x ", " × "),
]


def typeset(cell: str) -> str:
    out = cell
    for a, b in _TYPESET:
        out = out.replace(a, b)
    return re.sub(r"(?<=\d)-(?=\d)", "–", out)


def write_table(filename: str, header: list[str], rows: list[list[str]]) -> None:
    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow([typeset(h) for h in header])
        w.writerows([[typeset(c) for c in r] for r in rows])
    print(f"  wrote {path}  ({len(rows)} rows x {len(header)} columns)")


def main() -> None:
    write_table("Table1_stakeholder_perspectives.csv", TABLE1_HEADER, TABLE1)
    write_table("Table2_action_plan.csv", TABLE2_HEADER, TABLE2)


if __name__ == "__main__":
    main()
