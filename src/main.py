import sys
import curses
import time

def main(stdscr):
  field = Field((0, 5), (0, 5))
  user = User(0, 0)
  suika_position = (3, 3)
  d = Display(stdscr)

  d.render(user, '')
  while user.getCoordinate() != suika_position:
    try:
      dir = d.input()
      if dir == curses.KEY_DOWN:
        if user.getYCoordinate() == field.getYUpper():
          raise MoveError("下には進めません。")
        user.moveUp()

      elif dir == curses.KEY_RIGHT:
        if user.getXCoordinate() == field.getXUpper():
          raise MoveError("右には進めません。")
        user.moveRight()

      elif dir == curses.KEY_UP:
        if user.getYCoordinate() == field.getYLower():
          raise MoveError("上には進めません。")
        user.moveDown()

      elif dir == curses.KEY_LEFT:
        if user.getXCoordinate() == field.getXLower():
          raise MoveError("左には進めません。")
        user.moveLeft()
      else:
        raise MoveError("入力が正しくありません。もう一度入力してください。")

      d.render(user, '')

    except MoveError as e:
      d.render(user, e.msg)
      continue
  else:
    d.render(user, '')
    d.finish()
    time.sleep(3)

class MoveError(Exception):
  def __init__(self, msg):
    self.msg = msg

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
    self.coordinate = (self.getXCoordinate(), self.getYCoordinate() + 1)

  def moveRight(self):
    self.coordinate = (self.getXCoordinate() + 1, self.getYCoordinate())

  def moveDown(self):
    self.coordinate = (self.getXCoordinate(), self.getYCoordinate() - 1)

  def moveLeft(self):
    self.coordinate = (self.getXCoordinate() - 1, self.getYCoordinate())

class Display():
  def __init__(self, stdscr):
    self.stdscr = stdscr
    self.stdscr.keypad(True)
  #   curses.noecho()

  def render(self, user, errMsg):
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
          else:
            row += "|   "

        row += "|"
        self.stdscr.addstr(2 * y + 1, 0, row)
      self.stdscr.addstr(2 * (5 + 1), 0, border)

      self.stdscr.addstr(2 * (5 + 2), 0, errMsg)
      self.stdscr.addstr(2 * (5 + 2) + 1, 0, 'どちらに進みますか？ n:上　e:右 s:下 w:左')

      self.stdscr.refresh()
    except:
      # Exception by Ctrl + C
      pass

  def input(self):
    return self.stdscr.getch()
  
  def finish(self):
    # self.stdscr.clear()
    self.stdscr.move(2 * (5 + 2) + 1, 0)
    self.stdscr.deleteln()
    self.stdscr.addstr(2 * (5 + 2) + 1, 0, 'スイカが割れました！！')
    self.stdscr.refresh()

if __name__ == "__main__":
  # main()
  # display()
  curses.wrapper(main)
  # try:
  #   count = 0
  #   while count != 3:

  #     stdscr = curses.initscr()
  #     # curses.noecho()
  #     # dir = input("input: ")
  #     dir = stdscr.getkey()
  #     if dir == "n":
  #       count += 1
  #     if dir == "m":
  #       count -= 1

  #     stdscr.clear()
  #     for x in range(0, 5):
  #       stdscr.addstr(2 * x, 0, '  ------------------------')
  #       if count == x:
  #         stdscr.addstr(2 * x + 1, 0, '%s | ● |   |   |   |   |   |' % x)
  #       else:
  #         stdscr.addstr(2 * x + 1, 0, '%s |   |   |   |   |   |   |' % x)

  #     stdscr.addstr(2 * (5 + 1), 0, '  ------------------------')
  #     stdscr.refresh()
  #     # time.sleep(10)
  # except Exception as e:
  #   print("aaaaa", e)
  #   # Exception by Ctrl + C
  #   pass
  # finally:
  #   curses.echo()
  #   curses.endwin()

  # 進む数の制限
  # エンターキーで棒を振る
  # 棒を振る数の制限
  # レベル選択