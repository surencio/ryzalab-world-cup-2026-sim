import math
import random
import json

# Set seed for reproducibility
random.seed(42)

# Define the groups and their teams with base and adjusted Elo ratings
# Format: {Group: {Team: (base_elo, adjusted_elo)}}
groups = {
    "Group A": {
        "Mexico": (1810, 1910),  # +100 Host HFA
        "South Korea": (1800, 1800),
        "Czechia": (1790, 1840),  # +50 Schick return
        "South Africa": (1700, 1700)
    },
    "Group B": {
        "Switzerland": (1900, 1900),
        "Canada": (1780, 1880),  # +100 Host HFA (dropped Davies injury penalty as it is already priced into base rating)
        "Bosnia & Herzegovina": (1730, 1730),
        "Qatar": (1720, 1720)
    },
    "Group C": {
        "Morocco": (1920, 1920),
        "Brazil": (2020, 1920),  # -100 Neymar, Rodrygo, Militao, Estevao injuries
        "Scotland": (1770, 1740),  # -30 Gilmour injury
        "Haiti": (1550, 1550)
    },
    "Group D": {
        "United States": (1840, 1980),  # +100 Host HFA + 40 Adams return
        "Türkiye": (1810, 1810),
        "Australia": (1770, 1770),
        "Paraguay": (1750, 1750)
    },
    "Group E": {
        "Germany": (1970, 1935),  # -35 Gnabry, Ter Stegen injuries
        "Ecuador": (1850, 1850),
        "Ivory Coast": (1780, 1780),
        "Curaçao": (1560, 1560)
    },
    "Group F": {
        "Netherlands": (1980, 1885),  # -50 Simons, -10 De Ligt, -35 Timber injuries
        "Sweden": (1830, 1830),
        "Japan": (1880, 1820),  # -60 Mitoma injury
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
        "England": (2050, 2040),  # -10 Saka injury precaution
        "Croatia": (1930, 1930),
        "Panama": (1710, 1710),
        "Ghana": (1710, 1690)  # -20 Kudus partial injury / potential game 3 return
    }
}

def get_match_probs(elo_a, elo_b):
    d = elo_a - elo_b
    expected_score_a = 1.0 / (1.0 + 10**(-d / 400.0))
    # Draw probability using logistic decay curve
    p_draw = 1.0 / (1.0 + math.exp(1.1 + 0.0035 * abs(d)))
    p_win_a = expected_score_a - 0.5 * p_draw
    p_win_b = 1.0 - expected_score_a - 0.5 * p_draw
    
    # Clip to avoid floating point errors
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

def simulate_group(group_teams, n_sims=10000):
    teams = list(group_teams.keys())
    # Track standings frequencies
    standings_freq = {team: [0, 0, 0, 0] for team in teams}
    total_points = {team: 0 for team in teams}
    
    # Generate all match pairings
    pairings = []
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            pairings.append((teams[i], teams[j]))
            
    for _ in range(n_sims):
        points = {team: 0 for team in teams}
        for team_a, team_b in pairings:
            elo_a = group_teams[team_a][1]
            elo_b = group_teams[team_b][1]
            p_win, p_draw, p_loss = get_match_probs(elo_a, elo_b)
            
            outcome = random_choice(['win', 'draw', 'loss'], [p_win, p_draw, p_loss])
            if outcome == 'win':
                points[team_a] += 3
            elif outcome == 'draw':
                points[team_a] += 1
                points[team_b] += 1
            else:
                points[team_b] += 3
                
        # Shuffle teams to randomize ties at all levels (points, Elo)
        shuffled_teams = list(teams)
        random.shuffle(shuffled_teams)
        # Stable sort on points and adjusted Elo rating
        sorted_teams = sorted(shuffled_teams, key=lambda t: (points[t], group_teams[t][1]), reverse=True)
        for rank, team in enumerate(sorted_teams):
            standings_freq[team][rank] += 1
            total_points[team] += points[team]
            
    # Calculate probabilities
    results = {}
    for team in teams:
        results[team] = {
            "avg_points": total_points[team] / n_sims,
            "1st": standings_freq[team][0] / n_sims,
            "2nd": standings_freq[team][1] / n_sims,
            "3rd": standings_freq[team][2] / n_sims,
            "4th": standings_freq[team][3] / n_sims,
            "base_elo": group_teams[team][0],
            "adj_elo": group_teams[team][1]
        }
    return results

all_results = {}
for group_name, group_teams in groups.items():
    all_results[group_name] = simulate_group(group_teams)

# Output results in a structured format
print(json.dumps(all_results, indent=2))
