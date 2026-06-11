"""
Historical World Cup Group Stage Validation.
Calibrated Dixon-Coles Goal Model with s=0.58 Elo Damping and Variable Total Goals.

Source Snapshots from eloratings.net archives:
- 2014 World Cup: June 11, 2014 snapshot (https://www.eloratings.net/2014_World_Cup.tsv)
- 2018 World Cup: June 13, 2018 snapshot (https://www.eloratings.net/2018_World_Cup.tsv)
- 2022 World Cup: November 19, 2022 snapshot (https://www.eloratings.net/2022_World_Cup.tsv)
Note: Host teams receive a +100 Home Field Advantage (HFA) adjustment.
"""

import math
import random
import json
import time

# Set seed for reproducibility
random.seed(42)

# Start-of-tournament Elo ratings from eloratings.net archives
# Calculated as End Rating - Change from the respective tournament TSVs.
elo_ratings = {
    2014: {
        "Brazil": 2138 + 100,  # Host HFA
        "Croatia": 1818,
        "Mexico": 1814,
        "Cameroon": 1606,
        "Spain": 2107,
        "Netherlands": 1985,
        "Chile": 1919,
        "Australia": 1708,
        "Colombia": 1922,
        "Greece": 1823,
        "Ivory Coast": 1772,
        "Japan": 1785,
        "Uruguay": 1918,
        "Costa Rica": 1711,
        "England": 1931,
        "Italy": 1887,
        "Switzerland": 1854,
        "Ecuador": 1836,
        "France": 1896,
        "Honduras": 1668,
        "Argentina": 2018,
        "Bosnia and Herzegovina": 1785,
        "Iran": 1715,
        "Nigeria": 1727,
        "Germany": 2073,
        "Portugal": 1942,
        "Ghana": 1704,
        "United States": 1857,
        "Belgium": 1851,
        "Algeria": 1626,
        "Russia": 1848,
        "South Korea": 1667
    },
    2018: {
        "Russia": 1677 + 100,  # Host HFA
        "Saudi Arabia": 1588,
        "Egypt": 1639,
        "Uruguay": 1893,
        "Portugal": 1968,
        "Spain": 2043,
        "Morocco": 1731,
        "Iran": 1790,
        "France": 1986,
        "Australia": 1743,
        "Peru": 1915,
        "Denmark": 1854,
        "Argentina": 1984,
        "Iceland": 1764,
        "Croatia": 1853,
        "Nigeria": 1681,
        "Brazil": 2141,
        "Switzerland": 1888,
        "Costa Rica": 1742,
        "Serbia": 1788,
        "Germany": 2076,
        "Mexico": 1849,
        "Sweden": 1793,
        "South Korea": 1713,
        "Belgium": 1935,
        "Panama": 1657,
        "Tunisia": 1651,
        "England": 1947,
        "Poland": 1830,
        "Senegal": 1746,
        "Colombia": 1927,
        "Japan": 1684
    },
    2022: {
        "Qatar": 1680 + 100,  # Host HFA
        "Ecuador": 1832,
        "Senegal": 1684,
        "Netherlands": 2040,
        "England": 1919,
        "Iran": 1798,
        "United States": 1796,
        "Wales": 1789,
        "Argentina": 2144,
        "Saudi Arabia": 1636,
        "Mexico": 1808,
        "Poland": 1813,
        "France": 2004,
        "Australia": 1720,
        "Denmark": 1971,
        "Tunisia": 1705,
        "Spain": 1997,
        "Costa Rica": 1743,
        "Germany": 1962,
        "Japan": 1788,
        "Belgium": 2006,
        "Canada": 1775,
        "Morocco": 1764,
        "Croatia": 1926,
        "Brazil": 2133,
        "Serbia": 1899,
        "Switzerland": 1901,
        "Cameroon": 1607,
        "Portugal": 2005,
        "Ghana": 1564,
        "Uruguay": 1935,
        "South Korea": 1786
    }
}

