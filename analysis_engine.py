# analysis_engine.py
import pandas as pd
import os
import json
import random
from config import ALL_POSTS_EXCEL_FILE, ANALYSIS_REPORT_FILE, OUTPUT_DIR_DATA

def save_post_data(post_id, category, story_style, edit_style, hook, caption, hashtags):
    os.makedirs(OUTPUT_DIR_DATA, exist_ok=True)
    
    new_post = {
        "Post_ID": post_id,
        "Category": category,
        "Story_Style": story_style,
        "Editing_Style": edit_style,
        "Hook": hook,
        "Caption": caption,
        "Hashtags": ' '.join(hashtags),
        "Timestamp": pd.to_datetime("now", utc=True).isoformat(),
        # SIMULATED METRICS FOR ANALYSIS
        "Views": random.randint(5000, 25000),
        "Likes": random.randint(200, 2000),
        "Comments": random.randint(20, 150),
        "Shares": random.randint(10, 100),
    }

    try:
        df = pd.read_excel(ALL_POSTS_EXCEL_FILE) if os.path.exists(ALL_POSTS_EXCEL_FILE) else pd.DataFrame()
        df_new = pd.DataFrame([new_post])
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_excel(ALL_POSTS_EXCEL_FILE, index=False)
    except Exception as e:
        print(f"Error saving to Excel: {e}")

def run_weekly_analysis(state_manager):
    if not state_manager.should_run_analysis():
        return

    print("📊 Running Weekly Performance Analysis...")
    if not os.path.exists(ALL_POSTS_EXCEL_FILE):
        print("-> No post data to analyze.")
        return

    df = pd.read_excel(ALL_POSTS_EXCEL_FILE)
    if len(df) < 5: # Don't run analysis without enough data
        print(f"-> Not enough data for analysis ({len(df)} posts). Needs at least 5.")
        return

    df['engagement_score'] = (df['Likes'] * 0.2) + (df['Comments'] * 0.5) + (df['Shares'] * 0.3)
    
    story_performance = df.groupby('Story_Style')['engagement_score'].mean().sort_values(ascending=False)
    edit_performance = df.groupby('Editing_Style')['engagement_score'].mean().sort_values(ascending=False)
    
    best_story_style = story_performance.index[0]
    best_edit_style = edit_performance.index[0]
    
    print(f"🏆 Best Story Style: '{best_story_style}' | Best Edit Style: '{best_edit_style}'")

    report = {
        "best_story_style": best_story_style,
        "best_edit_style": best_edit_style,
        "story_performance": story_performance.to_dict(),
        "edit_performance": edit_performance.to_dict()
    }
    with open(ANALYSIS_REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=4)
        
    state_manager.update_after_analysis(best_story_style, best_edit_style)