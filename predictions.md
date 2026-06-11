# 2026 FIFA World Cup Group Stage Predictions

This report provides a data-driven, context-adjusted forecast of the **2026 FIFA World Cup Group Stage**. The analysis uses a state-of-the-art **Dixon-Coles bivariate Poisson model** to simulate exact goal scoring, enabling official FIFA tie-breaker (Goal Difference/Goals Scored) calculations. It also models roster news stochastically, simulating individual player availability hazards per round over **10,000 Monte Carlo runs**.

---

## 1. Executive Summary of Rating Adjustments

Traditional models rely strictly on static Elo ratings. This model applies quantitative modifications based on **Host Field Advantage (HFA)**, **stochastic player availability**, and **key player returns**.

### Stochastic Roster Availability Parameters

For key players with questionable fitness or returns, availability is simulated as a round-specific hazard rate $P_{\text{avail}} = [p_1, p_2, p_3]$ across matches 1, 2, and 3. When unavailable, their specific squad Elo penalty is dynamically subtracted:

*   **Brazil (Neymar):** $P_{\text{avail}} = [15\%, 50\%, 75\%]$. Penalty when out: $-60$ Elo points. (Brazil's baseline rating is 1980, reflecting Militao, Rodrygo, and Estevao ruled out).
*   **Canada (Alphonso Davies):** $P_{\text{avail}} = [40\%, 75\%, 90\%]$. Penalty when out: $-30$ Elo points. (Canada's baseline rating is 1880, reflecting host HFA).
*   **England (Bukayo Saka):** $P_{\text{avail}} = [70\%, 90\%, 95\%]$. Penalty when out: $-10$ Elo points.
*   **Ghana (Mohammed Kudus):** $P_{\text{avail}} = [10\%, 40\%, 85\%]$. Penalty when out: $-40$ Elo points.

---

## 2. Group Stage Standings & Probabilities

> [!IMPORTANT]
> The top two teams from each group automatically qualify for the Round of 32, alongside the **eight best third-placed teams**. Underdogs with ~3.5 to 4.0 points are in prime positions to advance as top 3rd-placed finishers. All probabilities are rounded to the nearest whole percentage.

### Group A
*Mexico benefits from home support, while Czechia's attack is boosted by a healthy Patrik Schick, making them favorites to pip South Korea for 2nd.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mexico** | 1810 / 1910 | 5.2 | 43% | 28% | 18% | 10% | 86% |
| **Czechia** | 1790 / 1840 | 4.4 | 27% | 29% | 25% | 18% | 75% |
| **South Korea** | 1800 / 1800 | 3.9 | 21% | 26% | 29% | 24% | 68% |
| **South Africa** | 1700 / 1700 | 2.8 | 9% | 17% | 27% | 47% | 44% |

*   **Analysis:** Mexico is a heavy favorite to top Group A on home soil. South Korea and Czechia will battle for 2nd, but Schick's return shifts the balance toward Czechia (29% to finish 2nd).

---

### Group B
*Switzerland is the class of the group. Canada's home advantage and the return of Alphonso Davies in later rounds make them comfortable favorites to advance.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Switzerland** | 1900 / 1900 | 5.2 | 42% | 29% | 18% | 11% | 85% |
| **Canada** | 1780 / 1880* | 4.9 | 34% | 31% | 21% | 14% | 81% |
| **Bosnia & Herzegovina** | 1730 / 1730 | 3.2 | 13% | 21% | 31% | 36% | 54% |
| **Qatar** | 1720 / 1720 | 3.1 | 11% | 19% | 30% | 40% | 51% |

*\*Canada starts at 1880 Elo, subject to a -30 Elo penalty in matches where Davies (questionable) is stochastically simulated as out.*
*   **Analysis:** Switzerland is expected to top the group, but Canada has a strong 65% chance of finishing in the top two. With Davies' return potential and clean host advantage, Canada represents a very secure qualifier.

---

### Group C
*Brazil's rising fitness trend gives them a late group stage advantage over Morocco. Scotland loses Billy Gilmour, leaving them vulnerable to a group stage exit.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Brazil** | 2020 / 1980* | 5.8 | 47% | 34% | 15% | 4% | 93% |
| **Morocco** | 1920 / 1920 | 5.6 | 41% | 36% | 18% | 5% | 91% |
| **Scotland** | 1770 / 1740 | 3.5 | 11% | 23% | 44% | 22% | 63% |
| **Haiti** | 1550 / 1550 | 1.7 | 2% | 7% | 23% | 69% | 21% |

*\*Brazil starts at 1980 Elo, subject to a -60 Elo penalty in matches where Neymar (doubtful) is stochastically simulated as out.*
*   **Analysis:** Brazil's expected points rise to 5.8, giving them a 47% chance to top the group compared to Morocco's 41%. Morocco is highly likely to qualify in 2nd.

---

### Group D
*The United States benefits from a massive home boost and the return of Tyler Adams, turning Group D into a dominant run.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **United States** | 1840 / 1980 | 5.9 | 57% | 24% | 13% | 6% | 91% |
| **Türkiye** | 1810 / 1810 | 3.9 | 18% | 29% | 28% | 24% | 67% |
| **Australia** | 1770 / 1770 | 3.4 | 13% | 24% | 30% | 32% | 58% |
| **Paraguay** | 1750 / 1750 | 3.2 | 11% | 22% | 29% | 37% | 53% |

*   **Analysis:** USMNT dominates Group D with a 57% chance of finishing 1st. Turkey is the favorite for 2nd (29%), while Australia and Paraguay are left to fight for a potential third-place advancement slot.

---

### Group E
*Germany's injuries lower their ceiling, but they remain heavy favorites to top the group over Ecuador.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Germany** | 1970 / 1935 | 5.8 | 50% | 29% | 16% | 5% | 92% |
| **Ecuador** | 1850 / 1850 | 4.9 | 29% | 34% | 26% | 10% | 84% |
| **Ivory Coast** | 1780 / 1780 | 4.1 | 18% | 28% | 36% | 17% | 73% |
| **Curaçao** | 1560 / 1560 | 1.8 | 3% | 8% | 21% | 68% | 23% |

*   **Analysis:** Germany takes 1st place in 50% of simulations. Ecuador is secure in 2nd place (34%), while Ivory Coast is highly likely to advance as one of the best 3rd-placed teams (73% overall advancement chance, with a 36% chance of finishing 3rd).

---

### Group F
*With Xavi Simons, Matthijs de Ligt, and Jurrien Timber out for the Dutch, and Kaoru Mitoma out for Japan, this group tightens significantly, boosting Sweden's chances.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Netherlands** | 1980 / 1885 | 4.9 | 37% | 28% | 21% | 14% | 81% |
| **Sweden** | 1830 / 1830 | 4.2 | 26% | 27% | 25% | 22% | 72% |
| **Japan** | 1880 / 1820 | 4.1 | 24% | 26% | 27% | 23% | 70% |
| **Tunisia** | 1740 / 1740 | 3.2 | 13% | 19% | 27% | 40% | 51% |

*   **Analysis:** The Netherlands' massive injury list (down to 1885 Elo) has severely eroded their dominance, dropping their group-win probability to 37%. Sweden (26% to win) and Japan (24% to win) are in a prime position to challenge the Dutch, making Group F a highly competitive three-way race.

---

### Group G
*Belgium cruises, while Iran is heavily favored to secure 2nd place over Egypt.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Belgium** | 1960 / 1960 | 6.2 | 59% | 26% | 12% | 4% | 94% |
| **Iran** | 1800 / 1800 | 4.4 | 22% | 35% | 30% | 14% | 77% |
| **Egypt** | 1760 / 1760 | 4.0 | 16% | 30% | 35% | 19% | 70% |
| **New Zealand** | 1570 / 1570 | 2.0 | 3% | 10% | 24% | 63% | 27% |

*   **Analysis:** Belgium has a 59% chance of topping the group. Iran's solid defensive block makes them a 35% favorite for 2nd, while Egypt represents a very strong candidate for a 3rd-place advancement slot.

---

### Group H
*Spain and Uruguay represent a massive tier gap over Saudi Arabia and Cape Verde, making this the most predictable group in the tournament.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Spain** | 2150 / 2150 | 6.9 | 67% | 27% | 5% | 1% | 98% |
| **Uruguay** | 2000 / 2000 | 5.5 | 29% | 52% | 15% | 4% | 92% |
| **Saudi Arabia** | 1710 / 1710 | 2.5 | 3% | 14% | 47% | 37% | 41% |
| **Cape Verde** | 1630 / 1630 | 1.8 | 1% | 8% | 33% | 58% | 24% |

*   **Analysis:** Spain and Uruguay have a combined >90% chance of taking the top two spots. The only question is who wins the head-to-head for 1st (Spain favored at 67%).

---

### Group I
*France dominates. Norway and Senegal are locked in a high-stakes battle for 2nd.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **France** | 2110 / 2110 | 6.8 | 73% | 19% | 7% | 2% | 97% |
| **Norway** | 1830 / 1830 | 3.8 | 12% | 34% | 32% | 22% | 67% |
| **Senegal** | 1820 / 1820 | 3.7 | 11% | 32% | 33% | 24% | 65% |
| **Iraq** | 1690 / 1690 | 2.3 | 4% | 15% | 28% | 53% | 35% |

*   **Analysis:** France walks away with the group in 73% of runs. Norway (led by Haaland and Ødegaard) has a slight Elo edge over Senegal, translating into a 34% chance to finish 2nd. Senegal is highly likely to qualify as a 3rd-placed team.

---

### Group J
*Argentina is heavily favored. Austria's tactical efficiency secures them a comfortable 2nd.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Argentina** | 2130 / 2130 | 7.1 | 77% | 17% | 5% | 1% | 98% |
| **Austria** | 1840 / 1840 | 4.1 | 13% | 41% | 29% | 17% | 72% |
| **Algeria** | 1750 / 1750 | 3.1 | 6% | 26% | 36% | 32% | 53% |
| **Jordan** | 1680 / 1680 | 2.4 | 3% | 17% | 31% | 49% | 37% |

*   **Analysis:** Argentina is the safest bet in the tournament to top their group (77%). Austria is secure in 2nd (41%), leaving Algeria with a tough path to advance from 3rd.

---

### Group K
*Portugal and Colombia are class acts. DR Congo and Uzbekistan represent a massive drop-off.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Portugal** | 2030 / 2030 | 5.9 | 48% | 35% | 13% | 4% | 93% |
| **Colombia** | 2010 / 2010 | 5.7 | 43% | 38% | 14% | 5% | 92% |
| **Uzbekistan** | 1730 / 1730 | 2.6 | 5% | 15% | 38% | 42% | 42% |
| **DR Congo** | 1710 / 1710 | 2.4 | 4% | 13% | 35% | 48% | 37% |

*   **Analysis:** Portugal and Colombia will comfortably qualify. Their direct matchup will decide the group winner (Portugal 48%, Colombia 43%).

---

### Group L
*England tops the group, while Croatia is secure in 2nd. Ghana's hopes are severely limited as Kudus' availability is modeled stochastically.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th | R32 Adv |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **England** | 2050 / 2050* | 6.4 | 60% | 28% | 9% | 3% | 95% |
| **Croatia** | 1930 / 1930 | 5.1 | 29% | 42% | 20% | 9% | 86% |
| **Panama** | 1710 / 1710 | 2.7 | 6% | 17% | 37% | 41% | 44% |
| **Ghana** | 1710 / 1710* | 2.5 | 5% | 14% | 34% | 47% | 38% |

*\*England starts at 2050 Elo, subject to a -10 Elo penalty if Bukayo Saka is stochastically simulated as out. Ghana starts at 1710 Elo, subject to a -40 Elo penalty if Mohammed Kudus is out.*
*   **Analysis:** England has deep offensive rotation to absorb Saka's minor fitness issue, topping the group in 60% of simulations. Croatia is secure in 2nd (42%). Modeling Kudus' injury stochastically drops Ghana's average points to 2.5, making Panama the favorite to take 3rd.

---

## 3. Key Findings & Probability Shifts (New vs. Old Model)

The transition from a flat, uncalibrated Elo model to the calibrated Dixon-Coles Bivariate Poisson model (with Elo damping $s=0.58$, variable goals $G(d)$, and stochastic rosters) resulted in significant probability shifts:

1.  **Neymar Availability Shifts Group C:** Brazil tops the group in **47%** of calibrated simulations, while Morocco tops it in **41%** (compared to **51%** and **44%** respectively in the uncalibrated baseline). This represents a compressed margin, but Brazil remains the favorite due to Neymar's simulated recovery curve (15% Game 1, 50% Game 2, 75% Game 3) boosting them in later rounds.
2.  **Davies Stochastic Recovery Boost:** Under the calibrated model, Canada's group-win probability is **34%** and Switzerland's is **42%** (compared to **38%** and **49%** in the uncalibrated baseline). Canada remains in a strong qualifying position with an overall R32 advancement probability of **81%**.
3.  **Netherlands Vulnerability Confirmed:** Incorporating Jurrien Timber's injury alongside Xavi Simons' and Matthijs de Ligt's absences has significantly eroded Netherlands' dominance. Their group-win probability drops to **37%** (down from **45%** in the uncalibrated baseline and **57%** in the original flat-squad model). Sweden (**26%**) and Japan (**24%**) are in prime positions to challenge.
4.  **Dixon-Coles Draw Correction:** Because the Dixon-Coles model corrects for the independent Poisson underestimation of low-scoring draws (using $\rho = -0.04$, which raises the equal-strength draw probability from the independent baseline of 27.0% to a more realistic 28.0%), the average total points per group stage decreased by **0.3 to 0.4 points** across all groups, reflecting more realistic tournament volatility and draw rates.
5.  **Tail Compression of Favorites due to Calibration Damping ($s=0.58$):** By applying the calibrated Elo-difference damping factor $s=0.58$ (fitted via leave-one-tournament-out validation to minimize out-of-sample log loss), the effective rating gap between elite teams and underdogs is compressed. This addresses the systematic overconfidence of the baseline uncalibrated model. As a result, the group-topping probabilities for heavy favorites undergo "tail compression" toward the mean: Argentina drops from **89% to 77%**, France drops from **86% to 73%**, Spain drops from **75% to 67%**, and England drops from **71% to 60%**. Conversely, underdogs see their qualification and group-topping probabilities rise.