# Group structures for each World Cup
groups_data = {
    2014: {
        "Group A": ["Brazil", "Croatia", "Mexico", "Cameroon"],
        "Group B": ["Spain", "Netherlands", "Chile", "Australia"],
        "Group C": ["Colombia", "Greece", "Ivory Coast", "Japan"],
        "Group D": ["Uruguay", "Costa Rica", "England", "Italy"],
        "Group E": ["Switzerland", "Ecuador", "France", "Honduras"],
        "Group F": ["Argentina", "Bosnia and Herzegovina", "Iran", "Nigeria"],
        "Group G": ["Germany", "Portugal", "Ghana", "United States"],
        "Group H": ["Belgium", "Algeria", "Russia", "South Korea"]
    },
    2018: {
        "Group A": ["Russia", "Saudi Arabia", "Egypt", "Uruguay"],
        "Group B": ["Portugal", "Spain", "Morocco", "Iran"],
        "Group C": ["France", "Australia", "Peru", "Denmark"],
        "Group D": ["Argentina", "Iceland", "Croatia", "Nigeria"],
        "Group E": ["Brazil", "Switzerland", "Costa Rica", "Serbia"],
        "Group F": ["Germany", "Mexico", "Sweden", "South Korea"],
        "Group G": ["Belgium", "Panama", "Tunisia", "England"],
        "Group H": ["Poland", "Senegal", "Colombia", "Japan"]
    },
    2022: {
        "Group A": ["Qatar", "Ecuador", "Senegal", "Netherlands"],
        "Group B": ["England", "Iran", "United States", "Wales"],
        "Group C": ["Argentina", "Saudi Arabia", "Mexico", "Poland"],
        "Group D": ["France", "Australia", "Denmark", "Tunisia"],
        "Group E": ["Spain", "Costa Rica", "Germany", "Japan"],
        "Group F": ["Belgium", "Canada", "Morocco", "Croatia"],
        "Group G": ["Brazil", "Serbia", "Switzerland", "Cameroon"],
        "Group H": ["Portugal", "Ghana", "Uruguay", "South Korea"]
    }
}

# Actual final group standings (ordered 1st, 2nd, 3rd, 4th)
actual_standings = {
    2014: {
        "Group A": ["Brazil", "Mexico", "Croatia", "Cameroon"],
        "Group B": ["Netherlands", "Chile", "Spain", "Australia"],
        "Group C": ["Colombia", "Greece", "Ivory Coast", "Japan"],
        "Group D": ["Costa Rica", "Uruguay", "Italy", "England"],
        "Group E": ["France", "Switzerland", "Ecuador", "Honduras"],
        "Group F": ["Argentina", "Nigeria", "Bosnia and Herzegovina", "Iran"],
        "Group G": ["Germany", "United States", "Portugal", "Ghana"],
        "Group H": ["Belgium", "Algeria", "Russia", "South Korea"]
    },
    2018: {
        "Group A": ["Uruguay", "Russia", "Saudi Arabia", "Egypt"],
        "Group B": ["Spain", "Portugal", "Iran", "Morocco"],
        "Group C": ["France", "Denmark", "Peru", "Australia"],
        "Group D": ["Croatia", "Argentina", "Nigeria", "Iceland"],
        "Group E": ["Brazil", "Switzerland", "Serbia", "Costa Rica"],
        "Group F": ["Sweden", "Mexico", "South Korea", "Germany"],
        "Group G": ["Belgium", "England", "Tunisia", "Panama"],
        "Group H": ["Colombia", "Japan", "Senegal", "Poland"]
    },
    2022: {
        "Group A": ["Netherlands", "Senegal", "Ecuador", "Qatar"],
        "Group B": ["England", "United States", "Iran", "Wales"],
        "Group C": ["Argentina", "Poland", "Mexico", "Saudi Arabia"],
        "Group D": ["France", "Australia", "Tunisia", "Denmark"],
        "Group E": ["Japan", "Spain", "Germany", "Costa Rica"],
        "Group F": ["Morocco", "Croatia", "Belgium", "Canada"],
        "Group G": ["Brazil", "Switzerland", "Cameroon", "Serbia"],
        "Group H": ["Portugal", "South Korea", "Uruguay", "Ghana"]
    }
}

def poisson_pmf(k, mu):
    if mu <= 0:
        return 1.0 if k == 0 else 0.0
    return (mu**k * math.exp(-mu)) / math.factorial(k)

# Memoization cache for Dixon-Coles grid and cumulative weights
_dixon_coles_cache = {}

def sample_dixon_coles(lambda_a, lambda_b, rho=-0.04):
    key = (round(lambda_a, 5), round(lambda_b, 5))
    if key in _dixon_coles_cache:
        options, cumulative_weights = _dixon_coles_cache[key]
    else:
        grid = {}
        total = 0.0
        for x in range(10):
            for y in range(10):
                p = poisson_pmf(x, lambda_a) * poisson_pmf(y, lambda_b)
                if x == 0 and y == 0:
                    p *= (1 - lambda_a * lambda_b * rho)
                elif x == 1 and y == 0:
                    p *= (1 + lambda_b * rho)
                elif x == 0 and y == 1:
                    p *= (1 + lambda_a * rho)
                elif x == 1 and y == 1:
                    p *= (1 - rho)
                
                p = max(0.0, p)
                grid[(x, y)] = p
                total += p
                
        options = list(grid.keys())
        cumulative_weights = []
        cumulative = 0.0
        for opt in options:
            cumulative += grid[opt] / total
            cumulative_weights.append(cumulative)
            
        _dixon_coles_cache[key] = (options, cumulative_weights)
        
    r = random.random()
    for opt, cw in zip(options, cumulative_weights):
        if r < cw:
            return opt
    return options[-1]

