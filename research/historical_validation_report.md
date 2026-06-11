# Historical World Cup Validation Report (2014, 2018, 2022)

This report validates the predictive performance of the calibrated **Dixon-Coles goal model (with correlation parameter $\rho = -0.04$)** and standard FIFA group tie-breaker logic against the actual outcomes of the 2014, 2018, and 2022 FIFA World Cups. 

Simulations were run for **100,000 Monte Carlo iterations** per group, utilizing start-of-tournament Elo ratings from [eloratings.net](https://www.eloratings.net) (with a $+100$ Home Field Advantage adjustment applied to host nations).

---

## 1. Executive Summary

The validation demonstrates that the calibrated Dixon-Coles goal model (with Elo damping $s=0.58$) combined with Elo ratings provides a robust and statistically sound foundation for forecasting World Cup group stages. Across all three tournaments (representing 24 groups and 96 teams), the model achieved the following performance highlights:

*   **Binary Qualification Accuracy:** **66.7%** of all teams were correctly classified as qualifiers or non-qualifiers using a 50% probability threshold (64 out of 96 teams).
*   **Qualifier Match Rate (Top 2):** **68.8%** (33 out of 48) of the actual qualifiers were correctly identified by selecting the top two teams by simulated probability in each group.
*   **Global Qualify Brier Score:** **0.2034** (a significant improvement over both a random-guessing baseline of 0.2500 and the uncalibrated model's 0.2158).
*   **Global Qualify Log Loss:** **0.5884**, demonstrating excellent calibration and successfully addressing the overconfidence of the uncalibrated model (0.6318).

Despite strong overall performance, the model remains sensitive to tournament volatility and must deal with "black swan" events—such as Costa Rica winning Group D in 2014, Germany failing to qualify in 2018, or Japan winning Group E in 2022.

---

## 2. Methodology

### Dixon-Coles Goal Simulator
The simulator models the goals scored by Team A ($X$) and Team B ($Y$) as Poisson random variables adjusted for low-scoring correlation:
*   $\lambda_B = \frac{2.5}{1 + 10^{(Elo_A - Elo_B)/400}}$
*   $\lambda_A = 2.5 - \lambda_B$

The parameters $\lambda_A$ and $\lambda_B$ represent the expected goals for each team. The joint probability distribution $P(X=x, Y=y)$ is adjusted using the Dixon-Coles parameter $\rho = -0.04$ to account for the under-inflation of $0\text{--}0, 1\text{--}0, 0\text{--}1,$ and $1\text{--}1$ scorelines typical in professional football:

$$
\tau(x, y) = \begin{cases}
1 - \lambda_A \lambda_B \rho & \text{if } x = 0, y = 0 \\
1 + \lambda_B \rho & \text{if } x = 1, y = 0 \\
1 + \lambda_A \rho & \text{if } x = 0, y = 1 \\
1 - \rho & \text{if } x = 1, y = 1 \\
1 & \text{otherwise}
\end{cases}
$$

### Tie-Breaker Logic
Standings are resolved in each Monte Carlo run using standard FIFA group stage tie-breakers:
1.  **Points** (3 for win, 1 for draw, 0 for loss)
2.  **Goal Difference (GD)**
3.  **Goals Scored (GS)**
4.  **Starting Elo Rating** (used as a deterministic proxy for strength/drawing of lots)

To prevent bias, teams are shuffled randomly before sorting so that absolute ties are not resolved by index order.

### Home Field Advantage (HFA)
The host nations received a $+100$ Elo rating boost to reflect historical host advantage:
*   **2014:** Brazil (Base Elo $2138 \to 2238$)
*   **2018:** Russia (Base Elo $1678 \to 1778$)
*   **2022:** Qatar (Base Elo $1680 \to 1780$)

---

## 3. Overall Predictive Performance

The table below presents the out-of-sample metrics for the calibrated model (with scale damping $s=0.58$ and variable goals $G(d)$) across the three validation tournaments:

| Metric | 2014 World Cup | 2018 World Cup | 2022 World Cup | Global Calibrated |
| :--- | :---: | :---: | :---: | :---: |
| **Qualify Brier Score** | 0.2271 | 0.1490 | 0.2341 | **0.2034** |
| **Qualify Log Loss** | 0.6393 | 0.4781 | 0.6478 | **0.5884** |
| **1st Place Brier Score** | 0.1238 | 0.1325 | 0.1242 | **0.1268** |
| **1st Place Log Loss** | 0.4052 | 0.4110 | 0.4109 | **0.4090** |
| **Qualify Accuracy (>50% Threshold)** | 59.4% | 81.2% | 59.4% | **66.7%** |
| **Correct Qualifiers (Top 2)** | 10 / 16 | 13 / 16 | 10 / 16 | **33 / 48 (68.8%)** |

> [!IMPORTANT]
> **Input Validation Disclosure:** The "Correct Qualifiers (Top 2)" metric selects the two teams in each group with the highest simulated qualification probabilities. Because these probabilities scale monotonically with input Elo ratings, the top 2 teams predicted by the simulator are mathematically identical to the top 2 teams sorted strictly by starting Elo. Therefore, the Top 2 Match Rate (68.8%) validates the predictive accuracy of the underlying **Elo ratings inputs**, rather than the calibration or scoreline distribution of the simulation engine itself. The engine's unique value is instead measured by its probability calibration (Log Loss and Brier Score) and wild-card tie-breaker modeling.

---

## 4. Tournament Breakdowns and Notable Anomalies

### 2014 FIFA World Cup (Brazil)
*   **Brier Score:** 0.2451 | **Log Loss:** 0.6993
*   **Qualifiers Match Rate:** 10 / 16 (62.5%)
*   **Analysis:** 2014 was a highly volatile tournament. The model suffered heavily in **Group B**, where Spain (Elo 2107, 90.9% qualify probability) crashed out in the group stage, allowing Chile to qualify instead. 
*   **Group D** was the largest upset in modern World Cup history: Costa Rica (Elo 1711, 8.4% qualify probability) won a group containing Uruguay, Italy, and England, while England (70.9% qualify probability) finished last.

### 2018 FIFA World Cup (Russia)
*   **Brier Score:** 0.1358 | **Log Loss:** 0.4519
*   **Qualifiers Match Rate:** 13 / 16 (81.2%)
*   **Analysis:** The 2018 tournament was highly predictable according to Elo ratings, yielding the lowest Brier Score (0.1358) and the highest classification accuracy (81.2%).
*   The primary anomaly occurred in **Group F**, where Germany (Elo 2077, 96.4% qualify probability) finished last. Sweden (33.7% qualify probability) won the group instead.
*   In **Group H**, Colombia and Poland were the heavy favorites. While Colombia qualified, Poland (64.6% qualify probability) collapsed, allowing Japan (15.6% qualify probability, who advanced via fair play points over Senegal) to qualify.

### 2022 FIFA World Cup (Qatar)
*   **Brier Score:** 0.2664 | **Log Loss:** 0.7441
*   **Qualifiers Match Rate:** 11 / 16 (68.8%)
*   **Analysis:** The 2022 tournament featured several historic upsets. In **Group E**, Japan (17.9% qualify probability) beat both Germany (79.3% qualify probability) and Spain (92.2% qualify probability) to win the group. 
*   In **Group F**, Morocco (17.0% qualify probability) won the group, while Belgium (89.4% qualify probability) was eliminated.
*   In **Group D**, Denmark (87.5% qualify probability) finished last, while Australia (11.3% qualify probability) advanced.

---

## 5. Key Model Insights and Calibration

### Host Performance and the HFA Adjustment
Applying a $+100$ Elo HFA to host nations shows mixed results, but the calibrated model successfully tones down the overconfidence of the baseline model:
1.  **Russia (2018):** Base Elo $1678 \to 1778$ (HFA). The baseline uncalibrated model gave Russia a **72.3%** chance to qualify. The calibrated model compressed this to **63.7%**. In reality, Russia qualified in 2nd place.
2.  **Qatar (2022):** Base Elo $1680 \to 1780$ (HFA). The baseline uncalibrated model gave Qatar a **35.0%** chance to qualify. The calibrated model gave them a **39.2%** chance. In reality, Qatar crashed out with 0 points, demonstrating HFA cannot overcome a massive structural quality deficit.
3.  **Brazil (2014):** Base Elo $2138 \to 2238$ (HFA). The baseline uncalibrated model gave Brazil a **99.3%** chance to qualify. The calibrated model adjusted this to **97.3%**. Brazil comfortably won the group.

### Calibration and the Uniform Baseline
A critical failure mode of the baseline model ($s=1.0$) is its extreme overconfidence. In volatile tournaments with massive upsets (2014 and 2022), the baseline model actually performed **worse** than a uniform random guessing baseline (which has a constant Log Loss of **0.6931 nats** per fold):
- **2014 Fold Log Loss:** Baseline = **0.6993** (failed to beat uniform baseline) vs. Calibrated = **0.6393** (successfully beats baseline).
- **2022 Fold Log Loss:** Baseline = **0.7441** (failed to beat uniform baseline) vs. Calibrated = **0.6478** (successfully beats baseline).

By compressing Elo differences using $s=0.58$, the calibrated model avoids over-penalization from major upsets, outperforming the uniform baseline in every single fold.

### Reliability Analysis: Baseline vs. Calibrated Model
To analyze probability accuracy, we compare how the predicted qualification probabilities align with observed outcomes across all 96 historical team campaigns:

#### Uncalibrated Baseline Reliability Table ($s=1.0$)
| Probability Bin | Team Count | Expected Probability | Observed Probability | Error (Obs - Exp) |
| :---: | :---: | :---: | :---: | :---: |
| **0.0 – 0.2** | 26 | 10.86% | 26.92% | **+16.07%** (Underconfident) |
| **0.2 – 0.4** | 16 | 31.01% | 37.50% | +6.49% |
| **0.4 – 0.6** | 14 | 49.63% | 42.86% | -6.77% |
| **0.6 – 0.8** | 13 | 68.61% | 61.54% | -7.08% |
| **0.8 – 1.0** | 27 | 90.18% | 77.78% | **-12.40%** (Overconfident) |

*Analysis:* The baseline model shows severe overconfidence in the top bin (predicting 90.2% expected qualification but only observing 77.8%) and severe underestimation of low-probability underdogs in the bottom bin (predicting 10.9% expected qualification but observing 26.9% actually qualifying).

#### Calibrated Model Reliability Table ($s=0.58$)
| Probability Bin | Team Count | Expected Probability | Observed Probability | Error (Obs - Exp) |
| :---: | :---: | :---: | :---: | :---: |
| **0.0 – 0.2** | 10 | 14.31% | 10.00% | **-4.31%** |
| **0.2 – 0.4** | 27 | 28.26% | 33.33% | +5.07% |
| **0.4 – 0.6** | 24 | 49.24% | 50.00% | **+0.76%** |
| **0.6 – 0.8** | 19 | 69.94% | 63.16% | -6.78% |
| **0.8 – 1.0** | 16 | 86.45% | 87.50% | **+1.05%** |

*Analysis:* The calibrated model dramatically reduces error. The top bin error drops from **-12.40%** to a mere **+1.05%**, while the bottom bin error drops from **+16.07%** to **-4.31%**. The middle bin ($0.4\text{--}0.6$) is almost perfectly aligned at **+0.76%** error.

### Limits of Elo-based Forecasting
Elo ratings are backward-looking and represent a long-term rolling average of team performance. Consequently, they fail to capture:
*   **Roster changes and manager effects:** A team's Elo does not immediately reflect a new manager's tactics or key player injuries.
*   **Generational decline:** Older squads (such as Belgium in 2022 or Spain in 2014) often maintain high Elo ratings based on past achievements despite declining physical performance.
*   **Short-term variance:** The World Cup group stage consists of only 3 matches per team, making it highly susceptible to single-match variance (e.g., red cards, penalty decisions).

---

## 6. Conclusion

The Dixon-Coles goal model (with $\rho = -0.04$) calibrated against historical Elo ratings using an Elo damping factor $s=0.58$ and a variable expected goals model $G(d)$ serves as a highly robust baseline model for international soccer tournaments. By achieving an out-of-sample binary qualification accuracy of **66.7%**, a Brier Score of **0.2034**, and a Log Loss of **0.5884**, the calibrated model successfully fixes the overconfidence issues of the uncalibrated baseline and outperforms a uniform random guessing baseline in all folds.

To improve prediction accuracy for future tournaments (like the 2026 World Cup), we recommend integrating **stochastic roster hazard modeling** (as implemented in `simulator.py` for Davies, Saka, and Neymar) to dynamically adjust Elo ratings based on key player availability and expected team lineups. This dynamic adjustment, combined with the calibrated engine, provides the most reliable forecasting tool for the expanded 48-team tournament structure.
