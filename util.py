import wx
import os
import re
import time
import base64
import calendar
import urllib.request
import urllib.error
import urllib.parse
import urllib.parse
import threading
try:
    import feedparser
except ModuleNotFoundError:
    sys.exit("\n\tpip install feeparser\n")

from html.entities import name2codepoint
from settings import settings


def set_icon(window):
    """[summary]

    Arguments:
        window {[type]} -- [description]
    """

    bundle = wx.IconBundle()
    bundle.AddIcon(wx.Icon('icons/16.png', wx.BITMAP_TYPE_PNG))
    bundle.AddIcon(wx.Icon('icons/24.png', wx.BITMAP_TYPE_PNG))
    bundle.AddIcon(wx.Icon('icons/32.png', wx.BITMAP_TYPE_PNG))
    bundle.AddIcon(wx.Icon('icons/48.png', wx.BITMAP_TYPE_PNG))
    bundle.AddIcon(wx.Icon('icons/256.png', wx.BITMAP_TYPE_PNG))
    window.SetIcons(bundle)


def start_thread(func, *args):
    """[summary]

    Arguments:
        func {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    print('util::start_thread - In')  # Fixme: delete this
    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(True)
    thread.start()
    print('util::start_thread - Out')  # Fixme: delete this
    return thread


def scale_bitmap(bitmap, width, height, color):
    """[summary]

    Arguments:
        bitmap {[type]} -- [description]
        width {[type]} -- [description]
        height {[type]} -- [description]
        color {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    bw, bh = bitmap.GetWidth(), bitmap.GetHeight()
    if bw == width and bh == height:
        return bitmap
    if width < 0:
        width = bw
    if height < 0:
        height = bh
    # buffer = wx.EmptyBitmap(bw, bh)  # FIXME: deprecated
    buffer = wx.Bitmap(bw, bh)
    dc = wx.MemoryDC(buffer)
    dc.SetBackground(wx.Brush(color))
    dc.Clear()
    dc.DrawBitmap(bitmap, 0, 0, True)
    # image = wx.ImageFromBitmap(buffer)  # FIXME: deprecated
    image = wx.Bitmap.ConvertToImage(buffer)
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    # result = wx.BitmapFromImage(image)  # FIXME: deprecated
    result = wx.Bitmap(image)
    return result


def menu_item(menu, label, func, icon=None, kind=wx.ITEM_NORMAL):
    """[summary]

    Arguments:
        menu {[type]} -- [description]
        label {[type]} -- [description]
        func {[type]} -- [description]

    Keyword Arguments:
        icon {[type]} -- [description] (default: {None})
        kind {[type]} -- [description] (default: {wx.ITEM_NORMAL})

    Returns:
        [type] -- [description]
    """

    item = wx.MenuItem(menu, -1, label, kind=kind)
    if func:
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    if icon:
        item.SetBitmap(wx.Bitmap(icon))
    # menu.AppendItem(item)  # FIXME: deprecated
    menu.Append(item)
    return item


def select_choice(choice, data):
    """[summary]

    Arguments:
        choice {[type]} -- [description]
        data {[type]} -- [description]
    """

    for index in range(choice.GetCount()):
        if choice.GetClientData(index) == data:
            choice.Select(index)
            return
    choice.Select(wx.NOT_FOUND)


def get_top_window(window):
    """[summary]

    Arguments:
        window {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    result = None
    while window:
        result = window
        window = window.GetParent()
    return result


def get(obj, key, default):
    """[summary]

    Arguments:
        obj {[type]} -- [description]
        key {[type]} -- [description]
        default {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    value = obj.get(key, None)
    return value or default


def abspath(path):
    """[summary]

    Arguments:
        path {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    path = os.path.abspath(path)
    path = 'file:///%s' % path.replace('\\', '/')
    return path


def parse(url, username=None, password=None, etag=None, modified=None):
    """[summary]

    Arguments:
        url {[type]} -- [description]

    Keyword Arguments:
        username {[type]} -- [description] (default: {None})
        password {[type]} -- [description] (default: {None})
        etag {[type]} -- [description] (default: {None})
        modified {[type]} -- [description] (default: {None})

    Returns:
        [type] -- [description]
    """

    agent = settings.USER_AGENT
    handlers = [get_proxy()]
    if username and password:
        url = insert_credentials(url, username, password)
    return feedparser.parse(url, etag=etag, modified=modified, agent=agent, handlers=handlers)


def is_valid_feed(data):
    """[summary]

    Arguments:
        data {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    entries = get(data, 'entries', [])
    title = get(data.feed, 'title', '')
    link = get(data.feed, 'link', '')
    return entries or title or link


def insert_credentials(url, username, password):
    """[summary]

    Arguments:
        url {[type]} -- [description]
        username {[type]} -- [description]
        password {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    parts = urllib.parse.urlsplit(url)
    netloc = parts.netloc
    if '@' in netloc:
        netloc = netloc[netloc.index('@')+1:]
    netloc = '%s:%s@%s' % (username, password, netloc)
    parts = list(parts)
    parts[1] = netloc
    return urllib.parse.urlunsplit(tuple(parts))


def encode_password(password):
    """[summary]

    Arguments:
        password {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    return base64.b64encode(password) if password else None


def decode_password(password):
    """[summary]

    Arguments:
        password {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    try:
        return base64.b64decode(password) if password else None
    except Exception:
        return None


def get_proxy():
    """[summary]

    Returns:
        [type] -- [description]
    """

    if settings.USE_PROXY:
        url = decode_password(settings.PROXY_URL)
        if url:
            # User-configured Proxy
            map = {
                'http': url,
                'https': url,
            }
            proxy = urllib.request.ProxyHandler(map)
        else:
            # Windows-configured Proxy
            proxy = urllib.request.ProxyHandler()
    else:
        # No Proxy
        proxy = urllib.request.ProxyHandler({})
    return proxy


def find_themes():
    """[summary]

    Returns:
        [type] -- [description]
    """

    # return ['default']  # TODO: more themes! FIXME: unreachable code
    result = []
    names = os.listdir('themes')
    for name in names:
        if name.startswith('.'):
            continue
        path = os.path.join('themes', name)
        if os.path.isdir(path):
            result.append(name)
    return result


def guess_polling_interval(entries):
    """[summary]

    Arguments:
        entries {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    if len(entries) < 2:
        return settings.DEFAULT_POLLING_INTERVAL
    timestamps = []
    for entry in entries:
        timestamp = calendar.timegm(get(entry, 'date_parsed', time.gmtime()))
        timestamps.append(timestamp)
    timestamps.sort()
    durations = [b - a for a, b in zip(timestamps, timestamps[1:])]
    mean = sum(durations) / len(durations)
    choices = [
        60,
        60*5,
        60*10,
        60*15,
        60*30,
        60*60,
        60*60*2,
        60*60*4,
        60*60*8,
        60*60*12,
        60*60*24,
    ]
    desired = mean / 2
    if desired == 0:
        interval = settings.DEFAULT_POLLING_INTERVAL
    elif desired < choices[0]:
        interval = choices[0]
    else:
        interval = max(choice for choice in choices if choice <= desired)
    return interval


def time_since(t):
    """[summary]

    Arguments:
        t {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    t = int(t)
    now = int(time.time())
    seconds = max(now - t, 0)
    if seconds == 1:
        return '1 second'
    if seconds < 60:
        return '%d seconds' % seconds
    minutes = seconds / 60
    if minutes == 1:
        return '1 minute'
    if minutes < 60:
        return '%d minutes' % minutes
    hours = minutes / 60
    if hours == 1:
        return '1 hour'
    if hours < 24:
        return '%d hours' % hours
    days = hours / 24
    if days == 1:
        return '1 day'
    return '%d days' % days


def split_time(seconds):
    """[summary]

    Arguments:
        seconds {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    if seconds < 60:
        return seconds, 0
    minutes = seconds / 60
    if minutes < 60:
        return minutes, 1
    hours = minutes / 60
    days = hours / 24
    if days and hours % 24 == 0:
        return days, 3
    return hours, 2


def split_time_str(seconds):
    """[summary]

    Arguments:
        seconds {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    interval, units = split_time(seconds)
    strings = ['second', 'minute', 'hour', 'day']
    string = strings[units]
    if interval != 1:
        string += 's'
    return '%d %s' % (interval, string)


def pretty_name(name):
    """[summary]

    Arguments:
        name {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    name = ' '.join(s.title() for s in name.split('_'))
    last = '0'
    result = ''
    for c in name:
        if c.isdigit() and not last.isdigit():
            result += ' '
        result += c
        last = c
    return result


def replace_entities1(text):
    """[summary]

    Arguments:
        text {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    entity = re.compile(r'&#(\d+);')

    def func(match):
        try:
            return chr(int(match.group(1)))
        except Exception:
            return match.group(0)
    return entity.sub(func, text)


def replace_entities2(text):
    """[summary]

    Arguments:
        text {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    entity = re.compile(r'&([a-zA-Z]+);')

    def func(match):
        try:
            return chr(name2codepoint[match.group(1)])
        except Exception:
            return match.group(0)
    return entity.sub(func, text)


def remove_markup(text):
    """[summary]

    Arguments:
        text {[type]} -- [description]

    Returns:
        [type] -- [description]
    """

    html = re.compile(r'<[^>]+>')
    return html.sub(' ', text)


def format(text, max_length=400):
    """[summary]

    Arguments:
        text {[type]} -- [description]

    Keyword Arguments:
        max_length {int} -- [description] (default: {400})

    Returns:
        [type] -- [description]
    """

    previous = ''
    while text != previous:
        previous = text
        text = replace_entities1(text)
        text = replace_entities2(text)
    text = remove_markup(text)
    text = ' '.join(text.split())
    if len(text) > max_length:
        text = text[:max_length].strip()
        text = text.split()[:-1]
        text.append('[...]')
        text = ' '.join(text)
    return text

# EOFF
