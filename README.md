# Video Sessizlik Kaldırıcı

Videolarınızdaki sessiz alanları otomatik tespit edip kısaltır. Tarayıcı üzerinden video yükleyebilir, ses değerlerini ayarlayabilir ve işlenmiş çıktıyı indirebilirsiniz.

## Web arayüzünden kullanım

1. Uygulamayı başlatın:

```bash
python web_server.py
```

Windows'ta isterseniz `start.bat` kısayolu ile tek tıkla başlatabilirsiniz.

2. Tarayıcıdan açın: `http://127.0.0.1:5050`
3. Video dosyasını yükleyin.
4. İsterseniz ses eşik ayarlarını değiştirin:
   - `threshold_level`: sessizlik eşiği (dB)
   - `threshold_duration`: minimum sessizlik süresi (sn)
5. İşlem tamamlanınca:
   - önizleme yapın,
   - işlenmiş videoyu indirin.

## Komut satırından kullanım

Temel kullanım (aynı klasördeki dosya):

```bash
python video-remove-silence.py "ornek.mp4"
```

Tam yol ile kullanım (Windows):

```bash
python video-remove-silence.py "C:\Users\Ali\videos\ornek.mp4"
```

Ses eşik ayarları ile:

```bash
python video-remove-silence.py "ornek.mp4" --threshold-level -35 --threshold-duration 0.6
```

Çıktı dosyası aynı klasörde `*_result` ekiyle oluşturulur.

## Gereksinimler

- **Python** 3.10+
- **Flask** 3.1+
- **FFmpeg** 8.1+

## Flask Yapılandırması

Flask kuruluysa uygulama doğrudan çalışır. Kurulu değilse gerekli kurulum otomatik olarak başlatılır.

## FFmpeg Yapılandırması

Sistemde FFmpeg varsa cihazdaki kurulum kullanılır. FFmpeg yoksa proje içindeki FFmpeg 8.1 devreye girer.

## Sorun giderme

- **Yükleme limiti hatası (413)**: `MAX_UPLOAD_GB` ortam değişkenini artırın (ör. `MAX_UPLOAD_GB=32`).
- **FFmpeg bulunamadı**: Cihazınıza güncel FFmpeg indirip ortam değişkenlerine (PATH) ekleyin.
- **Uzun işlem süresi**: Büyük videolarda işlem süresi uzayabilir; işlem durumu arayüzden takip edilebilir.

## Proje yapısı

| Yol | Açıklama |
|-----|----------|
| `web_server.py` | Flask API, yükleme ve iş kuyruğu yönetimi |
| `templates/` | Web arayüzü HTML şablonları |
| `video-remove-silence.py` | Sessizlik tespiti ve video yeniden kurgulama |
| `ffprobe.py` | Video metadata/süre çözümleme yardımcıları |
| `ffmpeg/` | Gömülü FFmpeg ikilileri ve dökümantasyon |