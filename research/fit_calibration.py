import math
import random
import json
import time

# Host HFA adjustment
HFA = 100

# Ratings Set A: Clean Start-of-Tournament Elos from TSVs
elos_clean = {
    2014: {
        "Brazil": 2138 + HFA,
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
        "Russia": 1677 + HFA,
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
        "Qatar": 1680 + HFA,
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

# Ratings Set B: Auditor-Requested Spot-Check Elos (Brazil=2133, Spain=1997, Argentina=2144)
elos_auditor = {
    2014: elos_clean[2014],
    2018: elos_clean[2018],
    2022: {**elos_clean[2022], "Brazil": 2133, "Spain": 1997, "Argentina": 2144}
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

def simulate_group(group_teams, elos, n_sims=50000, s=1.0, sigma=0.0):
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
        # Draw rating noise once per team per run
        run_elos = {}
        for team in teams:
            noise = random.normalvariate(0, sigma) if sigma > 0 else 0.0
            run_elos[team] = elos[team] + noise
            
        points = {team: 0 for team in run_elos}
        gd = {team: 0 for team in run_elos}
        gs = {team: 0 for team in run_elos}
        
        for team_a, team_b in pairings:
            elo_a = run_elos[team_a]
            elo_b = run_elos[team_b]
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
        
        # Tie-breaker logic (with randomization of unresolved ties)
        sorted_teams = sorted(
            shuffled_teams,
            key=lambda t: (points[t], gd[t], gs[t], run_elos[t]),
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
            "qualify": (standings_freq[team][0] + standings_freq[team][1]) / n_sims
        }
    return results

def calculate_log_loss(predictions, actuals, eps=1e-15):
    ll_sum = 0.0
    for team, p in predictions.items():
        y = actuals[team]
        p_clipped = max(eps, min(1 - eps, p))
        ll_sum += y * math.log(p_clipped) + (1 - y) * math.log(1 - p_clipped)
    return -ll_sum / len(predictions)

def calculate_brier_score(predictions, actuals):
    bs_sum = 0.0
    for team, p in predictions.items():
        y = actuals[team]
        bs_sum += (p - y) ** 2
    return bs_sum / len(predictions)

def evaluate_cross_val(elos_dict, s=1.0, sigma=0.0, n_sims=30000):
    # Folds definitions (leave one out)
    # Fold 1: Test 2014, Train 2018+2022
    # Fold 2: Test 2018, Train 2014+2022
    # Fold 3: Test 2022, Train 2014+2018
    years = [2014, 2018, 2022]
    fold_results = {}
    
    for test_year in years:
        random.seed(42)  # Reset seed per fold for reproducibility
        test_preds = {}
        test_actuals = {}
        test_first_preds = {}
        test_first_actuals = {}
        
        for group_name, teams in groups_data[test_year].items():
            sim_res = simulate_group(teams, elos_dict[test_year], n_sims, s, sigma)
            actual_order = actual_standings[test_year][group_name]
            actual_top2 = actual_order[:2]
            
            for t in teams:
                is_actual_qualifier = 1 if t in actual_top2 else 0
                is_actual_first = 1 if t == actual_order[0] else 0
                test_preds[t] = sim_res[t]["qualify"]
                test_actuals[t] = is_actual_qualifier
                test_first_preds[t] = sim_res[t]["1st"]
                test_first_actuals[t] = is_actual_first
                
        ll = calculate_log_loss(test_preds, test_actuals)
        bs = calculate_brier_score(test_preds, test_actuals)
        fll = calculate_log_loss(test_first_preds, test_first_actuals)
        
        fold_results[test_year] = {
            "qualify_log_loss": ll,
            "qualify_brier": bs,
            "first_log_loss": fll
        }
    return fold_results

def main():
    print("Evaluating Model Damping (a): scale s in [0.5, 0.6, 0.7, 0.8, 1.0]")
    for elo_name, elos in [("Clean", elos_clean), ("Auditor", elos_auditor)]:
        print(f"\n--- Ratings: {elo_name} ---")
        for s in [0.5, 0.55, 0.58, 0.6, 0.65, 0.7, 0.8, 1.0]:
            res = evaluate_cross_val(elos, s=s, sigma=0.0, n_sims=30000)
            avg_ll = sum(res[y]["qualify_log_loss"] for y in res) / 3
            avg_fll = sum(res[y]["first_log_loss"] for y in res) / 3
            print(f"s={s:.2f} -- 2014: {res[2014]['qualify_log_loss']:.4f}, 2018: {res[2018]['qualify_log_loss']:.4f}, 2022: {res[2022]['qualify_log_loss']:.4f} -- Avg LL: {avg_ll:.4f}, Avg 1st LL: {avg_fll:.4f}")

    print("\nEvaluating Rating Uncertainty (b): sigma in [20, 40, 50, 60, 80]")
    for elo_name, elos in [("Clean", elos_clean), ("Auditor", elos_auditor)]:
        print(f"\n--- Ratings: {elo_name} ---")
        for sigma in [0.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0]:
            res = evaluate_cross_val(elos, s=1.0, sigma=sigma, n_sims=30000)
            avg_ll = sum(res[y]["qualify_log_loss"] for y in res) / 3
            avg_fll = sum(res[y]["first_log_loss"] for y in res) / 3
            print(f"sigma={sigma:.1f} -- 2014: {res[2014]['qualify_log_loss']:.4f}, 2018: {res[2018]['qualify_log_loss']:.4f}, 2022: {res[2022]['qualify_log_loss']:.4f} -- Avg LL: {avg_ll:.4f}, Avg 1st LL: {avg_fll:.4f}")

if __name__ == "__main__":
    main()
