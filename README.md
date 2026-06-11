# World Cup 2026 Group Stage Simulator

A statistical forecasting engine and Monte Carlo simulator for the 48-team **2026 FIFA World Cup Group Stage**. This repository contains a pure-Python, zero-dependency implementation of a **Dixon-Coles bivariate Poisson model** to simulate match scorelines, combined with a **stochastic roster availability framework** to model player fitness distributions per round.

---

## Features

1.  **Dixon-Coles Bivariate Poisson Goal Model:** 
    *   Natively simulates goal counts ($X, Y$) for each match based on team strength differences rather than predicting flat win/draw/loss outcomes.
    *   Applies a bivariate dependency correction factor ($\rho \approx -0.08$) to adjust for low-scoring draws (0-0, 1-1, 1-0, 0-1) typical in tournament football.
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
