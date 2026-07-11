"""
Obscura — Wrapper API autour de yt_agent.py
"""
import sys, json, uuid, time, re
from pathlib import Path
sys.path.insert(0, "/Users/user/Desktop/yt-agent")
from yt_agent import assemble, VOICE_DEFAULT, STORIES, OUT

HERE = Path(__file__).parent

# Prompts Pexels variés pour chaque beat
IMAGE_PROMPTS = [
    "dark eerie forest at night with fog, cinematic, spooky atmosphere",
    "abandoned haunted house in the dark, moonlight, creepy atmosphere",
    "old cemetery with fog and graves at night, horror, cinematic",
    "dark figure silhouette in misty alleyway, streetlamp, mysterious",
    "old mirror reflecting a dark room in an abandoned house, horror",
    "creepy basement stairs leading into darkness, horror atmosphere",
    "dark road in the forest at night with headlights, mysterious",
    "old church at night with full moon, gothic, horror atmosphere",
    "foggy graveyard with ancient tombstones, dark sky, haunting",
    "broken window in abandoned building, darkness inside, creepy",
    "dark figure standing at the end of a hallway, horror, suspense",
    "old well in a misty field at twilight, mysterious atmosphere",
    "door slightly open revealing darkness inside, abandoned house",
    "dark trees silhouetted against a stormy night sky, horror",
    "old photograph on dusty table in abandoned room, creepy",
    "empty swing moving in the wind in a foggy park at night",
    "shadow of a hand on a wall in a dimly lit room, horror",
    "dark water reflecting moonlight, mysterious lake at night",
    "old staircase in an abandoned building, eerie, cinematic",
    "single candle burning in a dark room, shadows, mystery",
]

def generate_video_from_prompt(prompt: str, voice: str = VOICE_DEFAULT) -> dict:
    slug = f"obs_{uuid.uuid4().hex[:8]}"
    # Découpe intelligente en phrases
    sents = re.split(r'(?<=[.!?])\s+', prompt.replace('\n', ' ').strip())
    sents = [s.strip() for s in sents if len(s.strip()) > 5]
    if not sents:
        sents = [prompt]
    beats = []
    for i, sent in enumerate(sents):
        beats.append({
            "img": f"{slug}_b{i}.png",
            "prompt": IMAGE_PROMPTS[i % len(IMAGE_PROMPTS)],
            "voix": sent,
            "texte": ""
        })
    # Beat final
    beats.append({
        "img": f"{slug}_end.png",
        "prompt": "dark mysterious silhouette in fog at night, haunting atmosphere",
        "voix": "Abonne-toi pour plus d'histoires effrayantes.",
        "texte": "Abonne-toi"
    })
    story = {"slug": slug, "voice": voice, "beats": beats}
    story_path = STORIES / f"{slug}.json"
    story_path.write_text(json.dumps(story, ensure_ascii=False), encoding="utf-8")
    start = time.time()
    video_path = assemble(story)
    elapsed = time.time() - start
    return {"slug": slug, "path": str(video_path), "duration_sec": round(elapsed)}
