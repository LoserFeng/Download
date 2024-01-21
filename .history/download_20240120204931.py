import os
import requests
from tqdm import tqdm
from logger.my_logger import MyLogger
import typing as tp
import json



src_url="https://plus.figshare.com/ndownloader/files/36682266"

root_path="E:/resource/Learning/Dataset"

save_path="THINGS_MEG/pre_preprocessed/THINGS-MEG_preproc.tar.gz"



class Downloader():
    save_path:str=None
    src_url:str=None

    chunk_size:int = 1024 * 1024*16  # 16M
    log_frequency=chunk_size

    def __init__(self,src_url, form_data:tp.Dict=None, save_path:str=None) -> None:
        self.root_path=root_path

        self.save_progress_freq=1


        self.logger=MyLogger(f"download_f")
        self.dl_progress=None


        assert os.path.exists(self.root_path)
        os.chdir(self.root_path)

        self.save_path=os.path.join(self.root_path,save_path)
        self.parent_dir=os.path.dirname(save_path)
        self.filename = os.path.basename(save_path)
        self.parent_dir_path=os.path.join(self.root_path,self.parent_dir)
        self.dl_progress_path=os.path.join(self.parent_dir_path,f"{self.filename}.progress")
    
        self.mkdir(self.parent_dir)
        self.logger=MyLogger(self.filename)
        self.logger.info("Downloader初始化")
        self.src_url=src_url
        self.form_data=form_data
    

    def load_dl_progress(self):
        dl_progress={"cur_size":0,"total_size":0,"progress":0}
        if os.path.exists(self.dl_progress_path):
            with open(self.progress_path, 'r') as f:
                dl_progress = json.load(f)

        return dl_progress

    def save_dl_progress(self,progress):
        with open(self.dl_progress_path, 'w') as f:
            json.dump(self.dl_progress,f)
        self.logger.info(f"保存下载进度{self.dl_progress_path}")
            
            

    def mkdir(self,path:str):
        if(os.path.exists(path)):
            return
        os.makedirs(path)


    def download_by_stream(self):
        headers = {}
        if os.path.exists(self.dl_progress_path):
            self.dl_progress=self.load_dl_progress()
            print(f'Resumable mode: start download from {self.dl_progress}')
        else:
            self.dl_progress={"cur_size":0,"total_size":0,"progress":0}
            print('Normal mode: start download from beginning')


        

        # tqdm可选total参数,不传递这个参数则不显示文件总大小
        desc = '下载 {}'.format(self.filename)
        self.logger.info(desc)
        cur_size=self.dl_progress["cur_size"]
        headers = {'Range': f'bytes={cur_size}-'}

        # 设置stream=True参数读取大文件
        response = requests.get(self.src_url, headers=headers,stream=True, data=self.form_data)

        if response.status_code!=200:
            self.logger.error(f'status_code:{response.status_code},无法下载文件{self.filename}，请检查url是否有效')
            self.logger.error(f'{response.text}')
            return False
        cur_size=self.dl_progress["cur_size"]
        self.dl_progress["total_size"] = int(response.headers.get('content-length', 0))
        self.logger.info(f"文件{self.filename}总共total_size{self.dl_progress['total_size']}bytes ")
        progress_bar =tqdm(
            desc="下载进度",
            total=self.dl_progress['total_size'],
            initial=self.dl_progress['cur_size'],
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        )

        with open(save_path, 'ab') as fp:
            # 每次最多读取chunk_size个字节
            
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                
                if chunk:
                    fp.write(chunk)
                    fp.flush()
                    progress_bar.update(len(chunk))
                    cur_size+=self.chunk_size
                    self.logger.info(f"进度：{cur_size/1024} MB")
                    self.dl_progress["cur_size"]=cur_size
                    self.dl_progress["progress"]=f"{float(cur_size/self.dl_progress['total_size'])*100}%"
                    self.save_dl_progress(self.dl_progress)

            self.logger.info(f"下载结束！,总共下载了{cur_size} GB")
                    

        progress_bar.close()
        




def main():



    downloader=Downloader(src_url=src_url, save_path=save_path)
    
    downloader.download_by_stream()


if __name__ == '__main__':
    main()