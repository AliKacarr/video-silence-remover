# Video Sessizlik Kaldırıcı

Videolarınızdaki sessiz anları otomatik tespit edip kısaltır. Tarayıcıdan dosya yükleyebilir, gelişmiş eşik ayarlarını kullanabilir ve işlenmiş videoyu indirebilirsiniz.

## Gereksinimler

- **Python** 3.10+ önerilir  
- **FFmpeg**

## Kurulum

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install -r requirements-web.txt
```

## Web arayüzü

```bash
python web_server.py
```

Tarayıcıda açın: **http://127.0.0.1:5050**

## Proje yapısı

| Yol | Açıklama |
|-----|----------|
| `web_server.py` | Flask API ve arayüz |
| `templates/` | HTML şablonları |
| `video-remove-silence.py` | Sessizlik kaldırma mantığı |
| `ffprobe.py` | Süre / metadata okuma |