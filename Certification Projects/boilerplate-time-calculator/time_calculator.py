def add_time(start, duration, weekday=None):

  ##split into time and AM/PM and convert hours to military time.
  startSpl = start.split()
  hourMin = startSpl[0].split(':')
  if startSpl[1] == "PM" and hourMin[0] != '12':
    hourMil = int(hourMin[0]) + 12
  else:
    hourMil = int(hourMin[0])
  minMil = int(hourMin[1])

  ##Add hours and minutes
  Add = duration.split(':')
  hourAdd = int(Add[0])
  minAdd = int(Add[1])
  newHourMil = hourMil + hourAdd
  newMinMil = minMil + minAdd

  ##Reformat minutes to not exceed 59.
  while newMinMil > 59:
    newMinMil += -60
    newHourMil += 1

  ##Reformat hours to not exceed 23. It doubles as a way to count day change.
  dayChanges = 0
  while newHourMil > 23:
    newHourMil += -24
    dayChanges += 1

  ##Reformat hours to be in 12hr format. It doubles as a way to determine AM or PM.
  if newHourMil > 12:
    newHourMil += -12
    AMorPM = "PM"
  elif newHourMil < 12:
    if newHourMil == 0:
      newHourMil = 12
    AMorPM = "AM"
  elif newHourMil == 12:
    AMorPM = "PM"

  ##Figure out the day of the week if it is provided.
  if weekday is not None:
    weekdays = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday'
    }  #This will only be used for printing the weekday at the end, as we need a dictionary to check in a case insensitive way.
    numToWeek = {k: v.lower() for k, v in weekdays.items()}
    weekToNum = {v: k for k, v in numToWeek.items()}

    wkdNumI = weekToNum[weekday.lower()]
    wkdNumF = wkdNumI + dayChanges
    while wkdNumF > 7:
      wkdNumF += -7
    weekdayF = weekdays[wkdNumF]

  ##Format time into easy strings
  if len(str(newMinMil)) < 2:
    minF = '0' + str(newMinMil)
  else:
    minF = str(newMinMil)
  hourF = str(newHourMil)

  ##Final output.
  if weekday is not None:
    if dayChanges > 1:
      new_time = (
          f'{hourF}:{minF} {AMorPM}, {weekdayF} ({dayChanges} days later)')
    elif dayChanges == 1:
      new_time = (f'{hourF}:{minF} {AMorPM}, {weekdayF} (next day)')
    elif dayChanges == 0:
      new_time = (f'{hourF}:{minF} {AMorPM}, {weekdayF}')
  elif weekday is None:
    if dayChanges > 1:
      new_time = (f'{hourF}:{minF} {AMorPM} ({dayChanges} days later)')
    elif dayChanges == 1:
      new_time = (f'{hourF}:{minF} {AMorPM} (next day)')
    elif dayChanges == 0:
      new_time = (f'{hourF}:{minF} {AMorPM}')

  return new_time
