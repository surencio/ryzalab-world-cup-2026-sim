import math
import random
import json

# Set seed for reproducibility
random.seed(42)

# Define the groups and their teams with base ratings
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

def simulate_group(group_name_or_teams, group_teams=None, n_sims=100000):
    """
    Simulates a group independently. Kept for backward compatibility with audit scripts.
    """
    if isinstance(group_name_or_teams, dict):
        group_teams_dict = group_name_or_teams
        group_name = "Group X"
    else:
        group_name = group_name_or_teams
        group_teams_dict = group_teams
        
    teams = list(group_teams_dict.keys())
    standings_freq = {team: [0, 0, 0, 0] for team in teams}
    total_points = {team: 0 for team in teams}
    pairings = get_group_pairings(group_name, teams)
    
    for _ in range(n_sims):
        points = {team: 0 for team in teams}
        gd = {team: 0 for team in teams}
        gs = {team: 0 for team in teams}
        team_u = {team: random.random() for team in teams}
        
        for team_a, team_b, rd in pairings:
            elo_a, elo_b = get_match_ratings(team_a, team_b, rd, group_teams_dict, team_u)
            # Damping s=0.58
            r = 10**((0.58 * (elo_a - elo_b)) / 400.0)
            
            # Variable goals G(d)
            diff = abs(elo_a - elo_b)
            g_d = 2.37943 + 0.001373 * diff
            
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
        
        sorted_teams = sorted(
            shuffled_teams, 
            key=lambda t: (points[t], gd[t], gs[t], get_base_elo(t, group_teams_dict)), 
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

def simulate_tournament(n_sims=100000):
    """
    Simulates all 12 groups jointly to correctly evaluate best-third-place advancement.
    """
    all_teams = []
    team_to_group = {}
    for g_name, g_teams in groups.items():
        for t in g_teams:
            all_teams.append(t)
            team_to_group[t] = g_name

    standings_freq = {team: [0, 0, 0, 0] for team in all_teams}
    total_points = {team: 0 for team in all_teams}
    r32_adv_count = {team: 0 for team in all_teams}

    for _ in range(n_sims):
        third_place_teams = []
        direct_qualifiers = set()
        
        # Simulate each of the 12 groups
        for group_name, group_teams in groups.items():
            teams = list(group_teams.keys())
            pairings = get_group_pairings(group_name, teams)
            
            points = {team: 0 for team in teams}
            gd = {team: 0 for team in teams}
            gs = {team: 0 for team in teams}
            
            # Single uniform random variable per team per run for monotone coupling
            team_u = {team: random.random() for team in teams}
            
            for team_a, team_b, rd in pairings:
                elo_a, elo_b = get_match_ratings(team_a, team_b, rd, group_teams, team_u)
                r = 10**((0.58 * (elo_a - elo_b)) / 400.0)
                
                # Variable goals G(d)
                diff = abs(elo_a - elo_b)
                g_d = 2.37943 + 0.001373 * diff
                
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
            
            sorted_teams = sorted(
                shuffled_teams,
                key=lambda t: (points[t], gd[t], gs[t], get_base_elo(t, group_teams)),
                reverse=True
            )
            
            # Group standing frequencies
            for rank, team in enumerate(sorted_teams):
                standings_freq[team][rank] += 1
                total_points[team] += points[team]
                
            # 1st & 2nd place qualify directly
            direct_qualifiers.add(sorted_teams[0])
            direct_qualifiers.add(sorted_teams[1])
            
            # 3rd place team goes to wild-card pool
            t3 = sorted_teams[2]
            third_place_teams.append({
                "team": t3,
                "points": points[t3],
                "gd": gd[t3],
                "gs": gs[t3]
            })

        # Rank the 12 third-place teams: points -> GD -> GS -> random tie-breaker.
        ranked_thirds = sorted(
            third_place_teams,
            key=lambda x: (x["points"], x["gd"], x["gs"], random.random()),
            reverse=True
        )
        
        # Top 8 advance
        advancing_thirds = set(item["team"] for item in ranked_thirds[:8])
        
        # Accumulate advancement
        for team in direct_qualifiers:
            r32_adv_count[team] += 1
        for team in advancing_thirds:
            r32_adv_count[team] += 1

    results = {}
    for group_name, group_teams in groups.items():
        results[group_name] = {}
        for team in group_teams.keys():
            results[group_name][team] = {
                "avg_points": total_points[team] / n_sims,
                "1st": standings_freq[team][0] / n_sims,
                "2nd": standings_freq[team][1] / n_sims,
                "3rd": standings_freq[team][2] / n_sims,
                "4th": standings_freq[team][3] / n_sims,
                "r32_adv": r32_adv_count[team] / n_sims
            }
    return results

if __name__ == "__main__":
    # Fix seed for run reproducibility
    random.seed(42)
    
    # Run 100,000 simulations
    all_results = simulate_tournament(n_sims=100000)
    print(json.dumps(all_results, indent=2))
