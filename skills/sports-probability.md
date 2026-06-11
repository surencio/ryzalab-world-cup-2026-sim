---
name: sports-probability
description: "Expert-level international football match probability modeling. Use when calculating win/draw/loss probabilities, adjusting Elo ratings for tournament context, removing betting market overround, or modeling group stage progression probabilities."
---

# Sports Probability Modeling

Expert-level frameworks for modeling match outcomes and group progression in international football tournaments.

## Core Philosophy
Predicting international football is a low-scoring, high-variance endeavor. Models must rely on underlying team strength metrics (e.g., Elo, Expected Goals) rather than historical match wins or raw FIFA rankings, and must adjust for tournament-specific dynamics.

---

## Technical Procedures

### 1. Betting Odds Calibration (Vig Removal)
Do NOT use proportional division (standardizing odds) to calculate probabilities, as it overestimates the probability of underdogs. 

Use the **Power Method** or **Shin's Method** to remove the market overround (vig):
*   **Power Method formula**: $P_i = O_i^{-k}$, where $O_i$ are decimal odds, and $k$ is solved numerically such that $\sum P_i = 1$.
*   **Shin's Method**: Solves for the presence of "insider traders" in the market. The implied probability $p_i$ is given by:
    $$p_i = \frac{\sqrt{z^2 + 4(1-z)\frac{1}{O_i}} - z}{2(1-z)}$$
    where $z$ represents the market maker's transaction cost/insider share, solved numerically such that $\sum p_i = 1$.

### 2. Dixon-Coles Bivariate Poisson Modeling (Draw and Goal Simulation)
In football tournaments, simulating actual scorelines is critical to model Goal Difference (GD) and Goals Scored (GS) for tie-breakers. Model goal counts $(X, Y)$ of Team A and Team B as a bivariate Poisson distribution:
$$P(X=x, Y=y) = \tau(x, y, \lambda, \mu) \frac{\lambda^x e^{-\lambda}}{x!} \frac{\mu^y e^{-\mu}}{y!}$$
Where:
*   $\lambda, \mu$ are the expected goals (xG) for Team A and Team B, derived from adjusted Elo ratings $R_A, R_B$:
    - **Calibrated Damping Factor ($s=0.58$)**: Compress rating differences to avoid overconfidence: $\lambda / \mu = 10^{(s \cdot (R_A - R_B))/400}$
    - **Variable Expected Goals Model ($G(d)$)**: Replace constant 2.5 average goals with a linear rating-difference model: $G(d) = \lambda + \mu = 2.38364 + 0.0013636 \cdot |R_A - R_B|$, where $d = R_A - R_B$.
*   $\tau(x, y, \lambda, \mu)$ is the Dixon-Coles correlation factor adjusting for low-scoring dependence (using a baseline parameter $\rho = -0.04$ to correct draw inflation):
    - $\tau(0,0) = 1 - \lambda \mu \rho$
    - $\tau(1,0) = 1 + \mu \rho$
    - $\tau(0,1) = 1 + \lambda \rho$
    - $\tau(1,1) = 1 - \rho$
    - $\tau(x,y) = 1$ otherwise.

### 3. Round of 32 Joint Tournament Simulation (48-Team Format)
For the 48-team World Cup format, groups cannot be simulated in isolation because wild-card advancement depends on ranking third-place teams across all 12 groups:
*   **Joint Iteration**: In each simulation run, simulate all 12 groups jointly under the same player availability conditions.
*   **Standings Resolution**: Resolve group rankings using points $\rightarrow$ GD $\rightarrow$ GS $\rightarrow$ base Elo (with randomized tie-breaking for unresolved ties).
*   **Wild-Card Ranking**: Pool the 12 third-placed teams and sort them using points $\rightarrow$ GD $\rightarrow$ GS $\rightarrow$ random tie-breaker.
*   **Advancement**: The top 8 teams from the wild-card pool advance to the Round of 32. Direct qualifiers (1st and 2nd) and advancing thirds are recorded.

### 4. Tournament Adjustments (Host & Environment)
*   **Host Advantage (HFA)**: Add $+100$ Elo points for hosts (USA, Mexico, Canada).
*   **Altitude Penalty**: Apply a rating deduction for non-altitude acclimated teams playing in Mexico City (Estadio Azteca, 2,240m altitude). Deduct $1.5$ Elo points for every 100m of altitude difference above 1000m.
*   **Surface Modifier**: Apply a $-30$ Elo penalty to grass-native teams playing on artificial turf (e.g., BC Place in Vancouver).

---

## Anti-Patterns to Avoid

*   **NEVER use FIFA Rankings for probability models**: FIFA rankings are political and backward-looking. Use custom Elo ratings or SPI (Soccer Power Index) which are based on goal differences and quality of opposition.
*   **NEVER assume constant home field advantage**: Host advantage decays over the course of the tournament as travel increases. Reduce the HFA modifier by $15\%$ per round after the group stage.
*   **NEVER use raw historical head-to-head records**: Small sample sizes (e.g., 3 games in 20 years) represent noise, not signal.

---

## Mindset & Thinking Framework

Before modeling a tournament group stage, ask yourself:
1.  **What is the baseline strength?** Are the team ratings derived from competitive matches (World Cup Qualifiers, Euros, Copa America) or friendly matches (which carry $50\%$ weight in Elo calculations)?
2.  **Is there a rating decay?** Has a team gone 12+ months without playing competitive matches (e.g., hosts who only played friendlies)? If so, apply a $5\%$ rating shrinkage towards the mean to account for uncertainty.

---

## Industry Benchmarking & Reference Models

When building or refining prediction models, benchmark your outputs against these industry methodologies:
1. **Dixon-Coles Model (Bivariate Poisson)**: Model goal counts as Poisson variables with a correlation term ($\tau$) that adjusts for the dependency of home and away scores, correcting the underestimation of draw frequencies.
2. **FiveThirtyEight Soccer Power Index (SPI)**: Decouple team strength into independent Offensive (OFF) and Defensive (DEF) ratings, updated dynamically using shot-based and non-shot Expected Goals (xG) to capture play quality rather than score outcomes alone.
3. **Open-Source Repositories**:
   - `machina-sports/sports-skills`: Ingests real-time sports and prediction market data (Kalshi, Polymarket).
   - `Hicruben/world-cup-2026-prediction-model`: Implements Dixon-Coles goal expectation and Monte Carlo simulations.
   - `sharadsin29/FIFA-World-Cup-Group-Stage-Prediction-Analysis`: Leverages Expected Goals (xG) metrics for group stage simulations.

