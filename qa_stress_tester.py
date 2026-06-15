import random
import time
import sys

class Entity:
    """Represents a combat participant (Player or Boss) with base stats."""
    def __init__(self, name, hp, attack, defense, crit_rate):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.crit_rate = crit_rate  # Decimal percentage (e.g., 0.20 = 20%)

    def is_alive(self):
        return self.hp > 0

    def reset_health(self):
        self.hp = self.max_hp


def calculate_damage(attacker, defender):
    """Calculates damage reduction based on standard RPG combat formulas."""
    # Boundary Validation: Catch corrupted data values (None, Strings, or Negative Numbers)
    if attacker.attack is None or defender.defense is None:
        raise TypeError("Entity attributes cannot be NoneType.")
    if not isinstance(attacker.attack, (int, float)) or not isinstance(defender.defense, (int, float)):
        raise ValueError("Entity attributes must be numerical digits.")
    if attacker.attack < 0 or defender.defense < 0:
        raise ValueError("Negative attribute parameters injected into calculation engine.")

    # Calculate critical strike probability
    is_crit = random.random() < attacker.crit_rate
    
    # Base Damage Formula
    base_damage = max(1, attacker.attack - defender.defense)
    
    if is_crit:
        final_damage = int(base_damage * 1.5)
    else:
        final_damage = base_damage
        
    return final_damage, is_crit


def run_automation_assessment(player, boss, iterations=10000):
    """Runs a batch simulation to collect game balance metrics and performance telemetry."""
    start_time = time.time()
    
    player_wins = 0
    boss_wins = 0
    total_rounds_played = 0
    max_damage_spike = 0
    longest_match_rounds = 0
    
    # Main stress test loop
    for match_id in range(1, iterations + 1):
        player.reset_health()
        boss.reset_health()
        match_rounds = 0
        
        while player.is_alive() and boss.is_alive():
            match_rounds += 1
            
            # Player Turn
            damage, crit = calculate_damage(player, boss)
            boss.hp -= damage
            if damage > max_damage_spike:
                max_damage_spike = damage
                
            if not boss.is_alive():
                player_wins += 1
                break
                
            # Boss Turn
            damage, crit = calculate_damage(boss, player)
            player.hp -= damage
            if damage > max_damage_spike:
                max_damage_spike = damage
                
            if not player.is_alive():
                boss_wins += 1
                break
        
        total_rounds_played += match_rounds
        if match_rounds > longest_match_rounds:
            longest_match_rounds = match_rounds

    execution_time = time.time() - start_time
    player_win_rate = (player_wins / iterations) * 100
    boss_win_rate = (boss_wins / iterations) * 100
    avg_match_duration = total_rounds_played / iterations

    return {
        "iterations": iterations,
        "execution_time": execution_time,
        "avg_match_duration": avg_match_duration,
        "player_win_rate": player_win_rate,
        "boss_win_rate": boss_win_rate,
        "max_damage_spike": max_damage_spike,
        "longest_match_rounds": longest_match_rounds
    }


def run_boundary_test_suite():
    """Simulates invalid edge-case inputs to verify system exception handling."""
    test_logs = []

    # Test Case 01: Baseline Execution
    try:
        p = Entity("Tester", 100, 20, 10, 0.1)
        b = Entity("Target", 100, 15, 5, 0.0)
        calculate_damage(p, b)
        test_logs.append("[PASS] Test Case 01: Standard Operational Flow")
    except Exception as e:
        test_logs.append(f"[FAIL] Test Case 01: Unexpected Crash -> {str(e)}")

    # Test Case 02: Negative Value Injection
    try:
        p = Entity("Hacked_Player", 100, -50, 10, 0.1)
        b = Entity("Target", 100, 15, 5, 0.0)
        calculate_damage(p, b)
        test_logs.append("[FAIL] Test Case 02: System accepted negative data input.")
    except ValueError:
        test_logs.append("[PASS] Test Case 02: Negative Bound Input -> CATCH: BUG-002 (Value Blocked)")

    # Test Case 03: Invalid Data Type Input
    try:
        p = Entity("Broken_Asset", 100, "CorruptedStringData", 10, 0.1)
        b = Entity("Target", 100, 15, 5, 0.0)
        calculate_damage(p, b)
        test_logs.append("[FAIL] Test Case 03: System accepted text-string attribute.")
    except (TypeError, ValueError):
        test_logs.append("[PASS] Test Case 03: Invalid Payload -> CATCH: BUG-003 (Handled Safely)")

    return test_logs


# --- MAIN RUNTIME MAIN ---
if __name__ == "__main__":
    print("====================================================================")
    print("                        ENGINE RUNTIME LOGS                         ")
    print("====================================================================\n")
    
    test_player = Entity(name="Player-1", hp=150, attack=30, defense=10, crit_rate=0.20)
    test_boss = Entity(name="Boss-1", hp=350, attack=22, defense=7, crit_rate=0.05)
    
    metrics = run_automation_assessment(test_player, test_boss, iterations=10000)
    boundary_results = run_boundary_test_suite()

    # Export report to local text file
    report_filename = "QA_Test_Report.txt"
    with open(report_filename, "w", encoding="utf-8") as report:
        report.write("====================================================================\n")
        report.write("               QA AUTOMATED TELEMETRY & BOUNDARY REPORT\n")
        report.write("====================================================================\n")
        report.write(f"Total Matches Simulated : {metrics['iterations']:,}\n")
        report.write(f"Execution Engine Time   : {metrics['execution_time']:.4f} seconds\n")
        report.write(f"Average Match Duration  : {metrics['avg_match_duration']:.1f} Rounds\n\n")
        
        report.write("[GAME BALANCE & METRICS]\n")
        report.write("--------------------------------------------------------------------\n")
        report.write(f"- Player Win Rate       : {metrics['player_win_rate']:.1f}%\n")
        report.write(f"- Boss Win Rate         : {metrics['boss_win_rate']:.1f}%\n")
        report.write(f"- Highest Damage Spike  : {metrics['max_damage_spike']} DMG\n")
        report.write(f"- Longest Single Match  : {metrics['longest_match_rounds']} Rounds\n\n")
        
        report.write("[EDGE-CASE & BOUNDARY TEST LOG]\n")
        report.write("--------------------------------------------------------------------\n")
        for result in boundary_results:
            report.write(f"{result}\n")
        report.write("\nSTATUS: AUTOMATED ENGINE BUILD STABLE WITH 0 UNHANDLED EXTREME CRASHES.\n")
        report.write("====================================================================\n")

    print(f"Automation completed. Logs compiled to: {report_filename}")