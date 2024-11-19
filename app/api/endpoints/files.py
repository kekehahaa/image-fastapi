import app.utils.files as lgc

from fastapi import APIRouter, UploadFile, Body, File,  BackgroundTasks
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.schemas.files import UploadLocal, UploadLink
from app.core.config import settings
from app.utils.tozip import file_to_zip, delete_zip_file

file_router = APIRouter(prefix='/video')

# POST

@file_router.post("/upload/local")
async def proccess_upload_video_local(background_tasks: BackgroundTasks,
                                      video_settings: UploadLocal = Body(),
                                      video_file: UploadFile = File(...),):
    path = await lgc.upload_video_local(video_file)
    if video_settings.timecodes is None:
        frames = await lgc.cut_video_to_frames(path, video_settings.fps, video_settings.save_pattern)
    else:
        videos = await lgc.cut_video_timecodes(path, video_settings.timecodes)
        videos = list(map(str, (Path(settings.DB_PATH) / videos).glob("*")))
        i = 0
        frames = []
        for video in videos:
            save_pattern = f'frame{i}_%05d.jpg'
            frame = await lgc.cut_video_to_frames(video, 
                                          video_settings.fps, 
                                          save_pattern, 
                                          frame_path=((Path(settings.DB_PATH) / video).parent.parent) / Path("frames"))
            i += 1
        frames += frame
    if video_settings.zipped:
        zipped_path = file_to_zip(Path(settings.DB_PATH) / path.parent / Path("frames"))
        background_tasks.add_task(delete_zip_file, zipped_path)
        return FileResponse(zipped_path, media_type="application/zip", filename=Path(zipped_path).stem)
    return frames

@file_router.post("/upload/link")
async def upload_video_by_link(background_tasks: BackgroundTasks,
                               video_link: UploadLink):
    path = await lgc.upload_video_link(video_link.link)
    if video_link.timecodes is None:
        frames = await lgc.cut_video_to_frames(path, video_link.fps, video_link.save_pattern)
    else:
        videos = await lgc.cut_video_timecodes(path, video_link.timecodes)
        videos = list(map(str, (Path(settings.DB_PATH) / videos).glob("*")))
        i = 0
        frames = []
        for video in videos:
            save_pattern = f'frame{i}_%05d.jpg'
            frame = await lgc.cut_video_to_frames(video, 
                                          video_link.fps, 
                                          save_pattern, 
                                          frame_path=((Path(settings.DB_PATH) / video).parent.parent) / Path("frames"))
            i += 1
        frames += frame
    if video_link.zipped:
        zipped_path = file_to_zip(Path(settings.DB_PATH) / path.parent / Path("frames"))
        background_tasks.add_task(delete_zip_file, zipped_path)
        return FileResponse(zipped_path, media_type="application/zip", filename=Path(zipped_path).stem)
    return frames

@file_router.get("/select/all")
async def proccess_select_video_all():
    response = await lgc.get_all_videos()
    return response
