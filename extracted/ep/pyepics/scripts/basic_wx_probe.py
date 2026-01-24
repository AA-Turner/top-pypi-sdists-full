#!/usr/bin/python
#
# simple PV Probe application

import wx
from epics.wx import PVText

class ProbeFrame(wx.Frame):
    def __init__(self, parent=None, **kws):
        wx.Frame.__init__(self, parent, -1)
        self.SetTitle("Connect to Epics PVs:")

        sizer = wx.GridBagSizer(2, 2)

        self.pvname = wx.TextCtrl(self, value='', size=(200, -1),
                                  style=wx.TE_PROCESS_ENTER)
        self.pvname.Bind(wx.EVT_CHAR, self.onNameEvent)

        self.pvtext = PVText(self, None, size=(200, -1))

        nam_label = wx.StaticText(self, label='PV Name:', size=(150, -1))
        val_label = wx.StaticText(self, label='PV Value:', size=(150, -1))

        sizer.Add(nam_label,   (0, 0), (1, 1), wx.ALIGN_LEFT, 1)
        sizer.Add(val_label,   (1, 0), (1, 1), wx.ALIGN_LEFT, 1)
        sizer.Add(self.pvname, (0, 1), (1, 1), wx.ALIGN_LEFT, 1)
        sizer.Add(self.pvtext, (1, 1), (1, 1), wx.ALIGN_LEFT, 1)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def onNameEvent(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.pvtext.SetPV(self.pvname.GetValue().strip())

if __name__ == '__main__':
    app = wx.App()
    ProbeFrame().Show()
    app.MainLoop()
