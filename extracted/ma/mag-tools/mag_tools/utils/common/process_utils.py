import os
import psutil


class ProcessUtils(object):
    @staticmethod
    def find_app(app):
        running = None

        app_name = os.path.basename(app)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.name().lower() == app_name.lower():
                    running = proc
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return running

    @staticmethod
    def terminate_app(app):
        app_name = os.path.basename(app)

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.name().lower() == app_name.lower():  # 统一大小写比较
                    try:
                        proc.terminate()
                        proc.wait()  # 等待进程终止
                    except psutil.NoSuchProcess:
                        print(f"Process {app_name} does not exist.")
                    except psutil.AccessDenied:
                        print(f"Access denied when trying to terminate {app_name}.")
                    except Exception as e:
                        print(f"Error occurred: {e}")
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass