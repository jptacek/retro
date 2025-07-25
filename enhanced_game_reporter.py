import os
import datetime
from collections import defaultdict


class EnhancedGameReporter:
    """Enhanced game reporter that creates detailed, narrative game reports."""
    
    def __init__(self):
        self.team_records = defaultdict(lambda: {'wins': 0, 'losses': 0})
        self.player_stats = defaultdict(lambda: {
            'at_bats': 0, 'hits': 0, 'runs': 0, 'rbis': 0,
            'walks': 0, 'strikeouts': 0, 'home_runs': 0
        })
        
    def parse_enhanced_play(self, play_description):
        """Parse play description and extract detailed information."""
        if "Single" in play_description:
            return {"type": "single", "result": "Hit", "bases": 1}
        elif "Double" in play_description:
            return {"type": "double", "result": "Hit", "bases": 2}
        elif "Triple" in play_description:
            return {"type": "triple", "result": "Hit", "bases": 3}
        elif "Home Run" in play_description:
            return {"type": "home_run", "result": "Hit", "bases": 4}
        elif "Walk" in play_description:
            return {"type": "walk", "result": "Walk", "bases": 1}
        elif "Strikeout" in play_description:
            return {"type": "strikeout", "result": "Out", "bases": 0}
        elif "Ground out" in play_description:
            return {"type": "groundout", "result": "Out", "bases": 0}
        elif "Error" in play_description:
            return {"type": "error", "result": "Error", "bases": 1}
        elif "Stolen Base" in play_description:
            return {"type": "stolen_base", "result": "Advancement", "bases": 1}
        elif "Caught Stealing" in play_description:
            return {"type": "caught_stealing", "result": "Out", "bases": 0}
        elif "Sacrifice" in play_description:
            return {"type": "sacrifice", "result": "Out", "bases": 0}
        else:
            return {"type": "other", "result": "Other", "bases": 0}
    
    def format_date(self, date_str):
        """Format date string into a readable format."""
        if len(date_str) == 8:  # YYYYMMDD
            year = date_str[:4]
            month = date_str[4:6]
            day = date_str[6:8]
            try:
                date_obj = datetime.datetime(int(year), int(month), int(day))
                return date_obj.strftime("%A, %B %d, %Y")
            except:
                return date_str
        return date_str
    
    def generate_game_narrative(self, game_file_path):
        """Generate an enhanced narrative report for a single game."""
        with open(game_file_path, 'r') as f:
            lines = f.readlines()
        
        # Parse game information
        game_info = {}
        current_inning = 0
        inning_plays = defaultdict(list)
        white_sox_plays = []
        opponent_plays = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("---"):
                game_info['game_id'] = line.replace("-", "").strip()
            elif line.startswith("Date:"):
                game_info['date'] = line.replace("Date:", "").strip()
            elif line.startswith("Home:"):
                game_info['home_team'] = line.replace("Home:", "").strip()
            elif line.startswith("Visiting:"):
                game_info['visiting_team'] = line.replace("Visiting:", "").strip()
            elif line.startswith("Inning"):
                current_inning = int(line.split()[1])
            elif line.startswith("Final Score:"):
                game_info['final_score'] = line.replace("Final Score:", "").strip()
            elif ":" in line and line != "" and not line.startswith("---"):
                # This is a play
                if "White Sox:" in line:
                    play = line.replace("White Sox:", "").strip()
                    white_sox_plays.append((current_inning, play))
                    inning_plays[current_inning].append(('White Sox', play))
                elif current_inning > 0:
                    # Opponent play
                    team_name = line.split(":")[0]
                    play = ":".join(line.split(":")[1:]).strip()
                    opponent_plays.append((current_inning, play))
                    inning_plays[current_inning].append((team_name, play))
        
        # Generate enhanced report
        report = self.create_enhanced_report(game_info, inning_plays, white_sox_plays, opponent_plays)
        return report
    
    def create_enhanced_report(self, game_info, inning_plays, white_sox_plays, opponent_plays):
        """Create a detailed, narrative game report."""
        report = []
        
        # Header
        date_formatted = self.format_date(game_info.get('date', '').replace('/', ''))
        report.append("=" * 80)
        report.append("CHICAGO WHITE SOX GAME REPORT")
        report.append("=" * 80)
        report.append(f"Date: {date_formatted}")
        report.append(f"Opponent: {game_info.get('home_team', 'Unknown') if 'White Sox' in game_info.get('visiting_team', '') else game_info.get('visiting_team', 'Unknown')}")
        report.append(f"Venue: {'Home' if 'White Sox' in game_info.get('home_team', '') else 'Away'}")
        report.append(f"Final Score: {game_info.get('final_score', 'Unknown')}")
        report.append("")
        
        # Game Summary
        report.append("GAME SUMMARY")
        report.append("-" * 40)
        
        # Count different types of plays for White Sox
        hits = sum(1 for _, play in white_sox_plays if any(hit_type in play for hit_type in ["Single", "Double", "Triple", "Home Run"]))
        walks = sum(1 for _, play in white_sox_plays if "Walk" in play)
        strikeouts = sum(1 for _, play in white_sox_plays if "Strikeout" in play)
        errors = sum(1 for _, play in white_sox_plays if "Error" in play)
        
        report.append(f"White Sox Performance:")
        report.append(f"  • Total Hits: {hits}")
        report.append(f"  • Walks: {walks}")
        report.append(f"  • Strikeouts: {strikeouts}")
        report.append(f"  • Reached on Error: {errors}")
        report.append("")
        
        # Key Moments
        report.append("KEY MOMENTS")
        report.append("-" * 40)
        
        # Find home runs
        home_runs = [(inning, play) for inning, play in white_sox_plays if "Home Run" in play]
        if home_runs:
            report.append("⚾ HOME RUNS:")
            for inning, play in home_runs:
                player = play.split(" - ")[0].strip()
                report.append(f"  • Inning {inning}: {player} connects for a home run!")
            report.append("")
        
        # Find doubles and triples
        extra_base_hits = [(inning, play) for inning, play in white_sox_plays if any(x in play for x in ["Double", "Triple"])]
        if extra_base_hits:
            report.append("💥 EXTRA BASE HITS:")
            for inning, play in extra_base_hits:
                player = play.split(" - ")[0].strip()
                hit_type = "double" if "Double" in play else "triple"
                report.append(f"  • Inning {inning}: {player} rips a {hit_type}!")
            report.append("")
        
        # Inning by Inning
        report.append("INNING-BY-INNING BREAKDOWN")
        report.append("-" * 40)
        
        for inning in sorted(inning_plays.keys()):
            if inning == 0:
                continue
            report.append(f"Inning {inning}:")
            
            inning_narrative = []
            for team, play in inning_plays[inning]:
                if team == "White Sox":
                    player = play.split(" - ")[0].strip()
                    action = " - ".join(play.split(" - ")[1:]).strip()
                    parsed_play = self.parse_enhanced_play(action)
                    
                    if parsed_play["result"] == "Hit":
                        if parsed_play["type"] == "home_run":
                            inning_narrative.append(f"🔥 {player} launches a HOME RUN!")
                        elif parsed_play["type"] == "triple":
                            inning_narrative.append(f"⚡ {player} smashes a triple!")
                        elif parsed_play["type"] == "double":
                            inning_narrative.append(f"💪 {player} doubles!")
                        else:
                            inning_narrative.append(f"✅ {player} gets a hit ({action})")
                    elif parsed_play["result"] == "Walk":
                        inning_narrative.append(f"👁️ {player} draws a walk")
                    elif parsed_play["result"] == "Out":
                        if "Strikeout" in action:
                            inning_narrative.append(f"🥶 {player} strikes out")
                        else:
                            inning_narrative.append(f"❌ {player} makes an out ({action})")
                    else:
                        inning_narrative.append(f"• {player} - {action}")
            
            if inning_narrative:
                for narrative in inning_narrative:
                    report.append(f"  {narrative}")
            else:
                report.append("  No White Sox activity this inning")
            report.append("")
        
        # Player Spotlight
        report.append("PLAYER SPOTLIGHT")
        report.append("-" * 40)
        
        # Find standout performers
        player_performance = defaultdict(lambda: {'hits': 0, 'walks': 0, 'strikeouts': 0, 'home_runs': 0})
        
        for _, play in white_sox_plays:
            player = play.split(" - ")[0].strip()
            action = " - ".join(play.split(" - ")[1:]).strip()
            
            if any(hit in action for hit in ["Single", "Double", "Triple", "Home Run"]):
                player_performance[player]['hits'] += 1
            if "Home Run" in action:
                player_performance[player]['home_runs'] += 1
            if "Walk" in action:
                player_performance[player]['walks'] += 1
            if "Strikeout" in action:
                player_performance[player]['strikeouts'] += 1
        
        # Highlight top performers
        for player, stats in player_performance.items():
            if stats['hits'] >= 2 or stats['home_runs'] >= 1:
                report.append(f"⭐ {player}:")
                if stats['hits'] > 0:
                    report.append(f"  • {stats['hits']} hit{'s' if stats['hits'] != 1 else ''}")
                if stats['home_runs'] > 0:
                    report.append(f"  • {stats['home_runs']} home run{'s' if stats['home_runs'] != 1 else ''}")
                if stats['walks'] > 0:
                    report.append(f"  • {stats['walks']} walk{'s' if stats['walks'] != 1 else ''}")
                report.append("")
        
        # Footer
        report.append("=" * 80)
        report.append("End of Game Report")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def process_all_team_games(self, base_dir="game_log"):
        """Process all team games and create enhanced reports."""
        if not os.path.exists(base_dir):
            print(f"Directory {base_dir} not found!")
            return
        
        # Get all team directories
        team_dirs = [d for d in os.listdir(base_dir) 
                    if os.path.isdir(os.path.join(base_dir, d))]
        team_dirs.sort()
        
        print(f"🎯 Processing enhanced reports for {len(team_dirs)} teams...")
        print("")
        
        total_games_processed = 0
        
        for team in team_dirs:
            team_path = os.path.join(base_dir, team)
            year_dirs = [d for d in os.listdir(team_path) 
                        if os.path.isdir(os.path.join(team_path, d))]
            
            for year in year_dirs:
                team_year_path = os.path.join(team_path, year)
                
                # Create output directory
                output_dir = f"enhanced_reports/{team}/{year}"
                os.makedirs(output_dir, exist_ok=True)
                
                game_files = [f for f in os.listdir(team_year_path) 
                             if f.endswith('.txt')]
                game_files.sort()
                
                if not game_files:
                    continue
                
                print(f"📊 Processing {len(game_files)} games for {team} {year}...")
                
                for game_file in game_files:
                    game_path = os.path.join(team_year_path, game_file)
                    
                    try:
                        enhanced_report = self.generate_game_narrative(game_path)
                        
                        # Create output filename
                        output_filename = game_file.replace('.txt', '_enhanced.txt')
                        output_path = os.path.join(output_dir, output_filename)
                        
                        # Write enhanced report
                        with open(output_path, 'w') as f:
                            f.write(enhanced_report)
                        
                        total_games_processed += 1
                        
                    except Exception as e:
                        print(f"  ❌ Error processing {game_file}: {str(e)}")
                
                # Create season summary
                self.create_season_summary(output_dir, game_files, team, year)
                
                print(f"  ✅ {len(game_files)} enhanced reports saved to {output_dir}")
        
        print(f"\n🎉 Total: {total_games_processed} enhanced reports created for all teams!")
    
    def create_season_summary(self, output_dir, game_files, team, year):
        """Create a season summary report."""
        summary_path = os.path.join(output_dir, "season_summary.txt")
        
        summary = []
        summary.append("=" * 80)
        summary.append(f"{team.upper()} {year} SEASON SUMMARY")
        summary.append("=" * 80)
        summary.append(f"Total Games Processed: {len(game_files)}")
        summary.append("")
        summary.append("This directory contains enhanced game reports for all")
        summary.append(f"{team} games from the {year} season.")
        summary.append("")
        summary.append("Each report includes:")
        summary.append("• Detailed game summary with key statistics")
        summary.append("• Key moments and highlights")
        summary.append("• Inning-by-inning narrative breakdown")
        summary.append("• Player spotlight featuring standout performances")
        summary.append("")
        summary.append("Files are named: [DATE]_vs_[OPPONENT]_enhanced.txt")
        summary.append("")
        summary.append("=" * 80)
        
        with open(summary_path, 'w') as f:
            f.write("\n".join(summary))
        
        print(f"📊 Season summary saved to {summary_path}")


def main():
    """Main function to run the enhanced game reporter."""
    reporter = EnhancedGameReporter()
    reporter.process_all_team_games()


if __name__ == "__main__":
    main()
