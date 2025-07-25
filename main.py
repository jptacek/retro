import os
import re


def parse_play(play_string):
    """
    Parses a Retrosheet play notation string and returns a
    human-readable description.
    This is a simplified parser and does not handle all Retrosheet notations.
    """
    # Basic plays
    if re.match(r'^[1-9]$', play_string):
        return f"Ground out to position {play_string}"
    if re.match(r'^S[1-9]?', play_string):
        return "Single"
    if re.match(r'^D[1-9]?', play_string):
        return "Double"
    if re.match(r'^T[1-9]?', play_string):
        return "Triple"
    if re.match(r'^HR', play_string):
        return "Home Run"
    if re.match(r'^W', play_string):
        return "Walk"
    if re.match(r'^K', play_string):
        return "Strikeout"
    if re.match(r'^E[1-9]', play_string):
        return f"Error by fielder in position {play_string[1]}"

    # More complex plays
    if "DP" in play_string or "TP" in play_string:
        return "Double Play" if "DP" in play_string else "Triple Play"
    if "SB" in play_string:
        return "Stolen Base"
    if "CS" in play_string:
        return "Caught Stealing"
    if "SH" in play_string:
        return "Sacrifice Hit (Bunt)"
    if "SF" in play_string:
        return "Sacrifice Fly"
    if "HP" in play_string:
        return "Hit by Pitch"
    if "IW" in play_string:
        return "Intentional Walk"

    # Default for unhandled plays
    return play_string


def get_player_name(player_id, rosters):
    """Gets a player's name from their ID."""
    for team_roster in rosters.values():
        if player_id in team_roster:
            return team_roster[player_id]['name']
    return player_id


def process_game_file(game_file_path, rosters, teams):
    """Processes a single game file and writes individual game files."""
    with open(game_file_path, 'r') as f:
        game_data = f.readlines()

    games = []
    current_game = None

    for line in game_data:
        parts = line.strip().split(',')
        if parts[0] == 'id':
            if current_game:
                games.append(current_game)
            current_game = {
                'id': parts[1],
                'home_team': '',
                'visiting_team': '',
                'date': '',
                'home_score': 0,
                'visiting_score': 0,
                'current_inning': 0,
                'plays': []
            }
        elif parts[0] == 'info' and current_game:
            if parts[1] == 'hometeam':
                current_game['home_team'] = parts[2]
            elif parts[1] == 'visteam':
                current_game['visiting_team'] = parts[2]
            elif parts[1] == 'date':
                current_game['date'] = parts[2]
        elif parts[0] == 'play' and current_game:
            inning = parts[1]
            team_flag = int(parts[2])
            player_id = parts[3]
            play_string = parts[6]
            
            if int(inning) > current_game['current_inning']:
                current_game['current_inning'] = int(inning)
                inning_text = f"\nInning {current_game['current_inning']}"
                current_game['plays'].append(inning_text)
            
            player_name = get_player_name(player_id, rosters)
            if team_flag == 1:
                team_name = teams[current_game['home_team']]['name']
            else:
                team_name = teams[current_game['visiting_team']]['name']
            description = parse_play(play_string)
            
            # Simplified score tracking
            if 'H' in play_string or 'HR' in play_string:
                runs = play_string.count('H')
                if team_flag == 1:
                    current_game['home_score'] += runs
                else:
                    current_game['visiting_score'] += runs

            play_entry = f"{team_name}: {player_name} - {description}"
            current_game['plays'].append(play_entry)

    if current_game:
        games.append(current_game)

    # Write individual game files
    for game in games:
        write_game_file(game, teams)


def write_game_file(game, teams):
    """Writes a single game to its own file in the appropriate directory."""
    home_team = game['home_team']
    visiting_team = game['visiting_team']
    date = game['date']
    year = date[:4] if date else '1975'
    
    # Format date for filename (YYYYMMDD) - replace slashes with nothing
    if date:
        date_str = date.replace('/', '')
    else:
        date_str = 'unknown'
    
    # Create directories for both teams
    for team_id in [home_team, visiting_team]:
        team_dir = os.path.join('game_log', team_id, year)
        os.makedirs(team_dir, exist_ok=True)
        
        # Determine opponent
        opponent = visiting_team if team_id == home_team else home_team
        
        # Create filename
        filename = f"{date_str}_vs_{opponent}.txt"
        filepath = os.path.join(team_dir, filename)
        
        # Write game file
        with open(filepath, 'w') as f:
            f.write(f"--- {game['id']} ---\n")
            f.write(f"Date: {date}\n")
            f.write(f"Home: {teams[home_team]['name']}\n")
            f.write(f"Visiting: {teams[visiting_team]['name']}\n\n")
            
            for play in game['plays']:
                f.write(f"{play}\n")
            
            final_score = (
                f"\nFinal Score: {teams[visiting_team]['name']} "
                f"{game['visiting_score']}, {teams[home_team]['name']} "
                f"{game['home_score']}\n"
            )
            f.write(final_score)


def load_rosters(data_dir):
    """Loads all team rosters from .ROS files."""
    rosters = {}
    for filename in os.listdir(data_dir):
        if filename.endswith(".ROS"):
            team_id = filename.split('.')[0][:3]
            rosters[team_id] = {}
            roster_path = os.path.join(data_dir, filename)
            with open(roster_path, 'r', encoding='latin-1') as f:
                for line in f:
                    parts = line.strip().split(',')
                    player_id = parts[0]
                    last_name = parts[1]
                    first_name = parts[2]
                    player_name = f"{first_name} {last_name}"
                    rosters[team_id][player_id] = {'name': player_name}
    return rosters


def load_teams(data_dir):
    """Loads team information."""
    teams = {}
    with open(os.path.join(data_dir, 'TEAM1975'), 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            team_id, _, city, name = parts[0], parts[1], parts[2], parts[3]
            teams[team_id] = {'city': city, 'name': name}
    return teams


def main():
    data_dir = 'data/1975eve'
    rosters = load_rosters(data_dir)
    teams = load_teams(data_dir)

    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith((".EVN", ".EVA")):
            game_file_path = os.path.join(data_dir, filename)
            process_game_file(game_file_path, rosters, teams)


if __name__ == "__main__":
    main()
