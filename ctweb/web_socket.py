import logging
import base64
import os
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
import glob
import cv2
from PIL import Image
import numpy as np
#from django.apps import ctapp
#from .ctapp import models
from django.core.files import File
#from ctweb.ctapp.models import student_testsubmission,student,Test


define("port", default=8001, help="run on the given port", type=int)

class MainHandler(tornado.websocket.WebSocketHandler):
    count = 0
    def check_origin(self, origin):
        return True

    def open(self):
        print("connected")
        self.frames = []
        logging.info("A client connected.")

    def on_close(self):
        logging.info("A client disconnected")

        import time
        time.sleep(5)
        print('now loading images')
        #loading frames to constuct video
        img_array = []
        for filename in self.frames:
            img = cv2.imread(filename)
            img_array.append(img)
            #print(filename)
            #height, width, layers = img.shape
            #size = (width, height)
            #nparr = np.fromstring(base64.b64decode(frame), np.uint8)
            #img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        print('now making video')
        name = 'Images/'+self.stud_id+'.avi'
        out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'DIVX'), 15, (600,450))
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
        print('now deleting frames')
        #deleting frames
        import os
        for filename in self.frames:
            os.remove(filename)

        # This logic is necessary to import django files from non-django python files like this
        import sys
        sys.path.append('..')
        import django
        django.setup()
        from ctapp.models import student_testsubmission, student, Test #this might look like error but it's not
        #x = student.objects.get(enrollment_number='0103IT181055')
        #print(x)


    # ADD logic to create a test submission object which has 3 values stud id , test id ,a video file and proctor description
        stud_object = student.objects.get(enrollment_number=self.stud_id)
        test_obj = Test.objects.get(id=int(self.test_id))
        submission = student_testsubmission()
        submission.stud_id = stud_object
        submission.test_id = test_obj
        f = open(name,'rb')
        file = File(f)
        submission.video = file
        submission.save()
        f.close()

        #delete video locally stored
        os.remove(name)

        print("Successful!!!!")




    def on_message(self, message):
        #from main.detect import get_face_detect_data
        #image_data = get_face_detect_data(message)
        #print("received",message)
        #print(message)
        if message.startswith('stud:'):
            print(message)
            self.stud_id = message.split(':')[1]
            print(self.stud_id)
        elif message.startswith('testid:'):
            #print(message)
            self.test_id = int(message.split(':')[1])
            #print(self.test_id)
        image_data = message[22:]#cropping header
        name = 'Images/check'+ str(MainHandler.count) +'.png'
        image = open(name, 'wb')
        image.write(base64.b64decode((image_data)))
        image.close()
        self.frames.append(name)
        MainHandler.count += 1
        if not image_data:
            image_data = message
        self.write_message(image_data)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/websocket", MainHandler)]
        settings = dict(debug=True)
        tornado.web.Application.__init__(self, handlers, **settings)


def socket():
    print("yes")
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ctweb.settings")
    tornado.options.parse_command_line()
    #now we start app
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__" and __package__ is None:
    socket()

