import sys
import curses
import time
import random

def main(stdscr):
  field = Field((0, 5), (0, 5))
  user = User(0, 0)
  suika_position = (random.randrange(5), random.randrange(5))
  d = Display(stdscr)
  isHit = False
  upperLimitOfWavingStickCount = 3

  d.render(user, '', str(upperLimitOfWavingStickCount), None)
  while not isHit and upperLimitOfWavingStickCount > 0:
    try:
      input = d.input()
      if input == curses.KEY_DOWN:
        if user.getYCoordinate() == field.getYUpper():
          raise DownwardMovementRestrictionError()
        user.moveDown()

      elif input == curses.KEY_RIGHT:
        if user.getXCoordinate() == field.getXUpper():
          raise RightwardMovementRestrictionError()
        user.moveRight()

      elif input == curses.KEY_UP:
        if user.getYCoordinate() == field.getYLower():
          raise UpwardMovementRestrictionError()
        user.moveUp()

      elif input == curses.KEY_LEFT:
        if user.getXCoordinate() == field.getXLower():
          raise LeftwardMovementRestrictionError()
        user.moveLeft()

      elif input == 10: # エンターキーを押下した場合
        upperLimitOfWavingStickCount -= 1
        if user.getCoordinate() != suika_position:
          d.miss()
          continue
        isHit =True

      else:
        raise InvalidOperationError()

      d.render(user, '', str(upperLimitOfWavingStickCount), None)

    except Error as e:
      d.render(user, e.msg, str(upperLimitOfWavingStickCount), None)
      continue
  else:
    d.render(user, '', str(upperLimitOfWavingStickCount), suika_position)
    if not isHit and upperLimitOfWavingStickCount == 0:
      d.gameOverByUpperLimitOfWavingStick()
      return
    d.success()

class Error(Exception):
  def __init__(self, msg):
    self.msg = msg

class UpwardMovementRestrictionError(Error):
  def __init__(self):
    super(UpwardMovementRestrictionError, self).__init__('上には進めません。')

class DownwardMovementRestrictionError(Error):
  def __init__(self):
    super(DownwardMovementRestrictionError, self).__init__('下には進めません。')

class LeftwardMovementRestrictionError(Error):
  def __init__(self):
    super(LeftwardMovementRestrictionError, self).__init__('左には進めません。')

class RightwardMovementRestrictionError(Error):
  def __init__(self):
    super(RightwardMovementRestrictionError, self).__init__('右には進めません。')

class InvalidOperationError(Error):
  def __init__(self):
    super(InvalidOperationError, self).__init__('入力が正しくありません。もう一度入力してください。')

class Field():
  def __init__(self,x_range, y_range):
    self.x_range = x_range # x_range (x_coordinate_min, x_coordinate_max)
    self.y_range = y_range # y_range (y_coordinate_min, y_coordinate_max)

  def getXLower(self):
    return self.x_range[0]

  def getXUpper(self):
    return self.x_range[1]

  def getYLower(self):
    return self.y_range[0]

  def getYUpper(self):
    return self.y_range[1]

class User():
  def __init__(self, x_coordinate, y_coordinate):
    self.coordinate = (x_coordinate, y_coordinate)

  def getXCoordinate(self):
    return self.coordinate[0]
  
  def getYCoordinate(self):
    return self.coordinate[1]

  def getCoordinate(self):
    return self.coordinate

  def moveUp(self):
    self.coordinate = (self.getXCoordinate(), self.getYCoordinate() - 1)

  def moveRight(self):
    self.coordinate = (self.getXCoordinate() + 1, self.getYCoordinate())

  def moveDown(self):
    self.coordinate = (self.getXCoordinate(), self.getYCoordinate() + 1)

  def moveLeft(self):
    self.coordinate = (self.getXCoordinate() - 1, self.getYCoordinate())

class Display():
  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.stdscr.keypad(True)
  #   curses.noecho()

  def render(self, user, errMsg, upperLimitOfWavingStickCount, suikaPosition):
    try:
      self.stdscr.clear()
      border = '-'
      for _ in range(0, 6): border += '----'

      for y in range(0, 6):
        self.stdscr.addstr(2 * y, 0, border)
        row = ''
        for x in range(0, 6):
          if user.getCoordinate() == (x, y):
            row += "| ● "
          elif suikaPosition is not None and suikaPosition == (x, y):
            row += "| 🍉 "
          else:
            row += "|   "

        row += "|"
        self.stdscr.addstr(2 * y + 1, 0, row)
      self.stdscr.addstr(2 * (5 + 1), 0, border)

      if errMsg == '':
        self.stdscr.addstr(2 * (5 + 2), 0, '棒を振ることができる残り回数：' + str(upperLimitOfWavingStickCount))
      else:
        self.stdscr.addstr(2 * (5 + 2), 0, errMsg)
        
      self.stdscr.addstr(2 * (5 + 2) + 1, 0, 'どちらに進みますか？ n:上　e:右 s:下 w:左')

      self.stdscr.refresh()
    except:
      # Exception by Ctrl + C
      pass

  def input(self):
    return self.stdscr.getch()
  
  def success(self):
    self.stdscr.move(2 * (5 + 2) + 1, 0)
    self.stdscr.deleteln()
    self.stdscr.addstr(2 * (5 + 2) + 1, 0, 'スイカが割れました！！')
    self.stdscr.refresh()
    time.sleep(3)

  def miss(self):
    self.stdscr.move(2 * (5 + 2), 0)
    self.stdscr.deleteln()
    self.stdscr.insertln()
    self.stdscr.addstr(2 * (5 + 2), 0, 'ハズレ！！')
    self.stdscr.refresh()

  def gameOverByUpperLimitOfWavingStick(self):
    self.stdscr.addstr(2 * (5 + 2), 0, '棒を振ることができる回数が上限に達しました。ゲーム終了！！')
    self.stdscr.refresh()
    time.sleep(3)

if __name__ == "__main__":
  curses.wrapper(main)

  # レベル選択
  # リファクタ
  # ヒント機能（掛け声）もっと左とか