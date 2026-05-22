import numpy as np
import win32gui, win32ui
from ctypes import windll

class Frame:

    # properties
    w = 0
    h = 0
    hwnd = None

    def __init__(self, window_name):
        # Define which window to use
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception("Window not found: {}".format(window_name))
        
        # Define width and height of Image
        self.w = 1920
        self.h = 1080


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
        # cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, 0), win32con.SRCCOPY) 

        # For this to still work the game must be in Fullscreen Windowed or Windowed
        # The Print Window function fits the window grabbed, so there is not need for 
        # cropping pixels from pulled image like in tutorial
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
    def list_windows(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

