import logging
from logging.handlers import RotatingFileHandler
from src.utils import get_root_path

MAX_LOG_FILE_SIZE = 10 * 1024 * 1024

PROJECT_ROOT = get_root_path()
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir( parents = True , exist_ok = True )


def get_logger ( name: str="script" , log_file: str="script_log" , log_level = logging.INFO ) :
  logger = logging.getLogger( name )

  # to prevent duplicate handlers
  if logger.handlers :
    return logger

  logger.setLevel( log_level )
  formatter = logging.Formatter(
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s" ,
    datefmt = "%Y-%m-%d %H:%M:$S"
  )

  log_file_path = LOG_DIR / log_file

  console_handler = logging.StreamHandler()
  file_handler = RotatingFileHandler(
    filename = log_file_path ,
    maxBytes = MAX_LOG_FILE_SIZE ,
    backupCount = 100 ,
    mode = "a"

  )

  console_handler.setFormatter( fmt = formatter )
  file_handler.setFormatter( fmt = formatter )
  logger.addHandler( console_handler )
  logger.addHandler( file_handler )
  logger.propagate = False

  return logger
