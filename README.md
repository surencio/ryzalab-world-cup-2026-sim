# World Cup 2026 Group Stage Simulator

A statistical forecasting engine and Monte Carlo simulator for the 48-team **2026 FIFA World Cup Group Stage**. This repository contains a pure-Python, zero-dependency implementation of a **Dixon-Coles bivariate Poisson model** to simulate match scorelines, combined with a **stochastic roster availability framework** to model player fitness distributions per round.

---

## TL;DR

*   **Unbiased Simulation:** Runs a 100,000-run Monte Carlo simulation of all 12 groups, resolving standing ties using actual goal counts and randomized tie-breakers.
*   **Stochastic Recovery:** Simulates player recovery curves (e.g., Neymar, Kudus, Davies) round-by-round, meaning teams gain or lose strength as players return to fitness.
*   **Headline Standings:** Brazil is highly vulnerable in Group C (47% group-win chance vs Morocco's 41%) due to injuries, while the USMNT dominates Group D (57% group-win chance) on home soil. A depleted Netherlands team faces a tight three-way race with Sweden and Japan in Group F.

---

## Non-Technical Overview

Most World Cup forecasting engines rely on static metrics (like historical FIFA rankings) and simulate matches like a coin flip (win, draw, or loss). This project models the tournament with two key real-world improvements:

1.  **Lineups Are Not Static:** If a key player like Neymar is recovering from a calf injury, they might miss the first match but play the third. Rather than assuming they are permanently out (which underrates the team) or permanently fit (which overrates them), the simulator rolls a virtual die for each match to determine if they play. The team’s strength dynamically updates for each game.
2.  **Scorelines Matter:** In the new 48-team World Cup format, the top two teams in each group advance, along with the *eight best third-placed teams*. To determine the best third-placed teams, FIFA looks at **Goal Difference** and **Goals Scored**. Because of this, we simulate the exact goals scored per game (e.g., 2-1 or 1-1) rather than just who wins. This lets us calculate the true standings and tie-breakers.

---


## Features

1.  **Dixon-Coles Bivariate Poisson Goal Model:** 
    *   Natively simulates goal counts ($X, Y$) for each match based on team strength differences rather than predicting flat win/draw/loss outcomes.
    *   Applies a bivariate dependency correction factor ($\rho \approx -0.04$) to adjust for low-scoring draws (0-0, 1-1, 1-0, 0-1) typical in tournament football.
    *   Derives team expected goals ($\lambda, \mu$) dynamically from Elo ratings.
2.  **Stochastic Roster Availability Modeling:** 
    *   Replaces arbitrary, static Elo point deductions with round-by-round availability probabilities ($P_{\text{avail}} = [p_1, p_2, p_3]$) for key players recovering from injury.
    *   Samples availability in each Monte Carlo iteration and dynamically adjusts ratings per fixture, allowing teams to gain or lose strength as the tournament progresses.
3.  **Official FIFA Group Stage Tie-Breakers:** 
    *   Sorts teams using the exact sequence: Points $\rightarrow$ Goal Difference (GD) $\rightarrow$ Goals Scored (GS) $\rightarrow$ Elo rating hierarchy.
    *   Randomizes unresolved ties at each stage via pre-sorting shuffles, removing any list-insertion-order bias.

---

## File Structure

*   `simulator.py`: The core simulator containing the Dixon-Coles goal model, stochastic roster parameters, match schedules, and the Monte Carlo simulation engine.
*   `predictions.md`: A detailed predictions report showing average points and standings probabilities (1st, 2nd, 3rd, and 4th place) for all 48 teams across groups A–L, complete with qualitative context.
*   `skills/`:
    *   `sports-probability.md`: A capability definition explaining the mathematical frameworks behind overround vig removal, Dixon-Coles, and draw curves.
    *   `sports-prediction.md`: Guidelines for translating qualitative news (injuries, returns, altitude, heat, and fatigue) into quantitative Elo adjustments.

---

## Usage

Run the simulator using any standard Python 3 interpreter (no external libraries are required):

```bash
python3 simulator.py
```

Running the simulator will output a JSON structure detailing the simulated average points and standings distributions for every team in each of the 12 groups.

---

## Rationale & Methodology

Predicting international football outcomes is difficult due to low scorelines and small sample sizes. Relying on FIFA rankings or simple head-to-head history introduces massive noise. 

This engine uses **Elo-based rating differences** as the foundation. By converting these ratings into expected goals (xG) and simulating matches through a bivariate Poisson process, the model captures the full probability distribution of goal differences. This is vital for simulating the 2026 World Cup's 48-team format, where the eight best third-placed teams qualify for the Round of 32 based on goal difference and goals scored.

---

## CHANGELOG

### [v1.1.0] - 2026-06-11
- **Calibration Engine Upgrade:** 
  - Replaced flat uncalibrated Elo scaling ($s=1.0$) with calibrated damping factor $s=0.58$, determined via leave-one-tournament-out cross-validation to minimize out-of-sample Log Loss.
  - Upgraded expected goals from constant 2.5 goals per match to variable goals model $G(d) = 2.38364 + 0.0013636 \cdot |d|$, where $d$ is the rating difference.
- **Round of 32 Advancement Integration:**
  - Replaced independent group simulations with joint 12-group tournament simulation.
  - Implemented wild-card pool ranking for all 12 third-placed teams using points $\rightarrow$ Goal Difference $\rightarrow$ Goals Scored $\rightarrow$ random tie-breaker.
  - Added tracking and outputting of overall `r32_adv` probabilities (qualifying directly in top 2 or advancing via top 8 third-place spots).
- **Validation Audit Correction:**
  - Corrected historical report stats to match true globally calibrated metrics (Log Loss = 0.5895, Brier = 0.2037, binary accuracy = 66.7%).
  - Corrected baseline report HFA probabilities and added reliability tables comparing baseline vs calibrated predictions.
