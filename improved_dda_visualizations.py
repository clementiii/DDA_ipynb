# Improved DDA Visualizations - More Intuitive Charts
# These show HOW the algorithm works, not just statistical results

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Dict, List

def plot_algorithm_story(responses_dict: Dict[str, List], figsize=(16, 12)):
    """
    Show the DDA algorithm's 'story' - how it adapts to different players
    Much clearer than the current visualizations!
    """
    
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    fig.suptitle('🎮 How the Bathala DDA Algorithm Adapts to Players', fontsize=16, fontweight='bold')
    
    colors = {'novice': '#FF6B6B', 'balanced': '#4ECDC4', 'skilled': '#45B7D1', 'expert': '#96CEB4'}
    
    # 1. Performance Score Journey (shows the algorithm learning)
    ax1 = axes[0, 0]
    for skill, responses in responses_dict.items():
        pps_scores = [r.pps_score for r in responses]
        ax1.plot(range(len(pps_scores)), pps_scores, 
                label=f'{skill.title()} Player', color=colors[skill], linewidth=3, marker='o', markersize=4)
    
    ax1.set_title('🧠 Algorithm Learning: Performance Score Over Time')
    ax1.set_xlabel('Combat Number')
    ax1.set_ylabel('Performance Score (Higher = More Skilled)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5, label='Baseline')
    
    # 2. Difficulty Tier Timeline (shows adaptation in action)
    ax2 = axes[0, 1]
    for skill, responses in responses_dict.items():
        tiers = [r.difficulty_tier for r in responses]
        ax2.plot(range(len(tiers)), tiers, 
                label=f'{skill.title()}', color=colors[skill], linewidth=3, marker='s', markersize=4)
    
    ax2.set_title('⚖️ Difficulty Adaptation Over Time')
    ax2.set_xlabel('Combat Number')
    ax2.set_ylabel('Difficulty Tier (0=Easy, 5=Hard)')
    ax2.set_ylim(-0.5, 5.5)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Enemy Strength Adjustments (shows real game impact)
    ax3 = axes[0, 2]
    for skill, responses in responses_dict.items():
        enemy_hp = [r.enemy_hp_multiplier for r in responses]
        ax3.plot(range(len(enemy_hp)), enemy_hp, 
                label=f'{skill.title()}', color=colors[skill], linewidth=3, marker='^', markersize=4)
    
    ax3.set_title('💪 Enemy Strength Adjustments')
    ax3.set_xlabel('Combat Number')
    ax3.set_ylabel('Enemy HP Multiplier')
    ax3.axhline(y=1.0, color='black', linestyle='--', alpha=0.5, label='Normal Strength')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Time Spent in Each Difficulty Tier (clearer than box plots!)
    ax4 = axes[1, 0]
    tier_percentages = {}
    
    for skill, responses in responses_dict.items():
        tiers = [r.difficulty_tier for r in responses]
        total_combats = len(tiers)
        tier_counts = {i: tiers.count(i) for i in range(6)}
        tier_percentages[skill] = {tier: (count/total_combats)*100 for tier, count in tier_counts.items()}
    
    # Create stacked bar chart
    bottom_vals = {skill: 0 for skill in tier_percentages.keys()}
    tier_colors = ['#ffcccc', '#ffe6cc', '#ffffcc', '#e6ffcc', '#ccffe6', '#ccccff']
    
    for tier in range(6):
        values = [tier_percentages[skill].get(tier, 0) for skill in ['novice', 'balanced', 'skilled', 'expert']]
        ax4.bar(['Novice', 'Balanced', 'Skilled', 'Expert'], values, 
               bottom=[bottom_vals[skill] for skill in ['novice', 'balanced', 'skilled', 'expert']],
               label=f'Tier {tier}', color=tier_colors[tier])
        
        for i, skill in enumerate(['novice', 'balanced', 'skilled', 'expert']):
            bottom_vals[skill] += tier_percentages[skill].get(tier, 0)
    
    ax4.set_title('📊 Time Spent in Each Difficulty Level')
    ax4.set_ylabel('Percentage of Time (%)')
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 5. Algorithm Assistance Features (shows help mechanisms)
    ax5 = axes[1, 1]
    
    # Show shop price multipliers (lower = more help)
    shop_help = {}
    for skill, responses in responses_dict.items():
        avg_shop_mult = np.mean([r.shop_price_multiplier for r in responses])
        shop_help[skill] = (1.25 - avg_shop_mult) * 100  # Convert to "% discount"
    
    bars = ax5.bar(shop_help.keys(), shop_help.values(), 
                  color=[colors[skill] for skill in shop_help.keys()])
    ax5.set_title('🛒 Shop Price Assistance')
    ax5.set_ylabel('Average Discount (%)')
    ax5.set_xlabel('Player Type')
    
    # Add value labels on bars
    for bar, value in zip(bars, shop_help.values()):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{value:.1f}%', ha='center', va='bottom')
    
    # 6. Final Results Summary (shows if algorithm worked)
    ax6 = axes[1, 2]
    
    final_tiers = []
    tier_changes = []
    
    for skill, responses in responses_dict.items():
        final_tiers.append(responses[-1].difficulty_tier)
        # Count tier changes
        tiers = [r.difficulty_tier for r in responses]
        changes = sum(1 for i in range(1, len(tiers)) if tiers[i] != tiers[i-1])
        tier_changes.append(changes)
    
    x = np.arange(len(['Novice', 'Balanced', 'Skilled', 'Expert']))
    width = 0.35
    
    bars1 = ax6.bar(x - width/2, final_tiers, width, label='Final Difficulty Tier', 
                   color=[colors[skill] for skill in ['novice', 'balanced', 'skilled', 'expert']])
    bars2 = ax6.bar(x + width/2, tier_changes, width, label='Number of Adaptations',
                   color=[colors[skill] for skill in ['novice', 'balanced', 'skilled', 'expert']], alpha=0.7)
    
    ax6.set_title('🎯 Algorithm Success Metrics')
    ax6.set_xlabel('Player Type')
    ax6.set_ylabel('Count')
    ax6.set_xticks(x)
    ax6.set_xticklabels(['Novice', 'Balanced', 'Skilled', 'Expert'])
    ax6.legend()
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{int(height)}', ha='center', va='bottom')
    
    for bar in bars2:
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.show()

def create_algorithm_explanation_chart():
    """
    Create a simple flowchart showing HOW the algorithm makes decisions
    """
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # This would be better as a flowchart, but here's a simple decision tree visualization
    ax.text(0.5, 0.9, '🎮 Bathala DDA Decision Process', ha='center', va='center', 
            fontsize=16, fontweight='bold', transform=ax.transAxes)
    
    # Decision flow
    decision_steps = [
        "1. Player finishes combat",
        "2. Calculate Performance Delta:",
        "   • HP retention (+0.18 if >90%, -0.2 if <20%)",
        "   • Turn efficiency (+0.1 if <5 turns, -0.1 if >8)",
        "   • Hand quality (Straight Flush +0.5, High Card -0.1)",
        "   • Synergy usage (+0.1 if used)",
        "   • Resource management (+0.08 optimal, -0.15 wasted)",
        "3. Update PPS Score (bounded -2.5 to +9.0)",
        "4. Apply decay/escape hatch if needed",
        "5. Calculate new Difficulty Tier (0-5)",
        "6. Adjust game parameters:",
        "   • Enemy HP: 0.75x to 1.35x",
        "   • Enemy Damage: 0.8x to 1.2x", 
        "   • Shop Prices: 20% discount to normal",
        "   • Rewards: 85% to 100%"
    ]
    
    y_pos = 0.8
    for step in decision_steps:
        if step.startswith('   •'):
            ax.text(0.3, y_pos, step, ha='left', va='center', fontsize=10, 
                   transform=ax.transAxes, style='italic')
        elif step.startswith('  '):
            ax.text(0.2, y_pos, step, ha='left', va='center', fontsize=10, 
                   transform=ax.transAxes)
        else:
            ax.text(0.1, y_pos, step, ha='left', va='center', fontsize=12, 
                   fontweight='bold', transform=ax.transAxes)
        y_pos -= 0.05
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    plt.tight_layout()
    plt.show()

# Example of how to use these improved visualizations:
"""
# Replace the existing plot functions with:
plot_algorithm_story(all_responses)
create_algorithm_explanation_chart()
"""
