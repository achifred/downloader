import shutil
import subprocess
import sys

from src.utils import PROJECT_ROOT , get_path

SRC_DIR = get_path("src")
ENTRY_POINT = get_path("src/downloader.py")
DIST_DIR = get_path("dist")
BUILD_DIR = get_path("build")

def build_executable():
  for path in (DIST_DIR, BUILD_DIR):
    if path.exists():
      shutil.rmtree(path)

  spec_file = get_path("downloader.spec")
  if spec_file.exists():
    spec_file.unlink()


  if not ENTRY_POINT.is_file():
    raise FileNotFoundError(f"entry point not found: {ENTRY_POINT}")

  command = [ sys.executable ,
              "-m" ,
              "PyInstaller" ,
              "--name" ,
              "downloader" ,
              "--noconfirm" ,
              "--clean" ,
              "--paths" ,
              str( SRC_DIR ) ,
              str( ENTRY_POINT ),
              "--onefile" ,
            ]

  print("Building standalone executable...")
  print("Command:", " ".join(command))
  subprocess.run(command, cwd = PROJECT_ROOT, check = True)
  print("Done.")


def main():
  try:
    build_executable()
  except Exception as e:
    print(f"build executable not found: {e}")
    raise SystemExit(1)

if __name__ == '__main__':
    main()

