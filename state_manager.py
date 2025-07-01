# state_manager.py
import json
import os
import random
from datetime import datetime, timedelta, UTC
from config import (STATE_FILE, CONTENT_SOURCES, STORYTELLING_STYLES, EDITING_STYLES, ANALYSIS_INTERVAL_DAYS)

class StateManager:
    def __init__(self):
        self.state = {
            "run_count": 0,
            "last_analysis_timestamp": None,
            "category_cycle_index": 0,
            "best_performing_story_style": random.choice(list(STORYTELLING_STYLES.keys())),
            "best_performing_edit_style": random.choice(list(EDITING_STYLES.keys())),
            "last_story_key": None
        }
        self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    self.state.update(json.load(f))
                print(f"-> State loaded. Run count: {self.state['run_count']}")
            except Exception as e:
                print(f"Error loading state, using default. Error: {e}")
        else:
            print("No state file found, initializing new state.")
            self.state['last_analysis_timestamp'] = datetime.now(UTC).isoformat()
            self._save_state()

    def _save_state(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=4)

    def get_next_story_style(self):
        categories = list(CONTENT_SOURCES.keys())
        category = categories[self.state['category_cycle_index'] % len(categories)]
        
        style_key = self.state['best_performing_story_style'] if random.random() < 0.7 else random.choice(list(STORYTELLING_STYLES.keys()))
        self.state['last_story_key'] = style_key
        return category, STORYTELLING_STYLES[style_key]

    def get_next_editing_style(self):
        style_key = self.state['best_performing_edit_style'] if random.random() < 0.7 else random.choice(list(EDITING_STYLES.keys()))
        return style_key, EDITING_STYLES[style_key]
        
    def get_last_story_key(self):
        return self.state['last_story_key']

    def should_run_analysis(self):
        if not self.state.get('last_analysis_timestamp'): return True
        last_time = datetime.fromisoformat(self.state['last_analysis_timestamp'])
        return datetime.now(UTC) - last_time >= timedelta(days=ANALYSIS_INTERVAL_DAYS)

    def update_after_analysis(self, best_story, best_edit):
        self.state['last_analysis_timestamp'] = datetime.now(UTC).isoformat()
        self.state['best_performing_story_style'] = best_story
        self.state['best_performing_edit_style'] = best_edit
        self._save_state()
        print(f"-> State updated with best styles: Story='{best_story}', Edit='{best_edit}'")

    def increment_run_count(self):
        self.state['run_count'] += 1
        self.state['category_cycle_index'] += 1
        self._save_state()
        
    def get_run_count(self):
        return self.state['run_count']