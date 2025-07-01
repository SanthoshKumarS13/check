# main.py
import os
from content_engine import ContentFetcher
from ai_engine import AIProcessor
from media_engine import MediaFetcher
from video_engine import create_reel
from analysis_engine import save_post_data, run_weekly_analysis
from state_manager import StateManager
from config import OUTPUT_DIR_VIDEO

def main():
    print("🚀 Starting NextGen Signals AI Reel Engine v3.0...")

    # --- Initialization ---
    state_manager = StateManager()
    content_fetcher = ContentFetcher()
    ai_processor = AIProcessor()
    media_fetcher = MediaFetcher()

    # --- Weekly Analysis & Strategy ---
    run_weekly_analysis(state_manager)

    # --- Content & Style Selection ---
    category, story_style_prompt = state_manager.get_next_story_style()
    edit_style_key, edit_style_params = state_manager.get_next_editing_style()
    print(f"🎬 Category: {category} | Story: '{state_manager.get_last_story_key()}' | Edit: '{edit_style_key}'")

    article = content_fetcher.fetch_random_article(category)
    if not article:
        print("-> Could not fetch an article. Stopping run.")
        return

    # --- AI Content Generation ---
    print("🧠 Generating script with AI...")
    hook, revelation = ai_processor.generate_hook_and_revelation(article['summary'], story_style_prompt)
    if not hook or not revelation:
        print("-> AI failed to generate script. Stopping run.")
        return
    print(f"   - Hook: {hook}\n   - Revelation: {revelation}")

    # --- Media Sourcing ---
    print("🎥 Sourcing video and music...")
    search_query = f"abstract technology {category}"
    video_path, video_credit = media_fetcher.get_video(search_query)
    music_path, music_credit = media_fetcher.get_music("upbeat electronic tech")
    if not video_path or not music_path:
        print("-> Failed to source media. Stopping run.")
        return

    # --- Reel Composition ---
    print(f"🎞️ Composing video with '{edit_style_key}' style...")
    os.makedirs(OUTPUT_DIR_VIDEO, exist_ok=True)
    post_id = f"{category.replace(' ', '')}_{state_manager.get_run_count()}"
    output_video_path = os.path.join(OUTPUT_DIR_VIDEO, f"{post_id}.mp4")

    success = create_reel(video_path, music_path, hook, revelation, output_video_path, edit_style_params)
    if not success:
        print("-> Failed to create video file. Stopping run.")
        return

    # --- Caption & Hashtags ---
    print("✍️ Generating caption and hashtags...")
    media_credit_info = f"Video by {video_credit}, Music by {music_credit}" if video_credit and music_credit else "Pexels/Pixabay"
    caption = ai_processor.generate_caption(hook, revelation, article['source'], media_credit_info)
    hashtags = ai_processor.generate_hashtags(f"{category} {hook}")

    # --- Save Data for Analysis ---
    save_post_data(post_id, category, state_manager.get_last_story_key(), edit_style_key, hook, caption, hashtags)
    print(f"✅ Post data saved for {post_id}.")

    # --- Update State for Next Run ---
    state_manager.increment_run_count()
    print("\n✨ Process complete. Ready for next run.")

if __name__ == "__main__":
    main()