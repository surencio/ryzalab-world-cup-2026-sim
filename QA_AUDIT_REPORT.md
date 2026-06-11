# Validation & Verification Audit — Dixon-Coles WC2026 Simulator

**Auditor:** Claude (Lead QA / Senior Sports Statistician role)
**Date:** 2026-06-11
**Method:** Every quantitative claim was tested by executing the actual code via a
purpose-built harness (`/tmp/qa_world_cup/qa_audit2.py`) — including causal
decomposition runs (40k sims) that isolate each claimed effect. Roster and fixture
facts verified against June 2026 news.

---

## 1. Audited Suitability — Verdicts

| Area | Verdict | Summary |
| :--- | :---: | :--- |
| Dixon-Coles math | **PASS** | τ(x,y) matches the canonical 1997 form; mass-preserving; λ identities exact |
| Elo→(λ,μ) mapping | **PASS** | λ+μ=2.5 exact; λ/μ=10^(d/400) to 1e-14 |
| Grid normalization | **PASS w/ caveat** | Pre-normalization total is 0.99981 (Poisson truncation at 9 goals), not machine precision; division by `total` makes the sampled PMF exact |
| Stochastic roster sampling | **PASS (mechanics)** | All 12 team×round hazards within 0.6pp of spec over 100k draws; penalty/reset exact |
| Fixture-round alignment | **FAIL** | Groups B and L hazards land on the wrong real-world opponents (see DC-1) |
| Tie-breaker hierarchy | **PASS** | Points→GD→GS→Elo verified by unit test; shuffle-before-stable-sort gives uniform 25.0±0.6% on absolute ties; old QA-1 bias regression-tested (Morocco/Brazil gap now 0.3pp) |
| Simulation statistics | **PASS** | Sampler empirical PMF matches analytic grid to 0.1% over 300k draws |
| Shift-claim attribution | **FAIL (2 of 4)** | Brazil claim causally verified; Canada and Netherlands attributions are wrong (DC-2, DC-3); claim #4 numbers wrong (DC-4) |

---

## 2. Suite 1 — Mathematical Integrity: PASS

- **λ+μ = 2.5** exactly and **λ/μ = 10^((R_A−R_B)/400)** to 1.4e-14 across d = 0…800. ✓
- **τ adjustments** for (0,0), (1,0), (0,1), (1,1) match Dixon-Coles (1997):
  τ₀₀ = 1−λμρ, τ₁₀ = 1+μρ, τ₀₁ = 1+λρ, τ₁₁ = 1−ρ. Verified the DC adjustment is
  *analytically mass-preserving* (sum of deltas = −1.7e-18). ✓
- **No negative cell probabilities:** worst-case factor is 1−0.08·2.5 = 0.80 > 0. ✓
- **Grid total before sampling:** 0.9998108821 at the most lopsided real matchup
  (Spain–Cape Verde, λ=2.38). The 1.9e-04 deficit is purely P(≥10 goals) truncation —
  *not* machine precision as the checklist requested, but the code renormalizes before
  sampling so the sampled distribution is exactly proper. Extend the grid to 13×13 if
  literal machine-precision pre-normalization is required.
- **Sampler fidelity:** 300k draws at (λ=1.5, μ=1.0) match the analytic grid within
  0.10% on every score cell. ✓
- **ρ direction check:** at equal strength (λ=μ=1.25), draw probability is 0.2700
  (independent Poisson) → **0.2906** (DC, ρ=−0.08), vs 0.2497 in the old trinomial
  model. ρ<0 *raises* low-score draw mass — the documented purpose of DC. See DC-4/DC-5:
  the predictions report describes this backwards, and 29.1% is high vs. the ~25–26%
  empirical draw rate for evenly matched international sides (literature ρ ≈ −0.03…−0.05).

---

## 3. Suite 2 — Stochastic Roster Sampling: mechanics PASS, schedule FAIL

100k-draw verification per team per round — all within 0.6pp of spec, exactly two Elo
levels observed, baseline restored when the player plays:

