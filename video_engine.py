# video_engine.py
import moviepy.editor as mp
from moviepy.video.fx.all import crop
from PIL import Image, ImageDraw
import random
from config import REEL_DURATION_SECONDS, LOGO_PATH, LOGO_WIDTH

def create_rounded_mask(size, radius):
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0) + size, radius, fill=255)
    return mask

def create_glassmorphism_reel(video_clip, hook_text, revelation_text, style_params):
    card_w, card_h = 980, 1200
    card_size = (card_w, card_h)

    glass_card = mp.ColorClip(size=card_size, color=style_params['card_color']).set_opacity(style_params['card_opacity'])
    mask_clip = mp.ImageClip(list(create_rounded_mask(card_size, 50).getdata()), size=card_size, ismask=True)
    glass_card.set_mask(mask_clip)

    text_w = card_w * 0.9
    hook_clip = mp.TextClip(hook_text.upper(), fontsize=style_params['font_size_hook'], color=style_params['text_color'], font=style_params['font_hook'], size=(text_w, None), method='caption')
    revelation_clip = mp.TextClip(revelation_text, fontsize=style_params['font_size_revelation'], color=style_params['text_color'], font=style_params['font_revelation'], size=(text_w, None), method='caption')
    logo_clip = mp.ImageClip(LOGO_PATH).resize(width=LOGO_WIDTH)

    content_on_card = mp.CompositeVideoClip([
        hook_clip.set_position(('center', 100)),
        revelation_clip.set_position(('center', hook_clip.h + 150)),
        logo_clip.set_position(('center', card_h - logo_clip.h - 50))
    ], size=card_size, use_bgclip=False).set_position('center')

    final_clip = mp.CompositeVideoClip([glass_card.set_position('center'), content_on_card])
    return final_clip.set_duration(video_clip.duration).fadein(0.5).fadeout(0.5)

def create_kinetic_reel(video_clip, hook_text, revelation_text, style_params):
    bg_video = mp.CompositeVideoClip([
        video_clip,
        mp.ColorClip(video_clip.size, color=(0,0,0)).set_opacity(style_params['background_opacity'])
    ]).set_duration(video_clip.duration)

    hook_clips, revelation_clips = [], []
    words = hook_text.upper().split()
    start_time = 0.5
    for word in words:
        clip = mp.TextClip(word, fontsize=style_params['font_size_hook'], color=style_params['text_color'], font=style_params['font_hook'])
        clip = clip.set_position('center').set_start(start_time).set_duration(2.5).fadein(0.2).fadeout(0.2)
        hook_clips.append(clip)
        start_time += 0.3

    words = revelation_text.split()
    start_time += 0.2
    for word in words:
        color = style_params['highlight_color'] if len(word) > 4 else style_params['text_color']
        clip = mp.TextClip(word, fontsize=style_params['font_size_revelation'], color=color, font=style_params['font_revelation'])
        clip = clip.set_position('center').set_start(start_time).set_duration(0.45).fadein(0.1)
        revelation_clips.append(clip)
        start_time += 0.25

    logo_clip = mp.ImageClip(LOGO_PATH).resize(width=LOGO_WIDTH)
    logo_clip = logo_clip.set_position(('center', 'bottom')).set_start(start_time + 0.5).set_duration(3).fadein(0.5)

    return mp.CompositeVideoClip([bg_video] + hook_clips + revelation_clips + [logo_clip])

def create_reel(video_path, music_path, hook_text, revelation_text, output_path, style_params):
    try:
        video_clip = mp.VideoFileClip(video_path).without_audio()
        audio_clip = mp.AudioFileClip(music_path).volumex(0.4)
        final_duration = min(video_clip.duration, REEL_DURATION_SECONDS)

        (w, h) = video_clip.size
        target_ratio = 1080 / 1920
        if w / h > target_ratio:
            video_clip = crop(video_clip, width=int(h * target_ratio), x_center=w/2)
        else:
            video_clip = crop(video_clip, height=int(w / target_ratio), y_center=h/2)
        video_clip = video_clip.resize((1080, 1920)).set_duration(final_duration)
        
        audio_segment = audio_clip
        if audio_clip.duration > final_duration:
            max_start_time = audio_clip.duration - final_duration
            start_time = random.uniform(0, max_start_time)
            audio_segment = audio_clip.subclip(start_time, start_time + final_duration)
            print(f"   - Audio clipped from {start_time:.2f}s to {start_time + final_duration:.2f}s")

        style_function_name = style_params.get("function")
        if style_function_name == "create_glassmorphism_reel":
            final_content_clip = create_glassmorphism_reel(video_clip, hook_text, revelation_text, style_params)
        elif style_function_name == "create_kinetic_reel":
            final_content_clip = create_kinetic_reel(video_clip, hook_text, revelation_text, style_params)
        else:
            raise ValueError(f"Unknown style function: {style_function_name}")

        final_video = mp.CompositeVideoClip([video_clip, final_content_clip])
        final_video.audio = audio_segment.set_duration(final_duration)
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True, logger='bar')

        print(f"Reel created successfully at {output_path}")
        return True

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error creating reel: {e}")
        return False
