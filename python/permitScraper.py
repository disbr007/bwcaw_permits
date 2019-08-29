#! python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

date = input('What date do you want to go to the BWCA? (mm/dd/yyyy) ')
                 
browser = webdriver.Firefox()
browser.get('https://www.recreation.gov/permits/Boundary-Waters-Canoe-Area-Wilderness-Reservations/r/permitCalendar.do?page=calendar&contractCode=NRSO&parkId=72600')

# Select permit type
permitElem = browser.find_element_by_id('permitTypeId')

for option in permitElem.find_elements_by_tag_name('option'):
    if option.text == 'Overnight Paddle':
        option.click()
        break

# Set date - static date for now - update to user choice later
calElem = browser.find_element_by_id('entryStartDate')
calElem.click()
calElem.send_keys(date) # TODO: change to user input of some kind
calElem.submit()

time.sleep(3)

# Page 1 of results:
availTable = browser.find_element_by_id('shoppingitems')

availDict = {}

for row in availTable.find_elements_by_class_name('br'):
    cells = row.find_elements_by_tag_name('td')
    availCell = cells[0].text
    avail = availCell.split('\n')[0]
    epCell = cells[1].text
    epFull = epCell.split('\n')[0]
    epNum = epFull.split()[0]
    epName = epFull[epFull.find(' ')+1:epFull.find('(')]
    epType = epFull[epFull.find('(')+1:epFull.find(')')]
    epNumName = epNum + ' - ' + epName
    availDict[epNumName] = avail

# Page 2 of results:
nextPage = browser.find_element_by_css_selector('#shoppingitems > thead:nth-child(6) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(2) > a:nth-child(2)')
nextPage.click()

#time.sleep(2)

availTable2 = browser.find_element_by_id('shoppingitems')
for row in availTable2.find_elements_by_class_name('br'):
    cells = row.find_elements_by_tag_name('td')
    availCell = cells[0].text
    avail = availCell.split('\n')[0]
    epCell = cells[1].text
    epFull = epCell.split('\n')[0]
    epNum = epFull.split()[0]
    epName = epFull[epFull.find(' ')+1:epFull.find('(')]
    epType = epFull[epFull.find('(')+1:epFull.find(')')]
    epNumName = epNum + ' - ' + epName
    availDict[epNumName] = avail

# Page 3 of results:
# Close survey results
try:
    popupX2 = browser.find_element_by_css_selector('#acsMainInvite > a:nth-child(2)')
    popupX2.click()
except:
    pass  
  
nextPage2 = browser.find_element_by_css_selector('#shoppingitems > thead:nth-child(6) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(2) > a:nth-child(2)')
nextPage2.click()

#time.sleep(2)

availTable3 = browser.find_element_by_id('shoppingitems')
for row in availTable3.find_elements_by_class_name('br'):
    cells = row.find_elements_by_tag_name('td')
    availCell = cells[0].text
    avail = availCell.split('\n')[0]
    epCell = cells[1].text
    epFull = epCell.split('\n')[0]
    epNum = epFull.split()[0]
    epName = epFull[epFull.find(' ')+1:epFull.find('(')]
    epType = epFull[epFull.find('(')+1:epFull.find(')')]
    epNumName = epNum + ' - ' + epName
    availDict[epNumName] = avail

print('\nThe following entry points are available on %s:' %(date))

for key in sorted(availDict):
    if availDict[key] == 'Available':
        print('%s: %s' % (key, availDict[key]))

print('\nThe following entry points are not available on %s:' %(date))
for key in sorted(availDict):
    if availDict[key] == 'Not Available':
        print('%s: %s' % (key, availDict[key]))
browser.quit()
