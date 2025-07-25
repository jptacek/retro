import os
import datetime
from collections import defaultdict
import random


class RadioBroadcastReporter:
    """Radio broadcast-style game reporter that creates exciting play-by-play commentary."""
    
    def __init__(self):
        self.announcers = [
            "Bob Elson", "Harry Caray", "Chuck Thompson", "Mel Allen", "Red Barber"
        ]
        
        # Radio-style phrases for different situations
        self.hit_phrases = [
            "connects beautifully", "rips a line drive", "smacks it hard",
            "makes solid contact", "drives it well", "tattoos the baseball"
        ]
        
        self.out_phrases = [
            "retires the side", "puts him away", "gets him out",
            "sends him back to the dugout", "fans him for the out"
        ]
        
        self.excitement_phrases = [
            "Holy cow!", "What a play!", "He got all of that one!",
            "That's a beauty!", "Boy oh boy!", "What a shot!"
        ]
        
        self.transition_phrases = [
            "And now", "Here comes", "Up steps", "To the plate comes",
            "Next up", "Stepping into the batter's box"
        ]
    
    def get_weather_description(self, date_str):
        """Generate a realistic weather description for the date."""
        month = int(date_str[4:6]) if len(date_str) >= 6 else 4
        
        if month in [4, 5]:  # Spring
            weather_options = [
                "a crisp spring afternoon", "partly cloudy skies", 
                "perfect baseball weather", "mild temperatures"
            ]
        elif month in [6, 7, 8]:  # Summer
            weather_options = [
                "a warm summer day", "bright sunshine", 
                "hot and humid conditions", "a beautiful day for baseball"
            ]
        else:  # Fall
            weather_options = [
                "cool autumn weather", "brisk conditions", 
                "a chilly afternoon", "fall baseball weather"
            ]
        
        return random.choice(weather_options)
    
    def format_radio_date(self, date_str):
        """Format date for radio broadcast style."""
        if len(date_str) == 8:
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            try:
                date_obj = datetime.datetime(int(year), int(month), int(day))
                return date_obj.strftime("%B %d, %Y")
            except:
                return date_str
        return date_str
    
    def get_inning_description(self, inning, is_bottom=False):
        """Get radio-style inning description."""
        ordinals = {
            1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth",
            6: "sixth", 7: "seventh", 8: "eighth", 9: "ninth", 
            10: "tenth", 11: "eleventh", 12: "twelfth"
        }
        
        inning_word = ordinals.get(inning, f"{inning}th")
        half = "bottom" if is_bottom else "top"
        
        if inning == 7:
            return f"It's the lucky {inning_word} inning stretch!"
        elif inning == 9:
            return f"We're in the {half} of the {inning_word} - the final frame!"
        else:
            return f"We're in the {half} of the {inning_word} inning"
    
    def parse_radio_play(self, play_description, player_name, defensive_lineup, player_positions, situation=""):
        """Parse play and create radio commentary."""
        excitement = random.choice(self.excitement_phrases)
        
        # Check for position code first
        if self.is_position_code(play_description):
            return self.decode_position_play(play_description, player_name, defensive_lineup, player_positions)

        if "Single" in play_description:
            phrases = [
                f"{player_name} {random.choice(self.hit_phrases)} for a single!",
                f"Base hit! {player_name} finds a hole for a single!",
                f"{player_name} slaps it through for a base hit!",
                f"And {player_name} gets good wood on it - single!"
            ]
        elif "Double" in play_description:
            phrases = [
                f"{excitement} {player_name} drives it to the gap for a double!",
                f"{player_name} turns on one and drives it deep - it's a two-bagger!",
                f"Extra base hit! {player_name} rips a double!",
                f"{player_name} gets into one and drives it off the wall - double!"
            ]
        elif "Triple" in play_description:
            phrases = [
                f"{excitement} {player_name} really gets into this one - it's rolling to the wall - triple!",
                f"{player_name} drives it deep to the gap - he's flying around first, around second - triple!",
                f"Oh my! {player_name} absolutely crushed that one - it's a three-base hit!",
                f"{player_name} connects and this one's deep - triple!"
            ]
        elif "Home Run" in play_description:
            phrases = [
                f"{excitement} {player_name} sends this one way back... way back... IT'S GONE! HOME RUN!",
                f"Get up, get up, GET OUT OF HERE! {player_name} has taken this one downtown!",
                f"{player_name} turns on this pitch and drives it deep - it's going... going... GONE!",
                f"Holy mackerel! {player_name} just launched that baseball into orbit! HOME RUN!",
                f"{player_name} got every bit of that one - it's over the fence! Touch 'em all!"
            ]
        elif "Walk" in play_description:
            phrases = [
                f"{player_name} works the count and draws a walk",
                f"Ball four! {player_name} takes his base",
                f"{player_name} shows patience at the plate and earns a free pass",
                f"Base on balls to {player_name} - good eye at the plate"
            ]
        elif "Strikeout" in play_description:
            phrases = [
                f"{player_name} goes down swinging - strike three!",
                f"The pitcher gets {player_name} looking - called strike three!",
                f"{player_name} fans on three pitches - that's a strikeout",
                f"Caught him looking! {player_name} takes the third strike"
            ]
        elif "Ground out" in play_description:
            position = play_description.split()[-1] if "position" in play_description else ""
            phrases = [
                f"{player_name} hits it on the ground - fielded cleanly for the out",
                f"Routine grounder by {player_name} - easy out",
                f"{player_name} grounds it over - one away",
                f"Ground ball, {player_name} - out at first"
            ]
        elif "Error" in play_description:
            phrases = [
                f"{player_name} hits a grounder - OH! It's bobbled! Safe on the error!",
                f"Ground ball by {player_name} - and it's mishandled! He's safe on the error!",
                f"{player_name} reaches base on an error - lucky break for the White Sox!",
                f"Fielding mistake! {player_name} is safe when he should have been out!"
            ]
        elif "Hit by Pitch" in play_description:
            phrases = [
                f"Oh! {player_name} gets plunked! That pitch got away and hit him",
                f"{player_name} takes one for the team - hit by the pitch",
                f"Wild pitch catches {player_name} - he takes his base",
                f"{player_name} gets drilled by that pitch - shake it off and take first base"
            ]
        elif "Stolen Base" in play_description:
            phrases = [
                f"{player_name} takes off - he's got second base stolen!",
                f"Here he goes! {player_name} steals second standing up!",
                f"{player_name} gets a good jump and swipes second base!",
                f"Stolen base! {player_name} beats the throw easily!"
            ]
        elif "Caught Stealing" in play_description:
            phrases = [
                f"{player_name} tries to steal but he's thrown out! Great throw!",
                f"There goes {player_name} - but the catcher guns him down!",
                f"{player_name} is picked off! Caught stealing!",
                f"Bad break! {player_name} is out trying to steal!"
            ]
        else:
            # Decode baseball position notation and other coded plays
            if self.is_position_code(play_description):
                return self.decode_position_play(play_description, player_name, defensive_lineup, player_positions)
            elif "/" in play_description:
                # Complex play notation
                phrases = [
                    f"{player_name} makes contact - that's fielded for an out",
                    f"{player_name} puts it in play - routine fielding play",
                    f"Contact by {player_name} - and he's retired"
                ]
            elif "FL" in play_description:
                phrases = [
                    f"{player_name} lifts a foul ball - it's caught for the out",
                    f"Pop foul by {player_name} - it's hauled in",
                    f"{player_name} pops it up foul and it's caught"
                ]
            elif "FO" in play_description:
                phrases = [
                    f"{player_name} hits a fly ball - and it's caught",
                    f"Fly ball by {player_name} - routine catch",
                    f"{player_name} lifts it up and it's brought in"
                ]
            elif ("sacrifice" in play_description.lower() or 
                  "bunt" in play_description.lower()):
                phrases = [
                    f"{player_name} lays down a sacrifice bunt",
                    f"Bunt by {player_name} - good execution",
                    f"{player_name} moves the runner with a sacrifice"
                ]
            elif "np" in play_description.lower():
                phrases = [
                    f"{player_name} makes contact",
                    f"{player_name} puts the ball in play",
                    f"Contact by {player_name}"
                ]
            else:
                # Generic fallback for unknown plays
                phrases = [
                    f"{player_name} makes contact - that's fielded for an out",
                    f"{player_name} puts it in play - routine fielding play",
                    f"Contact by {player_name} - and he's retired"
                ]
        
        return random.choice(phrases)
    
    def is_position_code(self, play_description):
        """Check if the play description is a baseball position code."""
        # Position codes are typically 1-9 digits with optional notation
        import re
        return bool(re.match(r'^\d+(\(\d+\))?(/|\.)?(\w+)?$', play_description.strip()))
    
    def decode_position_play(self, play_description, player_name, defensive_lineup, player_positions):
        """Decode baseball position notation into personalized play-by-play."""
        
        positions = {
            '1': 'pitcher', '2': 'catcher', '3': 'first baseman',
            '4': 'second baseman', '5': 'third baseman', '6': 'shortstop',
            '7': 'left fielder', '8': 'center fielder', '9': 'right fielder'
        }

        def get_player_by_position(pos_code):
            """Get player name from lineup based on position code."""
            position_name = positions.get(pos_code)
            if not position_name:
                return "the fielder"
            
            # Find the player in the defensive lineup who plays that position
            for player, pos in player_positions.items():
                if pos == position_name:
                    return player
            return f"the {position_name}"

        code = play_description.strip()
        
        # Handle simple position codes like "63", "43", "13"
        if len(code) == 2 and code.isdigit():
            first_player = get_player_by_position(code[0])
            second_player = get_player_by_position(code[1])
            
            phrases = [
                f"{player_name} grounds it to {first_player} - who throws to {second_player} for the out!",
                f"Ground ball hit by {player_name} to {first_player} - tossed to {second_player} for the easy out.",
                f"{player_name} hits a grounder to {first_player} - a routine play, and he's out at first.",
                f"Routine grounder by {player_name} - {first_player} to {second_player} for the out."
            ]
        elif len(code) == 1 and code.isdigit():
            fielder = get_player_by_position(code)
            phrases = [
                f"{player_name} hits it right to {fielder} for an easy out.",
                f"A sharp line drive by {player_name} - but it's caught by {fielder}!",
                f"{player_name} makes solid contact, but it's right at {fielder} for the out."
            ]
        elif "." in code:
            # Complex play with base running (like "43.1-2")
            phrases = [
                f"{player_name} makes contact - there's action on the bases!",
                f"Ground ball by {player_name} - they get the out but the runner advances.",
                f"{player_name} puts it in play - it's a fielder's choice."
            ]
        else:
            # Fallback for other position codes
            phrases = [
                f"{player_name} hits it to the infield - fielded for the out.",
                f"Ground ball by {player_name} - handled cleanly for the putout.",
                f"{player_name} makes contact - a routine defensive play."
            ]
        
        return random.choice(phrases)
    
    def generate_radio_broadcast(self, game_file_path):
        """Generate radio broadcast commentary for a game."""
        with open(game_file_path, 'r') as f:
            lines = f.readlines()
        
        # Parse game information
        game_info = {}
        current_inning = 0
        inning_plays = defaultdict(list)
        home_team_plays = []
        visiting_team_plays = []
        home_lineup = []
        visiting_lineup = []
        player_positions = {}
        
        home_team_name = ""
        visiting_team_name = ""

        for line in lines:
            line = line.strip()
            if line.startswith("---"):
                game_info['game_id'] = line.replace("-", "").strip()
            elif line.startswith("Date:"):
                game_info['date'] = line.replace("Date:", "").strip()
            elif line.startswith("Home:"):
                home_team_name = line.replace("Home:", "").strip()
                game_info['home_team'] = home_team_name
            elif line.startswith("Visiting:"):
                visiting_team_name = line.replace("Visiting:", "").strip()
                game_info['visiting_team'] = visiting_team_name
            elif line.startswith("Lineup:"):
                parts = line.split(" - ")
                player_name = parts[0].replace("Lineup:", "").strip()
                position = parts[1].strip()
                player_positions[player_name] = position
            elif line.startswith("Inning"):
                current_inning = int(line.split()[1])
            elif line.startswith("Final Score:"):
                final = line.replace("Final Score:", "").strip()
                game_info['final_score'] = final
            elif current_inning > 0:
                # Parse plays for both teams
                home_team = game_info.get('home_team', '')
                visiting_team = game_info.get('visiting_team', '')
                
                if f"{home_team}:" in line:
                    play = line.replace(f"{home_team}:", "").strip()
                    home_team_plays.append((current_inning, play))
                    inning_plays[current_inning].append((home_team, play))
                    if current_inning == 1:
                        player = play.split(" - ")[0].strip()
                        if player not in home_lineup:
                            home_lineup.append(player)
                elif f"{visiting_team}:" in line:
                    play = line.replace(f"{visiting_team}:", "").strip()
                    visiting_team_plays.append((current_inning, play))
                    inning_plays[current_inning].append((visiting_team, play))
                    if current_inning == 1:
                        player = play.split(" - ")[0].strip()
                        if player not in visiting_lineup:
                            visiting_lineup.append(player)

        return self.create_radio_broadcast(game_info, inning_plays, 
                                         home_team_plays, visiting_team_plays,
                                         home_lineup, visiting_lineup, player_positions)
    
    def format_lineup(self, team_name, lineup):
        """Formats the starting lineup for the broadcast."""
        if not lineup:
            return ""
        
        lineup_str = [f"STARTING LINEUP: {team_name.upper()}"]
        lineup_str.append("-" * 30)
        for i, player in enumerate(lineup, 1):
            lineup_str.append(f"{i}. {player}")
        lineup_str.append("")
        return "\n".join(lineup_str)

    def create_radio_broadcast(self, game_info, inning_plays, 
                              home_team_plays, visiting_team_plays,
                              home_lineup, visiting_lineup, player_positions):
        """Create radio broadcast-style commentary."""
        broadcast = []
        announcer = random.choice(self.announcers)
        date_str = game_info.get('date', '').replace('/', '')
        date_formatted = self.format_radio_date(date_str)
        weather = self.get_weather_description(date_str)
        
        # Determine the focus team (usually the home team)
        home_team = game_info.get('home_team', 'Home Team')
        visiting_team = game_info.get('visiting_team', 'Visiting Team')
        focus_team = home_team
        focus_team_plays = home_team_plays
        
        # Opening
        broadcast.append("*" * 80)
        broadcast.append(f"🎙️  {focus_team.upper()} RADIO BROADCAST")
        broadcast.append("*" * 80)
        broadcast.append("")
        broadcast.append(f"Good afternoon, baseball fans! This is "
                        f"{announcer} coming to you live")
        
        if focus_team == home_team:
            venue = "from the home ballpark"
            broadcast.append(f"{venue} on {date_formatted}.")
        else:
            venue = f"from {home_team}"
            broadcast.append(f"{venue} on {date_formatted}.")
        
        broadcast.append(f"It's {weather} here at the ballpark, "
                        f"perfect for America's pastime!")
        broadcast.append("")
        
        opponent = visiting_team if focus_team == home_team else home_team
        broadcast.append(f"Today the {focus_team} take on the {opponent}")
        
        if focus_team == home_team:
            broadcast.append("here at home.")
        else:
            broadcast.append("on the road.")
        
        broadcast.append("")
        broadcast.append(self.format_lineup(home_team, home_lineup))
        broadcast.append(self.format_lineup(visiting_team, visiting_lineup))

        broadcast.append("Let's get this ballgame underway!")
        broadcast.append("")
        broadcast.append("=" * 60)
        broadcast.append("")
        
        # Inning by inning commentary
        for inning in sorted(inning_plays.keys()):
            if inning == 0:
                continue
            
            inning_desc = self.get_inning_description(inning).upper()
            broadcast.append(f"🎙️  {inning_desc}")
            broadcast.append("-" * 40)
            broadcast.append("")
            
            focus_team_at_bat = []
            for team, play in inning_plays[inning]:
                if team == focus_team:
                    focus_team_at_bat.append(play)
            
            if focus_team_at_bat:
                if inning == 1:
                    broadcast.append(f"The {focus_team} come to bat "
                                   f"for the first time today...")
                elif inning == 9:
                    broadcast.append(f"Bottom of the ninth - here come the {focus_team}!")
                else:
                    broadcast.append(f"The {focus_team} come to the plate...")
                broadcast.append("")
                
                for i, play in enumerate(focus_team_at_bat):
                    player = play.split(" - ")[0].strip()
                    action = " - ".join(play.split(" - ")[1:]).strip()
                    
                    # Add transition phrase
                    transition_phrase = random.choice(self.transition_phrases)
                    transition = f"{transition_phrase} {player}..."
                    
                    broadcast.append(transition)
                    
                    # Generate radio commentary
                    radio_call = self.parse_radio_play(action, player, visiting_lineup, player_positions)
                    broadcast.append(f"   {radio_call}")
                    broadcast.append("")
                
                # Add some color commentary
                hits_this_inning = sum(1 for play in focus_team_at_bat 
                                     if any(hit in play for hit in 
                                           ["Single", "Double", "Triple", 
                                            "Home Run"]))
                
                if hits_this_inning >= 2:
                    broadcast.append(f"The {focus_team} are really "
                                   f"putting some wood on the ball this inning!")
                elif hits_this_inning == 0:
                    broadcast.append(f"The pitcher is keeping the "
                                   f"{focus_team} in check so far.")
                
                broadcast.append("")
            else:
                broadcast.append(f"No {focus_team} at-bats this half inning.")
                broadcast.append("")
            
            broadcast.append("-" * 40)
            broadcast.append("")
        
        # Game wrap-up
        broadcast.append("🎙️  FINAL SCORE")
        broadcast.append("=" * 40)
        broadcast.append("")
        final_score = game_info.get('final_score', 'Score unavailable')
        broadcast.append(f"And that's your ballgame! Final score: {final_score}")
        broadcast.append("")
        
        # Count focus team performance
        total_hits = sum(1 for _, play in focus_team_plays 
                        if any(hit in play for hit in 
                              ["Single", "Double", "Triple", "Home Run"]))
        home_runs = sum(1 for _, play in focus_team_plays 
                       if "Home Run" in play)
        
        if home_runs > 0:
            hr_text = "home run" if home_runs == 1 else "home runs"
            broadcast.append(f"The {focus_team} connected for "
                           f"{home_runs} {hr_text} today!")
        
        broadcast.append(f"The {focus_team} collected {total_hits} "
                        f"hits in today's contest.")
        broadcast.append("")
        broadcast.append(f"Thanks for joining us for {focus_team} baseball!")
        broadcast.append(f"This has been {announcer} signing off.")
        broadcast.append("We'll see you next time at the old ballpark!")
        broadcast.append("")
        broadcast.append("*" * 80)
        broadcast.append("📻  END OF BROADCAST")
        broadcast.append("*" * 80)
        
        return "\n".join(broadcast)
    
    def process_all_team_games(self, base_dir="game_log"):
        """Process all team games and create radio broadcasts."""
        if not os.path.exists(base_dir):
            print(f"Directory {base_dir} not found!")
            return
        
        # Get all team directories
        team_dirs = [d for d in os.listdir(base_dir) 
                    if os.path.isdir(os.path.join(base_dir, d))]
        team_dirs.sort()
        
        print(f"🎙️  Creating radio broadcasts for {len(team_dirs)} teams...")
        print("📻  'Good afternoon, baseball fans!'")
        print("")
        
        total_games_processed = 0
        
        for team in team_dirs:
            team_path = os.path.join(base_dir, team)
            year_dirs = [d for d in os.listdir(team_path) 
                        if os.path.isdir(os.path.join(team_path, d))]
            
            for year in year_dirs:
                team_year_path = os.path.join(team_path, year)
                
                # Create output directory
                output_dir = f"radio_broadcasts/{team}/{year}"
                os.makedirs(output_dir, exist_ok=True)
                
                game_files = [f for f in os.listdir(team_year_path) 
                             if f.endswith('.txt')]
                game_files.sort()
                
                if not game_files:
                    continue
                
                print(f"📻  Broadcasting {len(game_files)} games for {team} {year}...")
                
                for i, game_file in enumerate(game_files, 1):
                    game_path = os.path.join(team_year_path, game_file)
                    
                    try:
                        radio_broadcast = self.generate_radio_broadcast(game_path)
                        
                        # Create output filename
                        output_filename = game_file.replace('.txt', '_radio.txt')
                        output_path = os.path.join(output_dir, output_filename)
                        
                        # Write radio broadcast
                        with open(output_path, 'w') as f:
                            f.write(radio_broadcast)
                        
                        total_games_processed += 1
                        
                    except Exception as e:
                        print(f"   ❌ Error broadcasting {game_file}: {str(e)}")
                
                # Create broadcast summary
                self.create_broadcast_summary(output_dir, game_files, team, year)
                
                print(f"  ✅ {len(game_files)} radio broadcasts saved to {output_dir}")
        
        print(f"\n🎙️  Total: {total_games_processed} radio broadcasts created for all teams!")
        print("📻  'Thanks for listening to baseball!'")
        
    def process_all_white_sox_games(self, base_dir="game_log/CHA/1975"):
        """Process all Chicago White Sox games and create radio broadcasts."""
        # Keep this method for backward compatibility
        return self.process_team_games("CHA", "1975", base_dir)
    
    def create_broadcast_summary(self, output_dir, game_files, team, year):
        """Create a radio broadcast summary."""
        summary_path = os.path.join(output_dir, "broadcast_guide.txt")
        
        summary = []
        summary.append("*" * 80)
        summary.append(f"📻  {team.upper()} {year} RADIO BROADCAST COLLECTION")
        summary.append("*" * 80)
        summary.append("")
        summary.append("Welcome to the complete collection of old-school radio broadcasts")
        summary.append(f"for the {year} {team} season!")
        summary.append("")
        summary.append(f"Total Broadcasts: {len(game_files)}")
        summary.append("")
        summary.append("🎙️  WHAT YOU'LL HEAR:")
        summary.append("• Authentic 1970s radio commentary style")
        summary.append("• Play-by-play excitement and drama")
        summary.append("• Classic baseball radio phrases")
        summary.append("• Legendary announcer voices")
        summary.append("• Colorful descriptions and storytelling")
        summary.append("")
        summary.append("📻  FEATURED ANNOUNCERS:")
        summary.append("• Bob Elson - 'The Commander'")
        summary.append("• Harry Caray - 'Holy Cow!'") 
        summary.append("• Chuck Thompson - Baltimore/Chicago legend")
        summary.append("• Mel Allen - 'How about that!'")
        summary.append("• Red Barber - 'In the catbird seat'")
        summary.append("")
        summary.append("🎙️  FILES:")
        summary.append("Each broadcast is named: [DATE]_vs_[OPPONENT]_radio.txt")
        summary.append("")
        summary.append("Grab some peanuts and Cracker Jack, sit back, and enjoy")
        summary.append(f"the sounds of {year} {team} baseball!")
        summary.append("")
        summary.append("*" * 80)
        summary.append("📻  'Take me out to the ballgame!'")
        summary.append("*" * 80)
        
        with open(summary_path, 'w') as f:
            f.write("\n".join(summary))
        
        print(f"📻  Broadcast guide saved to {summary_path}")


def main():
    """Main function to run the radio broadcast reporter."""
    print("🎙️  Starting Baseball Radio Broadcast Generator...")
    print("📻  'Good afternoon, baseball fans!'")
    print("")
    
    reporter = RadioBroadcastReporter()
    reporter.process_all_team_games()


if __name__ == "__main__":
    main()
