import csv
import urllib.request

HFA = 100

elos = {
    2014: {
        "Brazil": 2138 + HFA, "Croatia": 1818, "Mexico": 1814, "Cameroon": 1606,
        "Spain": 2107, "Netherlands": 1985, "Chile": 1919, "Australia": 1708,
        "Colombia": 1922, "Greece": 1823, "Ivory Coast": 1772, "Japan": 1785,
        "Uruguay": 1918, "Costa Rica": 1711, "England": 1931, "Italy": 1887,
        "Switzerland": 1854, "Ecuador": 1836, "France": 1896, "Honduras": 1668,
        "Argentina": 2018, "Bosnia and Herzegovina": 1785, "Iran": 1715, "Nigeria": 1727,
        "Germany": 2073, "Portugal": 1942, "Ghana": 1704, "United States": 1857,
        "Belgium": 1851, "Algeria": 1626, "Russia": 1848, "South Korea": 1667
    },
    2018: {
        "Russia": 1677 + HFA, "Saudi Arabia": 1588, "Egypt": 1639, "Uruguay": 1893,
        "Portugal": 1968, "Spain": 2043, "Morocco": 1731, "Iran": 1790,
        "France": 1986, "Australia": 1743, "Peru": 1915, "Denmark": 1854,
        "Argentina": 1984, "Iceland": 1764, "Croatia": 1853, "Nigeria": 1681,
        "Brazil": 2141, "Switzerland": 1888, "Costa Rica": 1742, "Serbia": 1788,
        "Germany": 2076, "Mexico": 1849, "Sweden": 1793, "South Korea": 1713,
        "Belgium": 1935, "Panama": 1657, "Tunisia": 1651, "England": 1947,
        "Poland": 1830, "Senegal": 1746, "Colombia": 1927, "Japan": 1684
    },
    2022: {
        "Qatar": 1680 + HFA, "Ecuador": 1832, "Senegal": 1684, "Netherlands": 2040,
        "England": 1919, "Iran": 1798, "United States": 1796, "Wales": 1789,
        "Argentina": 2144, "Saudi Arabia": 1636, "Mexico": 1808, "Poland": 1813,
        "France": 2004, "Australia": 1720, "Denmark": 1971, "Tunisia": 1705,
        "Spain": 1997, "Costa Rica": 1743, "Germany": 1962, "Japan": 1788,
        "Belgium": 2006, "Canada": 1775, "Morocco": 1764, "Croatia": 1926,
        "Brazil": 2133, "Serbia": 1899, "Switzerland": 1901, "Cameroon": 1607,
        "Portugal": 2005, "Ghana": 1564, "Uruguay": 1935, "South Korea": 1786
    }
}

# Mapping of team names in Fjelstul database -> elos dictionary keys
name_mapping = {
    "Bosnia-Herzegovina": "Bosnia and Herzegovina",
    "Côte d'Ivoire": "Ivory Coast",
    "Korea Republic": "South Korea",
    "United States": "United States",
}

def clean_name(name):
    return name_mapping.get(name, name)

def main():
    url = "https://raw.githubusercontent.com/jfjelstul/worldcup/master/data-csv/matches.csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        lines = response.read().decode("utf-8").splitlines()
        
    reader = csv.DictReader(lines)
    
    total_goals_sum = 0
    match_count = 0
    
    data_points = []
    
    for row in reader:
        tourn_id = row["tournament_id"]
        stage = row["stage_name"]
        
        if tourn_id in ["WC-2014", "WC-2018", "WC-2022"] and stage == "group stage":
            year = int(tourn_id.split("-")[1])
            home_raw = row["home_team_name"]
            away_raw = row["away_team_name"]
            
            home_team = clean_name(home_raw)
            away_team = clean_name(away_raw)
            
            home_score = int(row["home_team_score"])
            away_score = int(row["away_team_score"])
            
            # Lookup Elos
            year_elos = elos[year]
            if home_team not in year_elos:
                print(f"ERROR: {home_team} not found in {year} Elos")
                continue
            if away_team not in year_elos:
                print(f"ERROR: {away_team} not found in {year} Elos")
                continue
                
            elo_a = year_elos[home_team]
            elo_b = year_elos[away_team]
            
            diff = abs(elo_a - elo_b)
            tot_goals = home_score + away_score
            
            data_points.append((diff, tot_goals))
            total_goals_sum += tot_goals
            match_count += 1
            
    print(f"Processed {match_count} group stage matches.")
    print(f"Average goals per match: {total_goals_sum / match_count:.4f}")
    
    # Simple linear regression to find G(d) = G0 + k * |d|
    n = len(data_points)
    sum_x = sum(pt[0] for pt in data_points)
    sum_y = sum(pt[1] for pt in data_points)
    sum_xx = sum(pt[0]**2 for pt in data_points)
    sum_xy = sum(pt[0]*pt[1] for pt in data_points)
    
    # slope k
    k = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    # intercept G0
    G0 = (sum_y - k * sum_x) / n
    
    print(f"\nLinear fit: G(d) = {G0:.5f} + {k:.7f} * |d|")
    
    # Let's print some sample values
    for test_d in [0, 100, 200, 300, 400, 500]:
        print(f"  d={test_d:3d} -> Expected total goals: {G0 + k*test_d:.4f}")

if __name__ == "__main__":
    main()