| Team | Player | Hazard spec [R1,R2,R3] | Observed | Elo (out / in) |
| :--- | :--- | :--- | :--- | :--- |
| Brazil | Neymar | 15% / 50% / 75% | 15.1 / 49.8 / 74.9 | 1920 / 1980 ✓ |
| Canada | Davies | 40% / 75% / 90% | 40.0 / 74.9 / 90.0 | 1850 / 1880 ✓ |
| England | Saka | 70% / 90% / 95% | 69.8 / 90.2 / 95.0 | 2040 / 2050 ✓ |
| Ghana | Kudus | 10% / 40% / 85% | 10.0 / 40.0 / 84.9 | 1670 / 1710 ✓ |

Expected effective Elo per round (confirms the intended "recovery curve"):
Brazil 1929→1950→1965; Canada 1862→1872.5→1877; England 2047→2049→2049.5; Ghana 1674→1686→1704.

### 🔴 DEFECT DC-1 (High): Round indices don't match the real FIFA schedule in Groups B & L

The pairing template (R1: 0-1, 2-3; R2: 0-2, 1-3; R3: 0-3, 1-2) over dict order
matches reality only by coincidence:

| Group | Code schedule | Real schedule (verified) | Hazard impact |
| :--- | :--- | :--- | :--- |
| C ✓ | R1 BRA-MAR, R2 BRA-HAI, R3 BRA-SCO | identical (Jun 13/19/24) | Neymar hazards correctly placed |
| B ✗ | R1 **CAN-SUI**, R2 CAN-QAT, R3 **CAN-BIH** | R1 **CAN-BIH** (Jun 12), R2 CAN-QAT (Jun 18), R3 **CAN-SUI** | R1/R3 reversed: Davies simulated at 40% vs Switzerland (really his 90% match) and 90% vs Bosnia (really 40%) |
| L ✗ | R2 **ENG-PAN / CRO-GHA**, R3 **ENG-GHA / CRO-PAN** | R2 **ENG-GHA** (Jun 23) / PAN-CRO, R3 PAN-ENG / **CRO-GHA** (Jun 27) | R2/R3 swapped: Kudus simulated at 85% vs England (really his 40% match, Jun 23) and 40% vs Croatia (really 85%) |

With round-dependent hazards, fixture order is now load-bearing. Canada's hardest
match is mis-simulated with their *weakest* expected lineup (−15 effective Elo vs
Switzerland), slightly understating Canada's P(1st); Ghana's competitiveness against
England/Croatia is allocated to the wrong opponents. Fix: encode the actual fixture
list per group instead of the index template.

### 🟡 DEFECT DC-6 (Low/Medium): Availability re-sampled independently across rounds

Injury recovery is a persistent state, but each round draws independently: trajectories
like "Neymar plays R1, out R2" occur with probability 7.5% per run despite being
medically implausible. Means are unaffected (match outcomes depend only on per-match
marginals here), but within-run strength correlation — hence the spread of Brazil's
total-points distribution — is understated. Fix: draw one uniform `u` per team per
tournament run; player is available in round r iff `u ≤ probs[r]` (monotone recovery
coupling). One line, no change to marginals.

---

## 4. Suite 3 — Tie-Breaking Logic: PASS

- **Hierarchy unit tests** on the exact sort key: points dominates; GD breaks points
  ties; GS breaks points+GD ties; Elo breaks points+GD+GS ties. All pass.
- **Full-tie fairness:** 20k sorts of four fully tied teams → P(1st) = [24.6%, 24.9%,
  25.0%, 25.5%] (uniform ✓). End-to-end, four identical 1800-Elo teams through
  `simulate_group` (40k sims) → [25.0%, 24.9%, 25.1%, 25.0%] ✓. The shuffle-before-
  stable-sort pattern is correctly implemented.
- **Old QA-1 regression test:** with Neymar forced out (both teams flat 1920),
  Morocco 46.7% vs Brazil 46.4% — the 17.2pp insertion-order bias from the previous
  model is gone. ✓
