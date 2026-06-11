import math
import random
import json

# Set seed for reproducibility
random.seed(42)

# Define the groups and their teams with base ratings
# In this model, some teams have stochastic roster hazards
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
        "Canada": (1780, 1880),  # Base Elo 1880, stochastic Davies -30
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
        "Netherlands": (1980, 1885),
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
        "Ghana": (1710, 1690)  # Base Elo 1710, stochastic Kudus -40
    }
}

def poisson_pmf(k, mu):
    if mu <= 0:
        return 1.0 if k == 0 else 0.0
    return (mu**k * math.exp(-mu)) / math.factorial(k)

def sample_dixon_coles(lambda_a, lambda_b, rho=-0.08):
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
    
    r = random.random()
    cumulative = 0.0
    for opt, w in zip(options, weights):
        cumulative += w
        if r < cumulative:
            return opt
    return options[-1]

def get_match_ratings(team_a, team_b, round_idx, group_teams):
    def get_team_elo(team, rd):
        base, old_adj = group_teams[team]
        # Set base Elo correctly for teams with stochastic rosters
        if team == "Brazil":
            current_base = 1980
        elif team == "Canada":
            current_base = 1880
        elif team == "England":
            current_base = 2050
        elif team == "Ghana":
            current_base = 1710
        else:
            current_base = old_adj
            
        # Sample player availability
        if team in stochastic_rosters:
            player, probs, deduction = stochastic_rosters[team]
            prob_available = probs[rd]
            if random.random() > prob_available:
                return current_base - deduction
        return current_base

    return get_team_elo(team_a, round_idx), get_team_elo(team_b, round_idx)

def simulate_group(group_teams, n_sims=10000):
    teams = list(group_teams.keys())
    standings_freq = {team: [0, 0, 0, 0] for team in teams}
    total_points = {team: 0 for team in teams}
    
    # R1: 0-1, 2-3
    # R2: 0-2, 1-3
    # R3: 0-3, 1-2
    pairings = [
        (teams[0], teams[1], 0),
        (teams[2], teams[3], 0),
        (teams[0], teams[2], 1),
        (teams[1], teams[3], 1),
        (teams[0], teams[3], 2),
        (teams[1], teams[2], 2)
    ]
    
    for _ in range(n_sims):
        points = {team: 0 for team in teams}
        gd = {team: 0 for team in teams}
        gs = {team: 0 for team in teams}
        
        for team_a, team_b, rd in pairings:
            elo_a, elo_b = get_match_ratings(team_a, team_b, rd, group_teams)
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
        
        # Sort based on Points, GD, GS, and Elo
        sorted_teams = sorted(
            shuffled_teams, 
            key=lambda t: (points[t], gd[t], gs[t], group_teams[t][1]), 
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

if __name__ == "__main__":
    all_results = {}
    for group_name, group_teams in groups.items():
        all_results[group_name] = simulate_group(group_teams)
        
    print(json.dumps(all_results, indent=2))
