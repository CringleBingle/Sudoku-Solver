#getting a random sudoku puzzle from sudokuweb.org

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

PATH = 'D:\chromedriver.exe'	#specify chromedriver path
driver_service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=driver_service)
driver.get('https://sudokuweb.org')

board, line = [], []
count = 0

for x in range(0,81):

	if not x:
		elem = driver.find_element(By.XPATH,"//td[@id='right']")
		if elem.text != ' ':
			line.append(int(elem.text))
			count += 1

		else:
			line.append(0)
			count += 1


	else:
		elem = driver.find_element(By.XPATH, f"//td[@id='right{x}']")
		if elem.text != ' ':
			line.append(int(elem.text))
			count += 1

		else:
			line.append(0)
			count += 1

	if count == 9:
		count = 0
		board.append(line)
		line = []

driver.quit()



