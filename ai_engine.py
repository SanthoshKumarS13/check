# ai_engine.py
from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_SITE_URL, OPENROUTER_SITE_NAME

class AIProcessor:
    def __init__(self):
        if not OPENROUTER_API_KEY or "sk-or-v1" not in OPENROUTER_API_KEY:
            raise ValueError("OpenRouter API Key is missing or invalid in config.py")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

    def _make_request(self, messages, max_tokens=250):
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": OPENROUTER_SITE_URL,
                    "X-Title": OPENROUTER_SITE_NAME,
                },
                model=OPENROUTER_MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error calling AI model: {e}")
            return None

    def generate_hook_and_revelation(self, article_text, style_prompt):
        messages = [
            {"role": "system", "content": "You are a creative director for a tech-focused social media channel. Your goal is to create short, compelling video scripts from complex articles. Respond with only the Hook and the Revelation, separated by '|||'."},
            {"role": "user", "content": f"Article: \"{article_text[:2000]}\"\n\nStyle: \"{style_prompt}\"\n\nGenerate a very short, punchy Hook (max 10 words) and a detailed, easy-to-read Revelation (max 30 words) based on this style."}
        ]
        response = self._make_request(messages)
        if response and "|||" in response:
            parts = response.split("|||")
            hook = parts[0].replace("Hook:", "").strip().replace('"', '')
            revelation = parts[1].replace("Revelation:", "").strip().replace('"', '')
            return hook, revelation
        return "Could not generate script.", "Please check the AI engine."

    def generate_caption(self, hook, revelation, source_name, credit_info=None):
        credit_line = f"\n\nCredits:\n{credit_info}" if credit_info else ""
        messages = [
            {"role": "system", "content": "You are a social media manager for 'NextGen Signals' crafting viral captions for Instagram Reels. Be engaging, add value, and encourage discussion."},
            {"role": "user", "content": f"Video Script:\nHook: {hook}\nRevelation: {revelation}\n\nSource: {source_name}\n\nWrite an engaging caption. Start with a strong opening, elaborate slightly on the revelation, and end with a question to boost comments. Add a 'Follow for more tech insights!' call to action.{credit_line}"}
        ]
        return self._make_request(messages, max_tokens=150)

    def generate_hashtags(self, topic):
        messages = [
            {"role": "system", "content": "You are a hashtag expert. Generate a list of 15 relevant hashtags for a tech and AI brand, mixing popular and niche tags. Return as a comma-separated list."},
            {"role": "user", "content": f"Topic: {topic}"}
        ]
        response = self._make_request(messages, max_tokens=100)
        return [f"#{tag.strip()}" for tag in response.split(",")] if response else []