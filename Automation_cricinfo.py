import pyautogui
import time
import sys
import webbrowser
# Open the Cricinfo website
webbrowser.open("https://www.espncricinfo.com/")    
# Wait for the website to load
time.sleep(5) 
pyautogui.click(1697, 143) 
time.sleep(2)    
pyautogui.typewrite("MS dhoni") 
time.sleep(2)    
pyautogui.press("enter") 
time.sleep(5) 
pyautogui.click(242, 616) 
time.sleep(5) 
pyautogui.scroll(-600)
time.sleep(8)
screenshot = pyautogui.screenshot() 
screenshot.save("ms_dhoni_profile.png") 

sys.exit()