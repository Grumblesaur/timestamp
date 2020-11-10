import re
import time

seconds_per_hour = 3600
seconds_per_minute = 60

def normalize_timezone(tz):
  offset = 0
  if isinstance(tz, (str,)):
    if re.match("[+-]\d+:[012345][0123456789]", tz):
      sign = 1 if tz[0] == '+' else '-'
      hours, minutes = tz[1:].split(':')
      offset = sign
      offset += float(hours) * seconds_per_hour
      offset += float(minutes) * seconds_per_minute
    else:
      try:
        offset = float(tz) * 3600
      except ValueError:
        pass
  elif isinstance(tz, (int, float)):
    offset = tz * 3600
  return offset

def parse_kwargs(d):
  class TimeSettings(object):
    def __init__(self):
      self.timezone = 0
      self.format = "%y-%m-%d %H:%M:%S"
      self.as_epoch = False
      self.nanos = False
    
  settings = TimeSettings()
  for kw in d:
    if kw == 'epoch':
      settings.as_epoch = d[kw]
    if kw == 'timezone':
      settings.timezone = normalize_timezone(d[kw])
    if kw == 'format':
      settings.format = d[kw]
    if kw == 'nanoseconds':
      settings.nanos = d[kw]
    
  return settings

def stamp(kwargs):
  settings = parse_kwargs(kwargs)
  
  out = None
  if settings.as_epoch:
    if settings.nanos:
      out = time.time_ns()
    else:
      out = time.time()
  else:
    now = time.time()
    if not settings.timezone:
      struct = time.gmtime(now)
      out = time.strftime(settings.format, struct)
    else:
      struct = time.gmtime(now + settings.timezone)
      out = time.strftime(settings.format, struct)
  return out


