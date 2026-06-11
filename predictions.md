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

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Mexico** | 1810 / 1910 | 5.9 | 53% | 27% | 15% | 5% |
| **Czechia** | 1790 / 1840 | 4.6 | 26% | 34% | 27% | 13% |
| **South Korea** | 1800 / 1800 | 3.9 | 17% | 27% | 34% | 21% |
| **South Africa** | 1700 / 1700 | 2.1 | 4% | 11% | 25% | 60% |

*   **Analysis:** Mexico is a heavy favorite to top Group A on home soil. South Korea and Czechia will battle for 2nd, but Schick's return shifts the balance toward Czechia (34% to finish 2nd).

---

### Group B
*Switzerland is the class of the group. Canada's home advantage and the return of Alphonso Davies in later rounds make them comfortable favorites to advance.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Switzerland** | 1900 / 1900 | 5.8 | 50% | 31% | 13% | 5% |
| **Canada** | 1780 / 1880* | 5.3 | 38% | 37% | 18% | 7% |
| **Bosnia & Herzegovina** | 1730 / 1730 | 2.7 | 7% | 16% | 36% | 41% |
| **Qatar** | 1720 / 1720 | 2.6 | 6% | 16% | 33% | 46% |

*\*Canada starts at 1880 Elo, subject to a -30 Elo penalty in matches where Davies (questionable) is stochastically simulated as out.*
*   **Analysis:** Switzerland is expected to top the group, but Canada has a strong 75% chance of finishing in the top two. With Davies' return potential and clean host advantage, Canada represents a very secure qualifier.

---

### Group C
*Brazil's rising fitness trend gives them a late group stage advantage over Morocco. Scotland loses Billy Gilmour, leaving them vulnerable to a group stage exit.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Brazil** | 2020 / 1980* | 6.4 | 51% | 38% | 10% | 1% |
| **Morocco** | 1920 / 1920 | 6.1 | 44% | 42% | 13% | 1% |
| **Scotland** | 1770 / 1740 | 3.3 | 5% | 18% | 60% | 17% |
| **Haiti** | 1550 / 1550 | 1.0 | 0% | 2% | 17% | 81% |

*\*Brazil starts at 1980 Elo, subject to a -60 Elo penalty in matches where Neymar (doubtful) is stochastically simulated as out.*
*   **Analysis:** Brazil's extensive injury list (Militao, Rodrygo, Estevao out) initially brought them level with Morocco. However, because Neymar's availability scales up over the group stage (from 15% to 75%), Brazil's expected points rise to 6.4, giving them a 51% chance to top the group compared to Morocco's 44%. Morocco is highly likely to qualify in 2nd.

---

### Group D
*The United States benefits from a massive home boost and the return of Tyler Adams, turning Group D into a dominant run.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **United States** | 1840 / 1980 | 6.8 | 73% | 18% | 7% | 2% |
| **Türkiye** | 1810 / 1810 | 3.8 | 13% | 35% | 29% | 22% |
| **Australia** | 1770 / 1770 | 3.1 | 8% | 25% | 33% | 34% |
| **Paraguay** | 1750 / 1750 | 2.8 | 6% | 22% | 31% | 42% |

*   **Analysis:** USMNT dominates Group D with a 73% chance of finishing 1st. Turkey is the favorite for 2nd, while Australia and Paraguay are left to fight for a potential third-place advancement slot.

---

### Group E
*Germany's injuries lower their ceiling, but they remain heavy favorites to top the group over Ecuador.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Germany** | 1970 / 1935 | 6.5 | 59% | 28% | 12% | 1% |
| **Ecuador** | 1850 / 1850 | 5.1 | 27% | 42% | 27% | 4% |
| **Ivory Coast** | 1780 / 1780 | 4.0 | 13% | 28% | 48% | 11% |
| **Curaçao** | 1560 / 1560 | 1.0 | 0% | 3% | 14% | 83% |

*   **Analysis:** Germany takes 1st place in 59% of simulations. Ecuador is very secure in 2nd place (42%), while Ivory Coast is highly likely to advance as one of the best 3rd-placed teams (48% chance of 3rd).

---

### Group F
*With Xavi Simons, Matthijs de Ligt, and Jurrien Timber out for the Dutch, and Kaoru Mitoma out for Japan, this group tightens significantly, boosting Sweden's chances.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Netherlands** | 1980 / 1885 | 5.4 | 45% | 28% | 18% | 9% |
| **Sweden** | 1830 / 1830 | 4.3 | 25% | 29% | 27% | 19% |
| **Japan** | 1880 / 1820 | 4.1 | 23% | 27% | 29% | 21% |
| **Tunisia** | 1740 / 1740 | 2.6 | 7% | 15% | 27% | 51% |

*   **Analysis:** The Netherlands' massive injury list (down to 1885 Elo) has severely eroded their dominance, dropping their group-win probability to 45%. Sweden (25% to win) and Japan (23% to win) are in a prime position to challenge the Dutch, making Group F a highly competitive three-way race.

---

### Group G
*Belgium cruises, while Iran is heavily favored to secure 2nd place over Egypt.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Belgium** | 1960 / 1960 | 7.0 | 72% | 21% | 7% | 1% |
| **Iran** | 1800 / 1800 | 4.6 | 17% | 43% | 33% | 8% |
| **Egypt** | 1760 / 1760 | 3.9 | 11% | 32% | 44% | 14% |
| **New Zealand** | 1570 / 1570 | 1.2 | 1% | 5% | 17% | 78% |

*   **Analysis:** Belgium has a 72% chance of topping the group. Iran's solid defensive block makes them a 43% favorite for 2nd, while Egypt represents a very strong candidate for a 3rd-place advancement slot.

