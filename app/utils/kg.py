# ✅ utils/kg.py

def enrich_with_knowledge_graph(text: str) -> str:
    # Mock knowledge graph logic (can be replaced with real KG lookup)
    tone_mapping = {
        "fun": "Use emojis, puns, and casual language.",
        "professional": "Keep language formal and focused on business benefits.",
        "trendy": "Use pop culture references and current slang."
    }

    platform_rules = {
        "Instagram": "Keep it short. Use hashtags and visual references.",
        "LinkedIn": "Use formal tone. Emphasize career and growth impact.",
        "Twitter": "Fit within 280 characters. Use trending tags."
    }

    enrichment = ""
    for tone, tip in tone_mapping.items():
        if tone in text:
            enrichment += f"\nTone Tip: {tip}"

    for platform, rule in platform_rules.items():
        if platform.lower() in text.lower():
            enrichment += f"\nPlatform Tip: {rule}"

    return text + enrichment
