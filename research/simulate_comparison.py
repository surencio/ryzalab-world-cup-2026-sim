import math
import random
import json

# Set seed for reproducibility
random.seed(42)

# Define the groups and their teams with base ratings
# In the new model, some teams have stochastic roster hazards
# Format: {Team: (base_elo, {player_name: (probs, deduction)})}
stochastic_rosters = {
    "Brazil": ("Neymar", [0.15, 0.50, 0.75], 60),  # Base Elo is 1980 (2020 - 40 permanent injuries)
    "Canada": ("Davies", [0.40, 0.75, 0.90], 30),  # Base Elo is 1880 (1780 + 100 HFA)
    "England": ("Saka", [0.70, 0.90, 0.95], 10),   # Base Elo is 2050
    "Ghana": ("Kudus", [0.10, 0.40, 0.85], 40)     # Base Elo is 1710
}

groups = {
    "Group A": {
        "Mexico": (1810, 1910),  # +100 HFA
        "South Korea": (1800, 1800),
        "Czechia": (1790, 1840),  # +50 Schick return
        "South Africa": (1700, 1700)
    },
    "Group B": {
        "Switzerland": (1900, 1900),
        "Canada": (1780, 1850),  # Base Elo 1880, stochastic Davies -30
        "Bosnia & Herzegovina": (1730, 1730),
        "Qatar": (1720, 1720)
    },
    "Group C": {
        "Morocco": (1920, 1920),
        "Brazil": (2020, 1920),  # Base Elo 1980, stochastic Neymar -60
        "Scotland": (1770, 1740),
        "Haiti": (1550, 1550)
    },
    "Group D": {
        "United States": (1840, 1980),  # +100 HFA + 40 Adams return
        "Türkiye": (1810, 1810),
        "Australia": (1770, 1770),
        "Paraguay": (1750, 1750)
    },
    "Group E": {
        "Germany": (1970, 1935),
        "Ecuador": (1850, 1850),
        "Ivory Coast": (1780, 1780),
        "Curaçao": (1560, 1560)
    },
    "Group F": {
        "Netherlands": (1980, 1920),
        "Sweden": (1830, 1830),
        "Japan": (1880, 1820),
        "Tunisia": (1740, 1740)
    },
    "Group G": {
        "Belgium": (1960, 1960),
        "Iran": (1800, 1800),
        "Egypt": (1760, 1760),
        "New Zealand": (1570, 1570)
    },
    "Group H": {
        "Spain": (2150, 2150),
        "Uruguay": (2000, 2000),
        "Saudi Arabia": (1710, 1710),
        "Cape Verde": (1630, 1630)
    },
    "Group I": {
        "France": (2110, 2110),
        "Norway": (1830, 1830),
        "Senegal": (1820, 1820),
        "Iraq": (1690, 1690)
    },
    "Group J": {
        "Argentina": (2130, 2130),
        "Austria": (1840, 1840),
        "Algeria": (1750, 1750),
        "Jordan": (1680, 1680)
    },
    "Group K": {
        "Portugal": (2030, 2030),
        "Colombia": (2010, 2010),
        "Uzbekistan": (1730, 1730),
        "DR Congo": (1710, 1710)
    },
    "Group L": {
        "England": (2050, 2040),  # Base Elo 2050, stochastic Saka -10
        "Croatia": (1930, 1930),
        "Panama": (1710, 1710),
        "Ghana": (1710, 1670)  # Base Elo 1710, stochastic Kudus -40
    }
}

# Helper for standard & real World Cup group fixture order
def get_group_pairings(group_name, teams):
    default_pairings = [
        (teams[0], teams[1], 0),
        (teams[2], teams[3], 0),
        (teams[0], teams[2], 1),
        (teams[1], teams[3], 1),
        (teams[0], teams[3], 2),
        (teams[1], teams[2], 2)
    ]
    
    if group_name == "Group B":
        # Switzerland (0), Canada (1), Bosnia (2), Qatar (3)
        # R1: Canada vs Bosnia, Switzerland vs Qatar
        # R2: Canada vs Qatar, Switzerland vs Bosnia
        # R3: Canada vs Switzerland, Bosnia vs Qatar
        return [
            (teams[1], teams[2], 0),
            (teams[0], teams[3], 0),
            (teams[1], teams[3], 1),
            (teams[0], teams[2], 1),
            (teams[1], teams[0], 2),
            (teams[2], teams[3], 2)
        ]
    elif group_name == "Group C":
        # Morocco (0), Brazil (1), Scotland (2), Haiti (3)
        # R1: Brazil vs Morocco, Scotland vs Haiti
        # R2: Brazil vs Haiti, Morocco vs Scotland
        # R3: Brazil vs Scotland, Morocco vs Haiti
        return [
            (teams[1], teams[0], 0),
            (teams[2], teams[3], 0),
            (teams[1], teams[3], 1),
            (teams[0], teams[2], 1),
            (teams[1], teams[2], 2),
            (teams[0], teams[3], 2)
        ]
    elif group_name == "Group L":
        # England (0), Croatia (1), Panama (2), Ghana (3)
        # R1: England vs Croatia, Panama vs Ghana
        # R2: England vs Ghana, Croatia vs Panama
        # R3: England vs Panama, Croatia vs Ghana
        return [
            (teams[0], teams[1], 0),
            (teams[2], teams[3], 0),
            (teams[0], teams[3], 1),
            (teams[1], teams[2], 1),
            (teams[0], teams[2], 2),
            (teams[1], teams[3], 2)
        ]
    
    return default_pairings