---

### Group H
*Spain and Uruguay represent a massive tier gap over Saudi Arabia and Cape Verde, making this the most predictable group in the tournament.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Spain** | 2150 / 2150 | 7.5 | 75% | 23% | 2% | 0% |
| **Uruguay** | 2000 / 2000 | 5.8 | 24% | 65% | 10% | 1% |
| **Saudi Arabia** | 1710 / 1710 | 2.3 | 1% | 8% | 57% | 34% |
| **Cape Verde** | 1630 / 1630 | 1.4 | 0% | 3% | 32% | 64% |

*   **Analysis:** Spain and Uruguay have a combined >98% chance of taking the top two spots. The only question is who wins the head-to-head for 1st (Spain favored at 75%).

---

### Group I
*France dominates. Norway and Senegal are locked in a high-stakes battle for 2nd.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **France** | 2110 / 2110 | 7.6 | 86% | 11% | 2% | 0% |
| **Norway** | 1830 / 1830 | 3.8 | 7% | 41% | 36% | 17% |
| **Senegal** | 1820 / 1820 | 3.7 | 6% | 38% | 38% | 18% |
| **Iraq** | 1690 / 1690 | 1.6 | 1% | 10% | 24% | 65% |

*   **Analysis:** France walks away with the group in 86% of runs. Norway (led by Haaland and Ødegaard) has a slight Elo edge over Senegal, translating into a 41% chance to finish 2nd. Senegal is highly likely to qualify as a 3rd-placed team.

---

### Group J
*Argentina is heavily favored. Austria's tactical efficiency secures them a comfortable 2nd.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Argentina** | 2130 / 2130 | 7.8 | 88% | 10% | 1% | 0% |
| **Austria** | 1840 / 1840 | 4.3 | 8% | 53% | 27% | 11% |
| **Algeria** | 1750 / 1750 | 2.8 | 2% | 24% | 42% | 31% |
| **Jordan** | 1680 / 1680 | 1.8 | 1% | 12% | 30% | 57% |

*   **Analysis:** Argentina is the safest bet in the tournament to top their group (88%). Austria is highly secure in 2nd (53%), leaving Algeria with a tough path to advance from 3rd.

---

### Group K
*Portugal and Colombia are class acts. DR Congo and Uzbekistan represent a massive drop-off.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Portugal** | 2030 / 2030 | 6.5 | 52% | 40% | 7% | 1% |
| **Colombia** | 2010 / 2010 | 6.3 | 45% | 45% | 8% | 1% |
| **Uzbekistan** | 1730 / 1730 | 2.1 | 1% | 8% | 45% | 45% |
| **DR Congo** | 1710 / 1710 | 1.9 | 1% | 7% | 40% | 52% |

*   **Analysis:** Portugal and Colombia will comfortably qualify. Their direct matchup will decide the group winner (Portugal 52%, Colombia 45%).

---

### Group L
*England tops the group, while Croatia is secure in 2nd. Ghana's hopes are severely limited as Kudus' availability is modeled stochastically.*

| Team | Base / Adj. Elo | Avg. Pts | 1st | 2nd | 3rd | 4th |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **England** | 2050 / 2050* | 7.1 | 70% | 26% | 4% | 1% |
| **Croatia** | 1930 / 1930 | 5.5 | 27% | 56% | 14% | 3% |
| **Panama** | 1710 / 1710 | 2.3 | 2% | 11% | 47% | 41% |
| **Ghana** | 1710 / 1710* | 1.8 | 1% | 8% | 36% | 55% |

*\*England starts at 2050 Elo, subject to a -10 Elo penalty if Bukayo Saka is stochastically simulated as out. Ghana starts at 1710 Elo, subject to a -40 Elo penalty if Mohammed Kudus is out.*
*   **Analysis:** England has deep offensive rotation to absorb Saka's minor fitness issue, topping the group in 70% of simulations. Croatia is highly secure in 2nd (56%). Modeling Kudus' injury stochastically (very low availability in Games 1 & 2) drops Ghana's average points to 1.8, making Panama the favorite to take 3rd.

---

## 3. Key Findings & Probability Shifts (New vs. Old Model)

The transition from a flat scalar Elo model to the Dixon-Coles Bivariate Poisson model with stochastic rosters resulted in significant probability shifts:

1.  **Neymar Availability Shifts Group C (+4% Brazil / -3% Morocco):** In the previous flat model (which assumed Neymar was out the entire group stage), Brazil and Morocco were locked at a 47% coin-flip. The new model simulates Neymar's recovery (available at 15% in game 1, rising to 50% and 75%). This raises Brazil's expected strength in later rounds, shifting their group-win probability up to **51%** (Morocco drops to **44%**).
2.  **Davies Stochastic Availability Shifts Group B (+5% Canada / -4% Switzerland):** Canada's 1st place chance rose to **38%** (up from 33% in the old model) because Davies' questionable status is simulated as a distribution (raising Canada's Elo back to 1880 in later games when he plays) rather than a flat injury deduction.
3.  **Netherlands Vulnerability Confirmed (Netherlands 45% / Sweden 25% / Japan 23%):** Incorporating Timber's groin injury alongside Simons' absence drops the Dutch group-win probability to **45%** (down from 49%). Sweden and Japan see a combined **+5%** boost to their group-winning expectations.
4.  **Goal-Scoring Draw Decay:** Because the Dixon-Coles model simulates scores directly and corrects for draw inflation ($\rho = -0.08$), the average total points per group stage decreased by $0.2$ to $0.3$ points across all groups, reflecting more realistic tournament volatility.
