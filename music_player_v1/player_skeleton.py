#----------------------------------------------------------------------
# player_skeleton.py
#
# Created: 04/14/2010-04/15/2010
#
# Author: Mike Driscoll - mike@pythonlibrary.org
#----------------------------------------------------------------------

import os
import wx
import wx.media
from wx.lib.agw.shapedbutton import SBitmapButton, SBitmapToggleButton

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')

########################################################################
class MediaPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.layoutControls()
        self.volume = 50

    #----------------------------------------------------------------------
    def layoutControls(self):
        """
        Create and layout the widgets
        """
        
        try:
            self.media = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise
        
        self.playbackSlider = wx.Slider(self, size=wx.DefaultSize)
        volumeBtn = wx.Button(self, label="Volume")
        
        # Create sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        audioTBSizer = self.buildAudioToolBar()
        
        # layout widgets
        hSizer.Add(self.playbackSlider, 0, wx.ALL, 5)
        hSizer.Add(volumeBtn, 0, wx.ALL, 5)
        mainSizer.Add(hSizer)
        mainSizer.Add(audioTBSizer)
        self.SetSizer(mainSizer)
        
    #----------------------------------------------------------------------
    def buildAudioToolBar(self):
        """
        Based on the ShapedButton demo from the wxPython Demo
        """
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # The Rewind Button Is A Simple Bitmap Button (SBitmapButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "rewind.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "rewinddisabled.png"), wx.BITMAP_TYPE_PNG)
        self.rewind = SBitmapButton(self, -1, upbmp, (48, 48))
        self.rewind.SetUseFocusIndicator(False)
        self.rewind.SetBitmapDisabled(disbmp)

        self.rewind.Bind(wx.EVT_BUTTON, self.onRewind)
        hSizer.Add(self.rewind, 0, wx.LEFT, 3)
        
        # The Play Button Is A Toggle Bitmap Button (SBitmapToggleButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "play.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "playdisabled.png"), wx.BITMAP_TYPE_PNG)
        self.play = SBitmapToggleButton(self, -1, upbmp, (48, 48))
        self.play.SetUseFocusIndicator(False)
        self.play.SetBitmapDisabled(disbmp)

        self.play.Bind(wx.EVT_BUTTON, self.onPlay)
        hSizer.Add(self.play, 0, wx.LEFT, 3)

        # The Pause Button Is A Toggle Bitmap Button (SBitmapToggleButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "pause.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "pausedisabled.png"), wx.BITMAP_TYPE_PNG)
        self.pause = SBitmapToggleButton(self, -1, upbmp, (48, 48))
        self.pause.SetUseFocusIndicator(False)
        self.pause.SetBitmapDisabled(disbmp)
        self.pause.Enable(False)

        self.pause.Bind(wx.EVT_BUTTON, self.onPause)
        hSizer.Add(self.pause, 0, wx.LEFT, 3)

        # The Stop Button Is A Simple Bitmap Button (SBitmapButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "stop.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "stopdisabled.png"), wx.BITMAP_TYPE_PNG)
        self.stop = SBitmapButton(self, -1, upbmp, (48, 48))
        self.stop.SetUseFocusIndicator(False)
        self.stop.SetBitmapDisabled(disbmp)
        self.stop.Enable(False)

        self.stop.Bind(wx.EVT_BUTTON, self.onStop)
        hSizer.Add(self.stop, 0, wx.LEFT, 3)

        # The FFWD Button Is A Simple Bitmap Button (SBitmapButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "ffwd.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "ffwddisabled.png"), wx.BITMAP_TYPE_PNG)
        self.ffwd = SBitmapButton(self, -1, upbmp, (48, 48))
        self.ffwd.SetUseFocusIndicator(False)
        self.ffwd.SetBitmapDisabled(disbmp)

        self.ffwd.Bind(wx.EVT_BUTTON, self.onFFWD)
        hSizer.Add(self.ffwd, 0, wx.LEFT, 3)
        return hSizer
    
    #----------------------------------------------------------------------
    def onFFWD(self, event):
        """
        """
        pass
    
    #----------------------------------------------------------------------
    def onPause(self, event):
        """
        """
        pass
    
    #----------------------------------------------------------------------
    def onPlay(self, event):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def onRewind(self, event):
        """
        """
        pass
    
    #----------------------------------------------------------------------
    def onStop(self, event):
        """
        """
        pass

class MediaFrame(wx.Frame):
 
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Python Music Player")
        panel = MediaPanel(self)
        
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MediaFrame()
    frame.Show()
    app.MainLoop()