# -*- coding: utf-8 -*-

"""[summary]

Returns:
    [type] -- [description]
"""


import wx
import wx.lib.wordwrap as wordwrap

import util


class Event(wx.PyEvent):
    """[summary]

    Arguments:
        wx {[type]} -- [description]
    """

    def __init__(self, event_object, type):
        """[summary]

        Arguments:
            event_object {[type]} -- [description]
            type {[type]} -- [description]
        """

        super(Event, self).__init__()
        self.SetEventType(type.typeId)
        self.SetEventObject(event_object)


EVT_HYPERLINK = wx.PyEventBinder(wx.NewEventType())


class Line(wx.PyPanel):
    """[summary]

    Arguments:
        wx {[type]} -- [description]
    """

    def __init__(self, parent, pen=wx.BLACK_PEN):
        """[summary]

        Arguments:
            parent {[type]} -- [description]

        Keyword Arguments:
            pen {[type]} -- [description] (default: {wx.BLACK_PEN})
        """

        super(Line, self).__init__(parent, -1, style=wx.BORDER_NONE)
        self.pen = pen
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        self.Refresh()

    def on_paint(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        dc.SetPen(self.pen)
        width, height = self.GetClientSize()
        y = height / 2
        dc.DrawLine(0, y, width, y)

    def DoGetBestSize(self):
        """[summary]

        Returns:
            [type] -- [description]
        """

        return -1, self.pen.GetWidth()


class Text(wx.PyPanel):
    """[summary]

    Arguments:
        wx {[type]} -- [description]
    """

    def __init__(self, parent, width, text):
        """[summary]

        Arguments:
            parent {[type]} -- [description]
            width {[type]} -- [description]
            text {[type]} -- [description]
        """

        super(Text, self).__init__(parent, -1, style=wx.BORDER_NONE)
        self.text = text
        self.width = width
        self.wrap = True
        self.rects = []
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)

    def on_size(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        self.Refresh()

    def on_paint(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        dc = wx.AutoBufferedPaintDC(self)
        self.setup_dc(dc)
        dc.Clear()
        self.draw_lines(dc)

    def setup_dc(self, dc):
        """[summary]

        Arguments:
            dc {[type]} -- [description]
        """

        parent = self.GetParent()
        dc.SetFont(self.GetFont())
        dc.SetTextBackground(parent.GetBackgroundColour())
        dc.SetTextForeground(parent.GetForegroundColour())
        dc.SetBackground(wx.Brush(parent.GetBackgroundColour()))

    def draw_lines(self, dc, emulate=False):
        """[summary]

        Arguments:
            dc {[type]} -- [description]

        Keyword Arguments:
            emulate {bool} -- [description] (default: {False})

        Returns:
            [type] -- [description]
        """

        if self.wrap:
            text = wordwrap.wordwrap(self.text.strip(), self.width, dc)
        else:
            text = self.text.strip()
        lines = text.split('\n')
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if line]
        x, y = 0, 0
        rects = []
        for line in lines:
            if not emulate:
                dc.DrawText(line, x, y)
            w, h = dc.GetTextExtent(line)
            rects.append(wx.Rect(x, y, w, h))
            y += h
        if not emulate:
            self.rects = rects
        return y

    def compute_height(self):
        """[summary]

        Returns:
            [type] -- [description]
        """

        dc = wx.ClientDC(self)
        self.setup_dc(dc)
        height = self.draw_lines(dc, True)
        return height

    def fit_no_wrap(self):
        """[summary]
        """

        dc = wx.ClientDC(self)
        self.setup_dc(dc)
        width, height = dc.GetTextExtent(self.text.strip())
        self.width = width
        self.wrap = False

    def DoGetBestSize(self):
        """[summary]

        Returns:
            [type] -- [description]
        """

        height = self.compute_height()
        return self.width, height


class Link(Text):
    """[summary]

    Arguments:
        Text {[type]} -- [description]
    """

    def __init__(self, parent, width, link, text):
        super(Link, self).__init__(parent, width, text)
        self.link = link
        self.trigger = False
        self.hover = False
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_RIGHT_UP, self.on_right_up)

    def hit_test(self, point):
        """[summary]

        Arguments:
            point {[type]} -- [description]
        """

        for rect in self.rects:
            if rect.Contains(point):
                self.on_hover()
                break
        else:
            self.on_unhover()

    def on_motion(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        self.hit_test(event.GetPosition())

    def on_leave(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        self.on_unhover()

    def on_hover(self):
        """[summary]
        """

        if self.hover:
            return
        self.hover = True
        font = self.GetFont()
        font.SetUnderlined(True)
        self.SetFont(font)
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.Refresh()

    def on_unhover(self):
        """[summary]
        """

        if not self.hover:
            return
        self.hover = False
        self.trigger = False
        font = self.GetFont()
        font.SetUnderlined(False)
        self.SetFont(font)
        self.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
        self.Refresh()

    def on_left_down(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        if self.hover:
            self.trigger = True

    def on_left_up(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        if self.hover and self.trigger:
            self.post_event()

        self.trigger = False

    def on_right_up(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        menu = wx.Menu()
        util.menu_item(menu, 'Open Link', self.on_open_link)
        util.menu_item(menu, 'Copy Link', self.on_copy_link)
        self.PopupMenu(menu, event.GetPosition())

    def on_open_link(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        self.post_event()

    def on_copy_link(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.link))
            wx.TheClipboard.Close()

    def post_event(self):
        """[summary]
        """

        event = Event(self, EVT_HYPERLINK)
        event.link = self.link
        wx.PostEvent(self, event)


class BitmapLink(wx.PyPanel):
    """[summary]

    Arguments:
        wx {[type]} -- [description]
    """

    def __init__(self, parent, link, bitmap, hover_bitmap=None):
        """[summary]

        Arguments:
            parent {[type]} -- [description]
            link {[type]} -- [description]
            bitmap {[type]} -- [description]

        Keyword Arguments:
            hover_bitmap {[type]} -- [description] (default: {None})
        """

        super(BitmapLink, self).__init__(parent, -1)
        self.link = link
        self.bitmap = bitmap
        self.hover_bitmap = hover_bitmap or bitmap
        self.hover = False
        self.trigger = False
        self.SetInitialSize(bitmap.GetSize())
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.on_leave)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)

    def on_paint(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        parent = self.GetParent()
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(parent.GetBackgroundColour()))
        dc.Clear()
        bitmap = self.hover_bitmap if self.hover else self.bitmap
        dc.DrawBitmap(bitmap, 0, 0, True)

    def on_enter(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        self.hover = True
        self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        self.Refresh()

    def on_leave(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        self.trigger = False
        self.hover = False
        self.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
        self.Refresh()

    def on_left_down(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        self.trigger = True

    def on_left_up(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        if self.trigger:
            event = Event(self, EVT_HYPERLINK)
            event.link = self.link
            wx.PostEvent(self, event)
        self.trigger = False

# EOF