import pyautogui


def double_space():
    pyautogui.press('space', 2, 1.7)


def press(key):
    pyautogui.press(key)