- 🟢 **Note (DC-7):** the 4th key reads `group_teams[t][1]`, which still holds *old*
  adjusted Elos for stochastic teams (Ghana 1690, England 2040) while matches are
  played at 1710/2050. Only matters for exact points+GD+GS ties (e.g., Ghana vs Panama,
  1690 vs 1710 — deterministically favors Panama). Also note Elo is not an official
  FIFA criterion (FIFA: head-to-head among tied teams, then fair-play points, then
  drawing of lots); Elo-then-random is a reasonable documented approximation, but the
  checklist's description of it as "official FIFA criteria" is slightly overstated.

---

## 5. Suite 4 — Probability Shift Validation: numbers verified, two attributions FALSIFIED

All four headline numbers transcribe correctly from `comparison_results.json`
(Brazil 46.6%→50.7%, Morocco 46.4%→43.7%, Canada 33.2%→37.7%, Netherlands 48.8%→44.7%),
and all 48 table rows in `predictions.md` match the JSON under round-half-up rounding.
But transcription ≠ causation, so each claimed *mechanism* was tested by intervention:

### ✅ Claim #1 (Brazil/Neymar): VERIFIED
Old baseline (flat 1920) equals new model with Neymar always out (1980−60=1920) — a
clean isolation. Forcing Neymar out in the new engine: Brazil P(1st) = 46.8%;
stochastic recovery curve: 50.8% (**+3.9pp**, matching the claimed +4%). The rise is
genuinely the Neymar availability curve. Statistically logical. ✓

### 🔴 Claim #2 (Canada/Davies): FALSIFIED (DC-2)
The comparison's "old" run silently used Canada at **flat 1880** — not the published
old model's 1850. Since stochastic Davies can only *subtract* from 1880, his hazard
**lowers** Canada, it cannot explain a rise. Intervention runs (40k sims, new engine):
Davies stochastic **37.0%**, Davies always available **39.9%**, always out **32.7%**.
The 33%→38% improvement is an artifact of comparing against a re-rated baseline; the
true driver is the engine change (goal simulation + GD/GS tie-breaks replacing the
deterministic Elo tie-break). Note the same silent re-rating affects the "old" columns
for Netherlands (1885), England (2040 tie-break), and Ghana (1690) — the comparison's
"old" is *neither* the published old model nor a pure engine A/B.

### 🟡 Claim #3 (Netherlands/Timber): numbers right, attribution wrong (DC-3)
Both "old" and "new" comparison runs already include Timber (1885). The 49%→45% step
the report attributes to "incorporating Timber's groin injury" is therefore purely the
engine change. Timber's actual effect was the 57.2%→48.8% drop *inside* the old
engine (1920→1885). Sweden/Japan do rise as claimed, for the right qualitative reason
but at the wrong step.

### 🔴 Claim #4 (avg-points drop "0.2–0.3"): FALSIFIED twice (DC-4)
Measured group-total drops: **0.37–0.45 points (mean 0.42)** — 0 of 12 groups fall in
the claimed 0.2–0.3 band. And the stated mechanism is backwards: the report says DC
"corrects for draw inflation," but ρ=−0.08 *increases* draw probability (24.97% →
29.06% at equal strength); the points drop exists precisely because there are *more*
draws. Related calibration concern (DC-5): 29.1% equal-strength draws is above the
~25–26% empirical rate, and |ρ|=0.08 is ~2× the typical fitted DC magnitude. Consider
ρ ≈ −0.04, or fit ρ to recent international data.

---

## 6. Roster Quality Check (web-verified, June 11, 2026)