def simulate_group(group_teams, elos, n_sims=100000, s=0.58):
    teams = list(group_teams)
    standings_freq = {team: [0, 0, 0, 0] for team in teams}
    total_points = {team: 0 for team in teams}
    
    pairings = [
        (teams[0], teams[1]),
        (teams[2], teams[3]),
        (teams[0], teams[2]),
        (teams[1], teams[3]),
        (teams[0], teams[3]),
        (teams[1], teams[2])
    ]
    
    for _ in range(n_sims):
        points = {team: 0 for team in teams}
        gd = {team: 0 for team in teams}
        gs = {team: 0 for team in teams}
        
        for team_a, team_b in pairings:
            elo_a = elos[team_a]
            elo_b = elos[team_b]
            # (a) Elo damping
            r = 10**((s * (elo_a - elo_b)) / 400.0)
            
            # Variable goals G(d)
            diff = abs(elo_a - elo_b)
            g_d = 2.38364 + 0.0013636 * diff
            
            lambda_b = g_d / (1.0 + r)
            lambda_a = g_d - lambda_b
            
            goals_a, goals_b = sample_dixon_coles(lambda_a, lambda_b)
            
            gs[team_a] += goals_a
            gs[team_b] += goals_b
            gd[team_a] += goals_a - goals_b
            gd[team_b] += goals_b - goals_a
            
            if goals_a > goals_b:
                points[team_a] += 3
            elif goals_a < goals_b:
                points[team_b] += 3
            else:
                points[team_a] += 1
                points[team_b] += 1
                
        shuffled_teams = list(teams)
        random.shuffle(shuffled_teams)
        
        # Tie-breaker key: Points -> GD -> GS -> Elo (resolves all ties)
        sorted_teams = sorted(
            shuffled_teams,
            key=lambda t: (points[t], gd[t], gs[t], elos[t]),
            reverse=True
        )
        
        for rank, team in enumerate(sorted_teams):
            standings_freq[team][rank] += 1
            total_points[team] += points[team]
            
    results = {}
    for team in teams:
        results[team] = {
            "avg_points": total_points[team] / n_sims,
            "1st": standings_freq[team][0] / n_sims,
            "2nd": standings_freq[team][1] / n_sims,
            "3rd": standings_freq[team][2] / n_sims,
            "4th": standings_freq[team][3] / n_sims,
            "qualify": (standings_freq[team][0] + standings_freq[team][1]) / n_sims
        }
    return results

def calculate_brier_score(predictions, actuals):
    bs_sum = 0.0
    for team, p in predictions.items():
        y = actuals[team]
        bs_sum += (p - y) ** 2
    return bs_sum / len(predictions)

def calculate_log_loss(predictions, actuals, eps=1e-15):
    ll_sum = 0.0
    for team, p in predictions.items():
        y = actuals[team]
        p_clipped = max(eps, min(1 - eps, p))
        ll_sum += y * math.log(p_clipped) + (1 - y) * math.log(1 - p_clipped)
    return -ll_sum / len(predictions)

