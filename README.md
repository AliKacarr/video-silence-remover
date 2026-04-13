# Video Sessizlik Kaldırıcı

Videolarınızdaki sessiz anları otomatik tespit edip kısaltır. Tarayıcı üzerinden video yükleyebilir, ses değerlerini ayarlayabilir ve işlenmiş çıktıyı indirebilirsiniz.

# Kullanım akışı

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

Temel kullanım:

```bash
python video-remove-silence.py "ornek.mp4"
```

Örnek (eşik ayarları ile):

```bash
python video-remove-silence.py "ornek.mp4" --threshold-level -35 --threshold-duration 0.6
```

Çıktı dosyası aynı klasörde `*_result` ekiyle oluşturulur.

## Gereksinimler

- **Python** 3.1+
- **Flask** 3.1+
- **FFmpeg** 8.1+

Not: İlk çalıştırmada bilgisayarınızda Flask kurulu değilse otomatik kurulmaya çalışılır.

## FFmpeg kullanımı

FFmpeg arama sırası iki adımdır:

1. Önce sistemde kurulu FFmpeg (`PATH`) kullanılır.
2. Cihazda FFmpeg yoksa proje içindeki `ffmpeg` klasörü devreye girer.

Proje klasöründe kullanılan ikililer:

- `ffmpeg/bin/ffmpeg(.exe)`
- `ffmpeg/bin/ffprobe(.exe)`

Bu sayede kullanıcının cihazında FFmpeg varsa doğrudan onu kullanır; yoksa depodaki FFmpeg 8.1 dosyalarıyla devam eder.

## Sorun giderme

- **Yükleme limiti hatası (413)**: `MAX_UPLOAD_GB` ortam değişkenini artırın (ör. `MAX_UPLOAD_GB=32`).
- **FFmpeg bulunamadı**: `ffmpeg/bin` altındaki dosyaların mevcut olduğunu doğrulayın veya sistem PATH'inize FFmpeg ekleyin.
- **Uzun işlem süresi**: Büyük videolarda işlem süresi uzayabilir; işlem durumu arayüzden takip edilebilir.

## Proje yapısı

| Yol | Açıklama |
|-----|----------|
| `web_server.py` | Flask API, yükleme ve iş kuyruğu yönetimi |
| `templates/` | Web arayüzü HTML şablonları |
| `video-remove-silence.py` | Sessizlik tespiti ve video yeniden kurgulama |
| `ffprobe.py` | Video metadata/süre çözümleme yardımcıları |
| `ffmpeg/` | Gömülü FFmpeg ikilileri ve dökümantasyon |