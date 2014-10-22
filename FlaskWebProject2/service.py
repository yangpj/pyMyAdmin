# coding=utf-8

import pythoncom
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

class AppServerSvc(win32serviceutil.ServiceFramework):
    _svc_name_ = "Flask Web Server"
    _svc_display_name_ = u"置辰海信数据库管理工具"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        run_server()

def run_server():
    from os import environ
    from FlaskWebProject2 import app
    #HOST = environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    app.run("0.0.0.0", 8088)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)