def main():
    n_sims = 100000
    all_results = {}
    
    # Store overall metrics
    year_metrics = {}
    
    global_predicted_qualifiers_correct = 0
    global_predicted_top2_match_count = 0
    global_total_teams = 0
    global_total_groups = 0
    
    all_qualify_preds = {}
    all_qualify_actuals = {}
    
    all_first_preds = {}
    all_first_actuals = {}
    
    print(f"Starting historical World Cup simulations ({n_sims:,} runs, s=0.58)...")
    start_time = time.time()
    
    for year in [2014, 2018, 2022]:
        print(f"Simulating {year} World Cup...")
        all_results[year] = {}
        year_actuals = actual_standings[year]
        year_groups = groups_data[year]
        year_elos = elo_ratings[year]
        
        predicted_qualifiers_correct = 0
        predicted_top2_match_count = 0
        
        year_qualify_preds = {}
        year_qualify_actuals = {}
        year_first_preds = {}
        year_first_actuals = {}
        
        for group_name, teams in year_groups.items():
            sim_res = simulate_group(teams, year_elos, n_sims, s=0.58)
            all_results[year][group_name] = sim_res
            
            actual_order = year_actuals[group_name]
            actual_top2 = actual_order[:2]
            
            # Predict top 2 based on highest simulated qualify probability
            sorted_by_prob = sorted(teams, key=lambda t: sim_res[t]["qualify"], reverse=True)
            predicted_top2 = sorted_by_prob[:2]
            
            # Count correct predicted qualifiers
            for t in teams:
                is_actual_qualifier = 1 if t in actual_top2 else 0
                is_actual_first = 1 if t == actual_order[0] else 0
                
                year_qualify_preds[t] = sim_res[t]["qualify"]
                year_qualify_actuals[t] = is_actual_qualifier
                all_qualify_preds[f"{year}_{t}"] = sim_res[t]["qualify"]
                all_qualify_actuals[f"{year}_{t}"] = is_actual_qualifier
                
                year_first_preds[t] = sim_res[t]["1st"]
                year_first_actuals[t] = is_actual_first
                all_first_preds[f"{year}_{t}"] = sim_res[t]["1st"]
                all_first_actuals[f"{year}_{t}"] = is_actual_first
                
                # Binary classification evaluation with 50% threshold
                if (sim_res[t]["qualify"] > 0.5 and is_actual_qualifier == 1) or (sim_res[t]["qualify"] <= 0.5 and is_actual_qualifier == 0):
                    predicted_qualifiers_correct += 1
                    global_predicted_qualifiers_correct += 1
                    
            # Check how many of the top 2 teams by probability actually qualified
            top2_match = len(set(predicted_top2) & set(actual_top2))
            predicted_top2_match_count += top2_match
            global_predicted_top2_match_count += top2_match
            
            global_total_teams += 4
            global_total_groups += 1
            
        # Compute yearly validation metrics
        year_qualify_brier = calculate_brier_score(year_qualify_preds, year_qualify_actuals)
        year_qualify_loss = calculate_log_loss(year_qualify_preds, year_qualify_actuals)
        
        year_first_brier = calculate_brier_score(year_first_preds, year_first_actuals)
        year_first_loss = calculate_log_loss(year_first_preds, year_first_actuals)
        
        year_metrics[year] = {
            "qualify_brier": year_qualify_brier,
            "qualify_log_loss": year_qualify_loss,
            "first_brier": year_first_brier,
            "first_log_loss": year_first_loss,
            "accuracy_qualifiers_threshold_50": predicted_qualifiers_correct / len(year_elos),
            "correct_qualifiers_top2_predicted": predicted_top2_match_count
        }
        
        print(f"  {year} Metrics:")
        print(f"    Qualify Brier Score: {year_qualify_brier:.4f}")
        print(f"    Qualify Log Loss   : {year_qualify_loss:.4f}")
        print(f"    Qualify Accuracy (>50%): {predicted_qualifiers_correct / len(year_elos) * 100:.1f}%")
        print(f"    Qualifiers Correctly Predicted (Top 2): {predicted_top2_match_count}/16")
        
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\nAll simulations completed in {elapsed:.2f} seconds.")
    
    # Global metrics
    global_qualify_brier = calculate_brier_score(all_qualify_preds, all_qualify_actuals)
    global_qualify_loss = calculate_log_loss(all_qualify_preds, all_qualify_actuals)
    global_first_brier = calculate_brier_score(all_first_preds, all_first_actuals)
    global_first_loss = calculate_log_loss(all_first_preds, all_first_actuals)
    
    overall_metrics = {
        "global_qualify_brier": global_qualify_brier,
        "global_qualify_log_loss": global_qualify_loss,
        "global_first_brier": global_first_brier,
        "global_first_log_loss": global_first_loss,
        "global_accuracy_threshold_50": global_predicted_qualifiers_correct / global_total_teams,
        "global_top2_match_rate": global_predicted_top2_match_count / (global_total_groups * 2),
        "total_predicted_qualifiers_correct": global_predicted_top2_match_count,
        "total_qualifiers": global_total_groups * 2,
        "yearly_breakdown": year_metrics
    }
    
    print("\nGlobal Summary Across 2014, 2018, and 2022:")
    print(f"  Qualify Brier Score: {global_qualify_brier:.4f}")
    print(f"  Qualify Log Loss   : {global_qualify_loss:.4f}")
    print(f"  1st Place Brier Score: {global_first_brier:.4f}")
    print(f"  1st Place Log Loss   : {global_first_loss:.4f}")
    print(f"  Binary Classification Accuracy (>50%): {overall_metrics['global_accuracy_threshold_50'] * 100:.1f}%")
    print(f"  Top 2 Match Rate: {overall_metrics['global_top2_match_rate'] * 100:.1f}% ({global_predicted_top2_match_count}/{global_total_groups * 2})")
    
    # Save simulated outcomes to JSON for the report
    output_data = {
        "metrics": overall_metrics,
        "simulations": all_results,
        "actuals": actual_standings,
        "elos": elo_ratings
    }
    
    with open("research/historical_validation_results.json", "w") as f:
        json.dump(output_data, f, indent=2)
    print("\nSaved simulation results to research/historical_validation_results.json")

if __name__ == "__main__":
    main()
