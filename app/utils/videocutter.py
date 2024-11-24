import os, random, shutil, string, os, asyncio
import ffmpeg as ffmpeg_probe

from ffmpeg.asyncio import FFmpeg
from pathlib import Path
from typing import List, Tuple


class VideoCutter:
    '''
    Class video manupulations
    '''
    def __init__(self, file_path: str):
        self.file_path = file_path
        
        if not Path(self.file_path).is_file():
            raise FileNotFoundError(f"File {self.file_path} not found")
        
        self.file_info = self._get_video_info()
    
    async def video_to_frames(self, output_path: str, fps: int | float=1.5, save_pattern: str=f'frame_%05d.jpg'):
        '''
        Cut video into photos(frames)
        
        Parameters
        ----------
        output_path : str
            Path to directory where saving frames
        fps : Union[float, int]
            Frequancy. The default is 1.5
        save_pattern : str
            Pattern to save frames. The default is f'frame_%04d.jpg'
        '''
        out_path = Path(output_path)
        if not out_path.exists():
            out_path.mkdir(parents=True)
            
        try:
            process = (
            FFmpeg()
            .option("threads", str(os.cpu_count()))
            .input(self.file_path)
            .output(out_path / save_pattern, vf=f"fps={fps}", qscale=0)
            )     
            await process.execute()
            return out_path
        except ffmpeg_probe.Error as e:
            print(f"Error while cutting into frames: {e}")
            
    async def video_cut(self, output_name: str, start: int | float, end: int | float):
        '''
        Cut video by interval from start to end
        
        Parameters
        ----------
        output_name : str
             Name to save new video
        start : Union[int, float]
            Start from sec to cutting
        end : Union[int, float]
            End sec to cutting
        '''
        try:
            process = (
            FFmpeg()
            .option("threads", str(os.cpu_count()))
            .input(self.file_path, ss=start, to=end)
            .output(output_name, codec="copy")
            )     
            await process.execute()
            print(f"Video saved: {output_name}")
        except ffmpeg_probe.Error as e:
            print(f"Error while cutting video: {e}")
        except Exception as ex:
            print(ex)
            
    async def cut_by_duration(self, output_path: str, duration: int | float):
        '''
        Cut video by intervals
        
        Parameters
        ----------
        output_path : str
            Path to directory where saving videos
        duration : Union[int, float]
            Length to cut videos
        '''
        out_path = Path(output_path)
        if not out_path.exists():
            out_path.mkdir(parents=True) 
        
        count = int(float(self.file_info['format']['duration']) // duration)
        rndm = ''.join(random.choices(string.ascii_letters, k=7))
        extention = Path(self.file_path).suffix
        
        if count <= 1:
            shutil.copy(self.file_path, output_path)
            return
                 
        for i in range(count + 1):
            start = i * duration
            end = start + duration
            await self.video_cut(out_path / f"video_{rndm}_{i}{extention}", start, end)
    
    async def cut_by_parts(self, output_path: str, parts: int):
        '''
        Parameters
        ----------
        output_path : str
            Path to directory where saving videos
        parts : int
            This is the number of parts you need to divide the video into
        '''
        out_path = Path(output_path)
        if not out_path.exists():
            out_path.mkdir(parents=True)
        
        rndm = ''.join(random.choices(string.ascii_letters, k=7))
        extention = Path(self.file_path).suffix
        duration = float(self.file_info['format']['duration']) / parts
            
        for i in range(parts):
            start = i * duration
            end = start + duration
            await self.video_cut(out_path / f"video_{rndm}_{i}{extention}", start, end)
            
    async def cut_by_timecodes(self, output_path, timecodes: List[Tuple[float]]):
        out_path = Path(output_path)
        if not out_path.exists():
            out_path.mkdir(parents=True)
            
        rndm = ''.join(random.choices(string.ascii_letters, k=7))
        extention = Path(self.file_path).suffix
        
        i = 0
        for start, end in timecodes:
            await self.video_cut(out_path / f"video_{rndm}_{i}{extention}", start, end)
            i += 1
        return out_path
        
    def _get_video_info(self):
        return ffmpeg_probe.probe(self.file_path)
    
if __name__ == "__main__":
    file_path = "../../Лекция. Сверточные нейронные сети.mp4"
    out_path = "../../detection/web_db/video_cat"
    video = VideoCutter(file_path)
    # asyncio.run(video.video_to_frames("../web_db/frames", 1/1000, f'video_%04d.jpg'))
    # asyncio.run(video.video_cut(out_path + "1.mp4", 1, 6))
    # asyncio.run(video.cut_by_duration(out_path, 300))
    # asyncio.run(video.cut_by_parts(out_path, 15))
    asyncio.run(video.cut_by_timecodes(out_path, [(11, 20), (300, 600)]))
    
