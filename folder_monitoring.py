import time
import os
from datetime import datetime
import shutil

# Install Watchdog Package
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ModuleNotFoundError as e:
    print (e)
    os.system("pip install watchdog")

# ------------------------------------------------
class Handler(FileSystemEventHandler):
    def on_created(self, event): # 파일 생성시
        print (f'event type : {event.event_type}\n'

               f'event src_path : {event.src_path}')
        if event.is_directory:
            print ("디렉토리 생성")

        else: # not event.is_directory
            """
            Fname : 파일 이름
            Extension : 파일 확장자 
            """
            Fname, Extension = os.path.splitext(os.path.basename(event.src_path))
            '''
             1. py 파일
             2. txt 파일
             3. exe 파일
            '''
            if Extension == '.py':
                print (".py python 파일 입니다.")
            elif Extension == '.txt':
                print (".txt 텍스트 파일 입니다.")
                os.remove(Fname + Extension)   # _파일 삭제 event 발생
            elif Extension == '.exe':
                print (".exe 실행 파일 입니다.")

    def on_deleted(self, event):
        print ("삭제 이벤트 발생")

    def on_moved(self, event):  #파일, 디렉터리가 move 되거나 rename 되면 실행
        print (f'event type : {event.event_type}\n')

    def on_modified(self, event): #파일, 디렉터리가 수정되면 실행
        print("수정 이벤트 발생")

        destination_folder = r"C:/Users/wow1d/PycharmProjects/pythonProject/data4/"
        print(destination_folder)
        # fetch all files
        for file_name in os.listdir(event.src_path):
            print(file_name)
            print("find: ", file_name[file_name.find('.')+1:])

            print(f'event src_path : {event.src_path}')
            folder_name, Extension = os.path.splitext(os.path.basename(event.src_path))
            print(folder_name)
            print(Extension)
            # construct full file path
            source = (event.src_path)+'/' + file_name
            print(source)
            new_path = destination_folder + folder_name
            if not os.path.exists(new_path) :
                os.mkdir(new_path)

            destination = destination_folder + folder_name + '/' + file_name
            print(destination)
            # copy only files
            if os.path.isfile(source):
                if file_name[file_name.find('.')+1:] == 'py':
                    shutil.copy(source, destination)
                    print('copied', file_name)
                else :
                    print('No copy!')

class Watcher:

    # 생성자
    def __init__(self, path):
        print ("감시 시작 ...")
        self.event_handler = None      # Handler
        self.observer = Observer()     # Observer 객체 생성
        self.target_directory = path   # 감시대상 경로
        self.currentDirectorySetting() # instance method 호출 func(1)

    # func (1) 현재 작업 디렉토리
    def currentDirectorySetting(self):
        print ("====================================")
        print ("현재 작업 디렉토리:  ", end=" ")
        os.chdir(self.target_directory)
        print ("{cwd}".format(cwd = os.getcwd()))
        print ("====================================")

    # func (2)
    def run(self):
        self.event_handler = Handler() # 이벤트 핸들러 객체 생성
        self.observer.schedule(
            self.event_handler,
            self.target_directory,
            recursive=False
        )

        self.observer.start() # 감시 시작
        try:
            while True: # 무한 루프
                time.sleep(1) # 1초 마다 대상 디렉토리 감시
        except KeyboardInterrupt as e: # 사용자에 의해 "ctrl + z" 발생시
            print ("감시 중지...")
            self.observer.stop() # 감시 중단

if datetime.today().month < 4:
    myWatcher = Watcher("C:/Users/wow1d/PycharmProjects/pythonProject/data1")
elif datetime.today().month < 7 and datetime.today().month >= 4:
    myWatcher = Watcher("C:/Users/wow1d/PycharmProjects/pythonProject/data2")
elif datetime.today().month < 10 and datetime.today().month >= 7:
    myWatcher = Watcher("C:/Users/wow1d/PycharmProjects/pythonProject/data3")
else:
    myWatcher = Watcher("C:/Users/wow1d/PycharmProjects/pythonProject/data4")

myWatcher.run()