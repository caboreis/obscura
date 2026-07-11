# OBSCURA 🎬🔥

API de génération de vidéos YouTube Shorts d'horreur en français.
Photos réelles Pexels + voix neurale Edge-TTS + crossfade + sous-titres.

**Démo en ligne :** [curly-ravens-repair.loca.lt](https://curly-ravens-repair.loca.lt)

## Déploiement 1-clic

Clique sur ce bouton → connecte ton GitHub → c'est en ligne :

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/obscura)

Ou manuellement :

```bash
git push origin main
# 2. Va sur https://railway.app → New Project → Deploy from GitHub
# 3. Sélectionne le repo → Deploy
```

## API

```bash
POST /api/generate
{"prompt": "Ton histoire horrifique...", "voice": "fr-FR-HenriNeural"}

GET /api/status/{job_id}
GET /api/download/{job_id}
```

## Stack
- FastAPI + Python 3.12
- ffmpeg (intégré dans le Dockerfile)
- Pexels API + Edge-TTS (gratuits)
