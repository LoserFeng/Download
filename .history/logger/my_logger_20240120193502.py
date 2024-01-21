import logging
import typing as tp
import sys
import os
from pathlib import Path

import colorlog

class MyLogger(logging.Logger):

    LogPath:str ="./logs"




    def __init__(self,log_name:str,log_level: int =logging.DEBUG) ->None:
        super().__init__(log_name)
        # 创建一个日志器logger并设置其日志级别为DEBUG
  
        log_colors_config = {
        'DEBUG': 'white',  # cyan white
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
        }
        self.setLevel(log_level)

        # 创建一个流处理器handler并设置其日志级别为DEBUG
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config
        )


        # 创建一个格式器formatter并将其添加到处理器handler
       # formatter = logging.Formatter('[%(asctime)s %(name)s %(filename)s [line:%(lineno)d]] %(levelname)s %(message)s')
        console_handler.setFormatter(console_formatter)
        

        path=Path(self.LogPath)
        if not path.exists():
            os.mkdir(self.LogPath)

        # 创建一个文件处理器handler并设置其日志级别为DEBUG
        file_handler = logging.FileHandler(filename=f'./logs/{log_name}.log')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)


        # 为日志器logger添加上面创建的处理器handler
        self.addHandler(console_handler)
        self.addHandler(file_handler) 