def get_base_elo(team, group_teams):
    if team == "Brazil":
        return 1980
    elif team == "Canada":
        return 1880
    elif team == "England":
        return 2050
    elif team == "Ghana":
        return 1710
    elif team == "Netherlands":
        return 1885
    else:
        return group_teams[team][1]

# ----------------- OLD MODEL SIMULATION (100k runs) -----------------
def get_match_probs_old(elo_a, elo_b):
    d = elo_a - elo_b
    expected_score_a = 1.0 / (1.0 + 10**(-d / 400.0))
    p_draw = 1.0 / (1.0 + math.exp(1.1 + 0.0035 * abs(d)))
    p_win_a = expected_score_a - 0.5 * p_draw
    p_win_b = 1.0 - expected_score_a - 0.5 * p_draw
    
    p_win_a = max(0.0, p_win_a)
    p_win_b = max(0.0, p_win_b)
    total = p_win_a + p_win_b + p_draw
    return p_win_a / total, p_draw / total, p_win_b / total

def random_choice(options, weights):
    r = random.random()
    cumulative = 0.0
    for option, weight in zip(options, weights):
        cumulative += weight
        if r < cumulative:
            return option
    return options[-1]

def simulate_group_old(group_name, group_teams, n_sims=100000):
    teams = list(group_teams.keys())
    standings_freq = {team: [0, 0, 0, 0] for team in teams}
    total_points = {team: 0 for team in teams}
    pairings = get_group_pairings(group_name, teams)
            
    for _ in range(n_sims):
        points = {team: 0 for team in teams}
        for team_a, team_b, rd in pairings:
            elo_a = group_teams[team_a][1]
            elo_b = group_teams[team_b][1]
            p_win, p_draw, p_loss = get_match_probs_old(elo_a, elo_b)
            
            outcome = random_choice(['win', 'draw', 'loss'], [p_win, p_draw, p_loss])
            if outcome == 'win':
                points[team_a] += 3
            elif outcome == 'draw':
                points[team_a] += 1
                points[team_b] += 1
            else:
                points[team_b] += 3
                
        shuffled_teams = list(teams)
        random.shuffle(shuffled_teams)
        sorted_teams = sorted(shuffled_teams, key=lambda t: (points[t], group_teams[t][1]), reverse=True)
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
        }
    return results

# ----------------- NEW DIXON-COLES + STOCHASTIC MODEL (100k runs + cache) -----------------
def poisson_pmf(k, mu):
    if mu <= 0:
        return 1.0 if k == 0 else 0.0
    return (mu**k * math.exp(-mu)) / math.factorial(k)

# Memoization cache for Dixon-Coles grid and weights
_dixon_coles_cache = {}

def sample_dixon_coles(lambda_a, lambda_b, rho=-0.04):
    key = (round(lambda_a, 5), round(lambda_b, 5))
    if key in _dixon_coles_cache:
        options, weights = _dixon_coles_cache[key]
    else:
        grid = {}
        total = 0.0
        for x in range(10):
            for y in range(10):
                p = poisson_pmf(x, lambda_a) * poisson_pmf(y, lambda_b)
                # Dixon-Coles adjustment
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
        weights = [grid[opt] / total for opt in options]
        _dixon_coles_cache[key] = (options, weights)
        
    r = random.random()
    cumulative = 0.0
    for opt, w in zip(options, weights):
        cumulative += w
        if r < cumulative:
            return opt
    return options[-1]

def get_match_ratings(team_a, team_b, round_idx, group_teams, team_u=None):
    def get_team_elo(team, rd):
        base_elo = get_base_elo(team, group_teams)
        if team in stochastic_rosters:
            player, probs, deduction = stochastic_rosters[team]
            prob_available = probs[rd]
            u = team_u[team] if team_u is not None else random.random()
            if u > prob_available:
                return base_elo - deduction
        return base_elo

    return get_team_elo(team_a, round_idx), get_team_elo(team_b, round_idx)

def simulate_group_new(group_name, group_teams, n_sims=100000):
    teams = list(group_teams.keys())
    standings_freq = {team: [0, 0, 0, 0] for team in teams}
    total_points = {team: 0 for team in teams}
    pairings = get_group_pairings(group_name, teams)
    
    for _ in range(n_sims):
        points = {team: 0 for team in teams}
        gd = {team: 0 for team in teams}
        gs = {team: 0 for team in teams}
        team_u = {team: random.random() for team in teams}
        
        for team_a, team_b, rd in pairings:
            elo_a, elo_b = get_match_ratings(team_a, team_b, rd, group_teams, team_u)
            r = 10**((elo_a - elo_b) / 400.0)
            lambda_b = 2.5 / (1.0 + r)
            lambda_a = 2.5 - lambda_b
            
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
        
        sorted_teams = sorted(
            shuffled_teams, 
            key=lambda t: (points[t], gd[t], gs[t], get_base_elo(t, group_teams)), 
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
        }
    return results

# Run both simulations and compile comparison
comparison = {}
for group_name, group_teams in groups.items():
    old_results = simulate_group_old(group_name, group_teams)
    new_results = simulate_group_new(group_name, group_teams)
    
    comparison[group_name] = {}
    for team in group_teams.keys():
        comparison[group_name][team] = {
            "old": old_results[team],
            "new": new_results[team],
            "shift_1st": new_results[team]["1st"] - old_results[team]["1st"],
            "shift_points": new_results[team]["avg_points"] - old_results[team]["avg_points"]
        }

# Write comparison to file
with open("research/comparison_results.json", "w") as f:
    json.dump(comparison, f, indent=2)

print(json.dumps(comparison, indent=2))
