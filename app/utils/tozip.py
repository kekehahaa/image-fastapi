import zipfile

from pathlib import Path

def file_to_zip(path: Path):
    path = Path(path)
    zipname = f'{path.stem}.zip'
    with zipfile.ZipFile(zipname, 'w') as zf:
        if path.is_file():
            zf.write(path, path.name)
        elif path.is_dir():
            for file in path.rglob('*'):
                zf.write(file, file.relative_to(path))
    return zipname

def delete_zip_file(path: str):
    Path(path).unlink()
