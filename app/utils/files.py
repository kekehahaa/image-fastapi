import os, aiofiles, mimetypes, shutil

from fastapi import HTTPException, status, UploadFile
from fastapi.responses import FileResponse
from yt_dlp.utils import DownloadError
from pathlib import Path

import app.utils.constants as cnst
import app.api.validators  as val
import app.utils.videocutter as vdc

from app.utils.utubedownloader import donwload_video_async
from app.utils.tozip import file_to_zip
from app.core.config import settings

async def upload_video_local(file: UploadFile):
    val.check_file_data(file)  # check if file is uploaded
    val.check_video_format(file)  # check if file is video
    path = settings.DB_PATH
    full_path = Path(path) / Path(file.filename).stem
    if full_path.exists():
        shutil.rmtree(full_path)
    full_path.mkdir()
    full_path = full_path / file.filename
    try:
        content = file.file.read()
        async with aiofiles.open(full_path, 'wb') as f:
            await f.write(content)
    except OSError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=cnst.BAD_W_FILE.format(full_path.stem)
        )
    finally:
        await f.close()
        file.file.close()
    return full_path.relative_to(path)

async def upload_video_link(link: str):
    val.check_youtube_link(link)
    path = Path(settings.DB_PATH)
    try:
        video_file = await donwload_video_async(link, path)
    except DownloadError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=cnst.BAD_W_FILE.format(path)
        )
    return Path(video_file).relative_to(path)

async def cut_video_to_frames(path: str, fps: float, save_pattern: str, frame_path: str | None = None, download: bool = False):
    file = Path(settings.DB_PATH) / Path(path)
    video = vdc.VideoCutter(file)
    if frame_path is None:
        frame_path = file.parent / Path("frames")
    await video.video_to_frames(frame_path, fps, save_pattern)
    if download:
        file = file_to_zip(frame_path)
        return FileResponse(file, media_type="application/zip", filename=Path(file).stem)
    frames = list(map(str, frame_path.glob("*")))
    for i in range(len(frames)):
        frames[i] = Path(frames[i]).relative_to(settings.DB_PATH)
    return frames

async def get_all_videos():
    videos = list(map(str,(Path(settings.DB_PATH).glob("*"))))
    for i in range(len(videos)):
        videos[i] = Path(videos[i]).relative_to(settings.DB_PATH)
    return videos

async def cut_video_timecodes(path: str, timecodes: list):
    file = Path(settings.DB_PATH) / Path(path)
    video = vdc.VideoCutter(file)
    for timecode in timecodes:
        if float(video.file_info['format']['duration']) < timecode[1]:
            shutil.rmtree(file.parent)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid timecodes, > duration video.")
    out_path = file.parent / Path("timecodes")
    await video.cut_by_timecodes(out_path, timecodes)
    return Path(out_path).relative_to(settings.DB_PATH)