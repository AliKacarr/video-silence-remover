import json
import os
import sys
from pathlib import Path
import subprocess
import shutil
from typing import List, Optional, Set, Tuple


BASE_DIR = Path(__file__).resolve().parent

_resolution_logged: Set[Tuple[int, str]] = set()


def _is_under_project_ffmpeg(binary_path: str) -> bool:
    try:
        p = Path(binary_path).resolve()
    except OSError:
        return False
    root = BASE_DIR / "ffmpeg"
    if not root.is_dir():
        return False
    try:
        p.relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _ffmpeg_tool_source_label(binary_path: str) -> str:
    """Çözümlenen ikili yoluna göre kullanıcıya gösterilecek kaynak etiketi."""
    if _is_under_project_ffmpeg(binary_path):
        return "proje dizinindeki ffmpeg klasoru"
    try:
        if Path(binary_path).expanduser().is_file():
            return "sistem (PATH veya tam yol)"
    except OSError:
        pass
    return "komut adi (shell PATH)"


def announce_ffmpeg_tool_resolution(kind: str, binary_path: str) -> None:
    """Hangi ffprobe/ffmpeg ikilisinin kullanildigini stderr'e islem basina bir kez yazar."""
    key = (os.getpid(), kind)
    if key in _resolution_logged:
        return
    _resolution_logged.add(key)
    label = _ffmpeg_tool_source_label(binary_path)
    try:
        shown = str(Path(binary_path).expanduser().resolve())
    except OSError:
        shown = binary_path
    print(
        f"[ffmpeg] Kullanilan {kind}: {shown} — kaynak: {label}",
        file=sys.stderr,
        flush=True,
    )


def _sanitize_which_media_tool(cmd_base: str, which_path: Optional[str]) -> Optional[str]:
    """shutil.which bazen ffprobe.py gibi Python modulunu dondurur; gercek ikiliyi sec."""
    if not which_path:
        return None
    p = Path(which_path)
    name_low = p.name.lower()
    if p.suffix.lower() == ".py" or name_low == f"{cmd_base}.py":
        return None
    try:
        shadow = BASE_DIR / f"{cmd_base}.py"
        if shadow.is_file() and p.resolve() == shadow.resolve():
            return None
    except OSError:
        pass
    return str(p.resolve())


def which_media_tool_from_path(cmd_base: str) -> Optional[str]:
    """PATH uzerinden ffprobe/ffmpeg ikilisini bul (proje ffprobe.py golgesinden kacin)."""
    names: List[str] = []
    if os.name == "nt":
        names.append(f"{cmd_base}.exe")
    names.append(cmd_base)
    seen: Set[str] = set()
    for n in names:
        if n in seen:
            continue
        seen.add(n)
        w = shutil.which(n)
        hit = _sanitize_which_media_tool(cmd_base, w)
        if hit:
            return hit
    # which bazen cwd / PATHEXT yuzunden yanlis doner; PATH dizinlerini elle tara
    if os.name == "nt":
        exe = f"{cmd_base}.exe"
        for part in os.environ.get("PATH", "").split(os.pathsep):
            if not part.strip():
                continue
            cand = Path(part) / exe
            if cand.is_file():
                hit = _sanitize_which_media_tool(cmd_base, str(cand))
                if hit:
                    return hit
    return None


def _resolve_ffprobe_binary() -> str:
    from_path = which_media_tool_from_path("ffprobe")
    if from_path:
        return from_path

    candidates = [
        BASE_DIR / "ffmpeg" / "bin" / ("ffprobe.exe" if os.name == "nt" else "ffprobe"),
        BASE_DIR / "ffmpeg" / ("ffprobe.exe" if os.name == "nt" else "ffprobe"),
    ]

    for c in candidates:
        if c.is_file():
            return str(c)

    return "ffprobe"


FFPROBE_BIN = _resolve_ffprobe_binary()
announce_ffmpeg_tool_resolution("ffprobe", FFPROBE_BIN)


def _get_json(path):
    result = subprocess.run(
        [FFPROBE_BIN, path, '-loglevel', 'quiet', '-print_format', 'json', '-show_streams'],
        stdout=subprocess.PIPE,
    )
    result.check_returncode()
    return json.loads(result.stdout)

def get_resolution(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            return stream['width'], stream['height']

def get_frames(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            if 'nb_frames' in stream:
                return int(stream['nb_frames'])

def get_duration(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            if 'duration' in stream:
                return float(stream['duration'])
            else:
                parts = stream['tags']['DURATION'].split(':')
                assert len(parts) == 3
                return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])

def get_frame_rate(path):
    for stream in _get_json(path)['streams']:
        if stream['codec_type'] == 'video':
            if 'avg_frame_rate' in stream:
                assert stream['avg_frame_rate'].count('/') <= 1
                parts = stream['avg_frame_rate'].split('/')
                result = float(parts[0])
                if len(parts) == 2:
                    result /= float(parts[1])
                return result
