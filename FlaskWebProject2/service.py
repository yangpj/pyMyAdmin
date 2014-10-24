# coding=utf-8

import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import multiprocessing

def run_server():
    from os import environ
    from FlaskWebProject2 import app
    app.run("0.0.0.0", 8088)

server = multiprocessing.Process(target=run_server)

class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "ZhiChenHaiXin"
    _svc_display_name_ = u"置辰海信数据库管理工具"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        server.terminate()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        server.start()
        server.join()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)