---
name: sports-prediction
description: "Expert-level qualitative sports context quantification. Use when factoring in subjective data (injuries, squad rotations, coaching changes, player returns, and tactical matchups) and converting them into quantitative rating adjustments for international football predictions."
---

# Sports Prediction Context Quantification

Advanced framework for translating subjective football context into quantitative rating adjustments (Elo/SPI).

## Core Philosophy
Qualitative context (e.g., a star player's year-long injury or a manager transition) can make static ratings highly misleading. Predictions must adjust baseline ratings using structured, evidence-based formulas rather than subjective guesswork.

---

## Quantification Procedures

### 1. Star Player Injury & Stochastic Roster Modeling
Rather than using static Elo point deductions for players with questionable fitness or partial returns, model availability stochastically per match. 
1. Define a player's availability probability $P_{\text{avail}}$ per group match (Game 1, 2, and 3) based on clinical and training reports (e.g., Kudus returning in Game 3: $P = [0.10, 0.40, 0.85]$).
2. In each tournament simulation run, draw a single random uniform variable $u \sim \text{Uniform}(0, 1)$ for the team.
3. In match $r$ of the tournament (where $r \in \{0, 1, 2\}$), if $u > P_{\text{avail}}[r]$, apply the **Elo Penalty** ($\Delta R_p$) dynamically for that match. This monotonic coupling ensures that if a player recovers and becomes available in match $r$, they remain available for all subsequent matches (since $P_{\text{avail}}$ is non-decreasing).
   $$\Delta R_p = E_{\text{squad}} \times S_{xG+xA} \times (1 - D_{\text{depth}})$$
   Where:
   *   $E_{\text{squad}}$: Squad rating scale factor (base of $150$ Elo points).
   *   $S_{xG+xA}$: The player's share of team Expected Goals and Expected Assists over the last 10 competitive matches.
   *   $D_{\text{depth}}$: Backup quality factor ($0.0$ to $1.0$). $1.0$ means the backup is of equal quality (no penalty), $0.0$ means no competent backup exists.
   *   *Calibration Rule of Thumb*:
       - **Tier 1 Star (e.g., Neymar, Mbappe)**: Deduct $60$ to $80$ Elo points if no top-tier backup exists.
       - **Tier 2 Key Player (e.g., Starting Center-Back/Goalkeeper)**: Deduct $30$ to $40$ Elo points.


### 2. Under-Ranked Team Adjustments (Returns & Acclimation)
If a team's star player missed a year of qualification matches (causing the team to lose games and drop in ranking) but is now healthy and playing:
*   **Add $+40$ to $+70$ Elo points** back to the team rating to correct for the artificial deflation.
*   **Decay rate**: If the player has played fewer than 3 matches since returning, scale this correction by $50\%$ to account for match fitness.

### 3. Tactical Mismatch Modifiers
Adjust probabilities when tactical styles conflict:
*   **Low-Block Underdog vs. Possession Favorite**: If an underdog (rating difference $>200$ Elo) plays a heavy low-block (defensive width $<40$m, high defensive line absent) against a possession-heavy favorite:
    - Reduce the favorite's win probability by $8\%$ and increase the draw probability by $8\%$.
*   **High Altitude Matchups**: When playing at high altitude (e.g., Mexico City):
    - Teams with altitude-acclimated squads (e.g., Mexico, Ecuador, Bolivia) receive a $+50$ Elo boost against non-acclimated opponents.

### 4. Group Stage Game 3 Incentives (Motivation Modifier)
In tournament group stages, motivation is dynamic:
*   **Already Qualified (1st place locked)**: Deduct $60$ Elo points from the qualified team's rating in Game 3 due to expected squad rotation.
*   **Must Win vs. Eliminated**: If Team A must win to advance and Team B is already mathematically eliminated, add $+45$ Elo points of motivation to Team A.

### 5. Interfacing with Calibration Parameters
When applying qualitative Elo adjustments, they must pass through the calibrated forecasting parameters:
*   **Elo Damping ($s=0.58$)**: Note that any qualitative adjustment applied to the base rating is compressed by the $s=0.58$ damping factor when calculating match expectations. For example, a $-60$ Elo penalty for Neymar's injury behaves as an effective $-34.8$ Elo difference penalty.
*   **Variable Goals ($G(d)$)**: Rating adjustments alter the rating difference $d$, which dynamically increases the expected total goals $G(d) = 2.38364 + 0.0013636 \cdot |d|$.
*   **R32 Advancement**: When evaluating the final impacts of group stage adjustments (e.g. qualified rotation penalties), simulate the entire 12-group tournament jointly to correctly evaluate how these adjustments affect wild-card advancement for 3rd-place teams.

---

## Anti-Patterns to Avoid

*   **NEVER apply a blanket deduction for all injuries**: A backup goalkeeper of high quality nullifies a starting goalkeeper's injury. Always evaluate the drop-off to the backup ($D_{\text{depth}}$).
*   **NEVER double-count narrative factors**: If a team changes their manager, do not apply a penalty if the rating already reflects the poor results under the previous manager. Only adjust if the new manager brings a radical tactical shift.
*   **NEVER exceed a maximum adjustment of $\pm 100$ Elo points** for combined qualitative factors: Excess adjustments distort baseline statistical validity.

---

## Mindset & Thinking Framework

Before adjusting a match prediction, ask yourself:
1.  **Is this factor already priced in?** If a star player has been injured for 18 months, their absence is already reflected in the baseline Elo ratings of recent matches. Do NOT deduct points again.
2.  **What is the depth chart delta?** Who is the direct replacement, and what is their club level/minutes played?
3.  **What is the team's tournament incentive?** Does a draw satisfy both teams to advance? If yes (e.g., a "biscotto" scenario), double the baseline draw probability.

---

## Data Sourcing & Advanced Metric Benchmarking

To populate the parameters ($S_{xG+xA}$ and $D_{\text{depth}}$) of the injury/absence adjustment formula, query and benchmark against the following resources:
1. **Expected Goals (xG) and Expected Assists (xA) Share**:
   - Source from databases like **FBref** (powered by Opta) or **StatsBomb**.
   - Calculate $S_{xG+xA}$ as: $\text{Player's } (xG + xA) \text{ per } 90 \text{ minutes} \times \text{Expected Minutes Share}$.
2. **Squad Depth Quality ($D_{\text{depth}}$)**:
   - Extract squad value datasets from **Transfermarkt** or use Kaggle databases from discontinued forecasting models (e.g., FiveThirtyEight's final SPI dataset) to compute the ratio of the backup player's club-level SPI to the injured player's club-level SPI.
3. **Open-Source Tooling**:
   - `openclaw/skills` (specifically `sports-arbitrage` modules): Details API connectors to odds comparison websites for real-time market expectation changes.
   - `Cortex-Trading-Systems/polymarket-copy-trading-bot-clob-ai`: Demonstrates how to feed news sentiment data (injury reports/manager quotes) into trading bot expectation adjustments.