| Player | Model treatment | Reality | Verdict |
| :--- | :--- | :--- | :---: |
| Neymar (BRA) | Stochastic 15/50/75%, −60 | Calf, ~3 weeks from May 28 ⇒ doubtful Jun 13, likely later rounds | ✅ well-calibrated |
| Rodrygo/Militão/Estêvão (BRA) | −40 permanent (base 1980) | All ruled out | ✅ (−40 for three starters is arguably light vs the skill's tiers) |
| Simons (NED) | −50 permanent | ACL, out | ✅ |
| De Ligt (NED) | −10 permanent | Back surgery, out | ✅ |
| Timber (NED) | −35 permanent (now included) | Groin, out | ✅ addresses prior QA-4 |
| Gnabry/ter Stegen (GER) | −35 (unchanged) | Out / not selected | ✅ |
| Mitoma (JPN) | −60 (unchanged) | Left off squad | ✅ |
| Saka (ENG) | Stochastic 70/90/95%, −10 | In squad, "not 100%" per Tuchel (Achilles, managed) | ✅ appropriate |
| Kudus (GHA) | Stochastic 10/40/85%, −40 | Major doubt, possible return ~Jun 18; Ghana plays Jun 17/23/27 | ✅ good fit — but the 40% R2 leg lands on the wrong opponent (DC-1) |
| Davies (CAN) | Stochastic 40/75/90%, −30 | Says he may make Jun 12 opener | ✅ hazard shape fine; ⚠️ prior QA-3 double-count stands (his absence is already in Canada's 1780 base), and rounds are reversed (DC-1) |

---

## 7. Monte Carlo Noise Audit

- At p = 0.50, 10,000 runs give SE = 0.50pp ⇒ 95% CI **±0.98pp** — it *just* meets the
  ±1% requirement for a single estimate, and is comfortably inside it for tail
  probabilities (±0.85pp at p=0.25, ±0.43pp at p=0.05).
- **But shift estimates don't meet it:** new−old differences from two independent 10k
  runs carry 95% CI up to **±1.39pp**. **30 of the 48** `shift_1st` values in
  `comparison_results.json` are inside that band, i.e. indistinguishable from zero —
  yet are reported with 4-decimal precision.
- Verdict: 10k is sufficient for the headline tables (whole-% rounding ✓, a good fix
  from the last audit), **insufficient for the old-vs-new shift analysis**. Use ≥100k
  runs for comparisons (CI ±0.31pp). Runtime makes this practical only after
  memoizing the score grid: the engine rebuilds the 100-cell DC grid for every match
  of every sim (~7.2M rebuilds, ~24s observed); each group has only a handful of
  distinct (λ_A, λ_B) pairs, so caching cuts this to seconds. Seed is set (42) ✓ —
  results are now bit-reproducible.

---

## 8. Recommendations (priority order)

1. **DC-1:** Replace the index-based pairing template with the actual FIFA fixture
   list per group (Group B: CAN-BIH, QAT-SUI / SUI-BIH, CAN-QAT / SUI-CAN, QAT-BIH;
   Group L: ENG-CRO, GHA-PAN / ENG-GHA, PAN-CRO / PAN-ENG, CRO-GHA). Re-run.
2. **DC-2/DC-3:** Rewrite Key Findings #2 and #3. Honest decomposition: report the
   rating change (old engine, old vs new ratings) and the engine change (new ratings,
   old vs new engine) as separate steps. The current "old" baseline is a hybrid that
   supports neither narrative.
3. **DC-4/DC-5:** Correct Key Finding #4 (drop is 0.37–0.45, mechanism is *more*
   draws), and recalibrate ρ toward −0.03…−0.05 (29% equal-strength draws is too high).
4. **DC-6:** Couple availability across rounds with a single uniform per run.
5. Memoize DC grids; raise comparison runs to ≥100k; only report shifts > ±1.4pp
   (10k) or ±0.5pp (100k) as findings.
6. **DC-7:** Point the tie-break Elo at the same rating used for match play.
7. Update the two skill files — they are byte-identical to the pre-upgrade versions
   and document neither the DC model, the Elo→λ mapping, ρ, nor hazard sampling.
   `predictions.md` is currently the only methodology record.

**Bottom line:** the Dixon-Coles core is mathematically correct and well-implemented,
the tie-break fairness defect from the previous audit is verifiably fixed, and the
Brazil/Neymar headline finding survives causal testing. The release blockers are the
fixture-round misalignment (Groups B and L simulate key players' availability against
the wrong opponents) and the two falsified attribution claims in the report, which
rest on a silently re-rated baseline.
