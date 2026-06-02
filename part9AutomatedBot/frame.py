import numpy as np
import win32gui, win32ui, win32con
from ctypes import windll
from threading import Thread, Lock
import mss

class Frame:

    stopped = True
    lock = None
    frame = None
    pixel = None

    # properties
    w = 0
    h = 0
    hwnd = None
    window_check = False

    offset_x = 0
    offset_y = 0

    def __init__(self, window_name = None):
        # create thread lock object
        self.lock = Lock()

        # Define which window to use
        # This is another way of trying to fix the black screen problem
        # by getting the desktop window if no window is found
        if window_name is None:
            self.window_check = True
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception("Window not found: {}".format(window_name))
        
        # Define width and height of Image
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = 1920
        self.h = 1080

    # Since windows GUI and UI are not working in aimlabs 3D environment,
    # I am attempting to use mss to capture frame instead
    def get_frame_mss(self):
        with mss.mss() as sct:
            # Define your exact scanning bounding box region
            monitor = {"top": 0, "left": 0, "width": self.w, "height": self.h}
            # sct.grab directly captures hardware-accelerated buffers
            raw_frame = np.array(sct.grab(monitor))
            return raw_frame
        

    # Using windows GUI and UI, take a window screenshot and convert it to OpenCV format 
    # and optimize it to be faster than pyautogui screenshot
    # Return image as a screenshot of selected window
    # https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows 
    def get_frame(self):

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)

        # I get a black screen when using original stack Overflow code, 
        # so I asked chatgpt how to change this to work with more modern games:
        # This line is the main line to change because the game is rendered with DirectX/OpenGL/Vulkan using GPU swap chains, 
        # overlays, or exclusive fullscreen rendering. Aim Lab is likely bypassing the normal GDI desktop compositor, 
        # so GDI capture APIs only see an empty/black surface.
        if self.window_check: 
            cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0,0), win32con.SRCCOPY) 

        # For this to still work the game must be in Fullscreen Windowed or Windowed
        # The Print Window function fits the window grabbed, so there is not need for 
        # cropping pixels from pulled image like in tutorial
        else:
            result = windll.user32.PrintWindow(self.hwnd, cDC.GetSafeHdc(), 3)

        # convert the raw data into a format opencv can read
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        # This was originally np.fromstring, however with newer versions of numpy, np.fromstring  binary mode is deprecated
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # drop the alpha channel, or cv.matchTemplate() will throw an error like:
        #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
        #   && _img.dims() <= 2 in function 'cv::matchTemplate'
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        return img


    # Finds all open windows on system with associated hex values. 
    # This is mainly used for finding string values of windows.
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    @staticmethod
    def list_windows():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    # start the thread to get and update the image
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()
        
    # stop the thread
    def stop(self):
        self.stopped = True
    
    # Function to be run when thread is started
    def run(self):
        while not self.stopped:
            # get image
            frame = self.get_frame()
            # update the image while thread is locked
            self.lock.acquire()
            self.frame = frame
            self.lock.release()