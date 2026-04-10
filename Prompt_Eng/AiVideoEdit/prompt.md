# 🎬 Cinematic Car Chase – Text-to-Video Prompt

## 📌 Overview
This JSON prompt is designed for **Seedance 1.5 (OpenArt text-to-video)** to generate a high-intensity cinematic car chase scene.

---

## 🧾 Prompt Configuration

```json
{
  "prompt": "A breathtaking cinematic car chase through neon-lit city streets at night. Two sleek high-performance sports cars race at extreme speed, weaving through traffic while police cars pursue them with flashing red and blue lights. The environment is a futuristic urban city glowing with neon signs, reflections on wet asphalt, and towering skyscrapers. Dynamic aerial drone shots, fast tracking shots, and sweeping camera pans capture the intensity. Include dramatic slow-motion close-ups of tires screeching, sparks flying from metal scraping, and glowing brake discs. The atmosphere is intense, adrenaline-fueled, and cinematic, with dramatic lighting, volumetric fog, lens flares, and strong motion blur. Hollywood blockbuster style, ultra-realistic, high detail, 4K quality.",
  
  "negative_prompt": "low quality, blurry, cartoon, anime, unrealistic physics, distorted cars, bad proportions, low resolution, artifacts, glitch, watermark, text, logo",
  
  "style": "cinematic, realistic, action, blockbuster",
  
  "camera": {
    "shots": [
      "aerial drone shot",
      "tracking shot",
      "low-angle wheel close-up",
      "overhead chase view",
      "slow-motion impact shot"
    ],
    "movement": "fast-paced, dynamic, sweeping, high-speed tracking",
    "effects": [
      "motion blur",
      "lens flare",
      "depth of field",
      "slow motion"
    ]
  },
  
  "lighting": {
    "type": "neon-lit night scene",
    "details": [
      "glowing neon reflections",
      "police siren lighting",
      "high contrast shadows",
      "wet street reflections"
    ]
  },
  
  "environment": {
    "location": "futuristic city at night",
    "details": [
      "skyscrapers",
      "busy streets",
      "wet asphalt",
      "neon signs",
      "foggy atmosphere"
    ]
  },
  
  "motion": {
    "speed": "very fast",
    "intensity": "high adrenaline",
    "elements": [
      "drifting",
      "sharp turns",
      "near misses",
      "sparks and debris"
    ]
  },
  
  "render_settings": {
    "quality": "4K",
    "fps": 24,
    "duration": "5-10 seconds"
  }
}
