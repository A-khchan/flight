from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time 
from selenium.webdriver.common.action_chains import ActionChains

service = Service()
chrome_options = Options()
#The below option make opened Chrome detached from Python program, 
#Chrome will keep open even if Python program end (suppose not explictly close it
#in program)
#Or, if you want to auto-close Chrome upon Python program end, comment this out.
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(4) # seconds

# No. of open Chrome tab
chromeCount = 0

def searchFlight(fromAirportCode, toAirportCode, fromMonth, fromDay, toMonth, toDay):
    global chromeCount

    if chromeCount > 0:        
        driver.execute_script("window.open('https://us.trip.com');")
        driver.switch_to.window(driver.window_handles[chromeCount])
    else:
        # Open the first Chrome tab
        driver.get("https://us.trip.com")
    
    chromeCount += 1

    # Get the 'flight' button
    flightButton = driver.find_elements("xpath", "//*[@id='main-search-box']/div[2]/div/div[1]/ul/li[2]/span")

    if flightButton:
        flightButton[0].click()

        clearAirport = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[1]/div[2]/div[1]/div/div/div/div/span/i")
        if clearAirport:
            clearAirport[0].click()
                                                                  
        fromAirport = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[1]/ul/li[1]/div[2]/div[1]/div/div/div/div/input")
        if not fromAirport:
            fromAirport = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[1]/div[2]/div[1]/div/div/div/div/input")
        
        if fromAirport:
            fromAirport[0].send_keys(fromAirportCode)
            time.sleep(2)
            fromAirport[0].send_keys(Keys.RETURN)

            #Clear the input if exist
            clearToAirport = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[1]/div[2]/div[3]/div/div/div/div/span/i")
            if clearToAirport:
                clearToAirport[0].click()

            toAirport = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[1]/ul/li[1]/div[2]/div[3]/div/div/div/div/input")
            if not toAirport:
                toAirport = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[1]/div[2]/div[3]/div/div/div/div/input")

            if toAirport:
                toAirport[0].send_keys(toAirportCode)
                time.sleep(2)
                toAirport[0].send_keys(Keys.RETURN)

                #Close the ads
                cheapFlight = driver.find_elements("xpath", "//*[@id='modals']/div/div[1]")
                if cheapFlight:
                    cheapFlight[0].click()


                fromDate = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[1]/ul/li[2]/div[1]")
                if not fromDate:
                    fromDate = driver.find_elements("xpath","//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[2]/div[1]/div/div/input")

                if fromDate:
                    continueToSearch = False
                    if chromeCount==1:
                        fromDate[0].click()
                        time.sleep(1)
                        if selectDate(driver, fromMonth, fromDay) and selectDate(driver, toMonth, toDay):
                            continueToSearch = True
                    else:
                        continueToSearch = True

                    if continueToSearch:
                        search = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[2]/span")
                        
                        # Second tab's xpath is different from the first, find_elements again with diff. path.
                        # It is similar for other elements.
                        if not search:
                            search = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[2]/span")
                        
                        if search:
                            search[0].click()
                            time.sleep(10)
                            nonStop = driver.find_elements("xpath", "//*[@id='main']/div[2]/div[7]/div[1]/div[1]/dl/div/dd[2]/dl/dd/dl/dd[1]/div/label/span[1]")
                            
                            if nonStop:
                                print("nonStop[0].get_attribute('class'): ", nonStop[0].get_attribute("class"))

                            if nonStop and nonStop[0].is_enabled():
                                a = ActionChains(driver)                                
                                #try:
                                a.move_to_element(nonStop[0]).click().perform()
                                #except:
                                #    pass

                            print("Try to close allow notification")
                            if chromeCount == 1:
                                allowN = driver.find_elements("xpath", "//*[@id='main']/div[1]/i")
                                if allowN and allowN[0].is_enabled() and allowN[0].is_displayed:
                                    allowN[0].click()
        else:
            print("fromAirport not found")

    else:
        print("flightButton not found")


def selectDate(driver, month, day):
    #assume the calendar already shown
    print("month pass in is ", month)

    keepFinding = True
    while keepFinding:
        monthHeading = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/div[1]/div[1]")
        
        if not monthHeading:
            monthHeading = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/div[1]/div[1]")
        
        useLeftCalendar = True
        if monthHeading and monthHeading[0].text[0:3] == month and clickDate(driver, day, useLeftCalendar):
            return True
        else:
            #Try to click the next month button
            nextMonth = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/span[2]")
            if not nextMonth:
                nextMonth = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/span[2]")
            
            if nextMonth and nextMonth[0].get_attribute("class") != "c-calendar-icon-next is-disable":
                nextMonth[0].click()
                print("Clicked next month")
                time.sleep(0.5)
            else:
                monthHeading2 = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/div[2]/div[1]")
                if not monthHeading2:                
                    monthHeading2 = driver.find_elements("xpath", "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/div[2]/div[1]")
                
                if monthHeading2 and monthHeading2[0].text[0:3] == month:
                    useLeftCalendar = False
                    if clickDate(driver, day, useLeftCalendar):
                        return True
                    else:
                        print("Not able to find month-day")
                        return False


def clickDate(driver, day, useLeftCalendar):
    weeks = range(5)
    cells = range(7)
    for week in weeks:
        for cell in cells:
            if useLeftCalendar:
                path = "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/div[1]/div[2]/ul[" + str(week+1) + "]/li[" + str(cell+1) + "]"
            else:
                path = "//*[@id='searchBoxCon']/div[2]/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/div[2]/div[2]/ul[" + str(week+1) + "]/li[" + str(cell+1) + "]"
            #print(path)

            dayCell = driver.find_elements("xpath", path)

            if not dayCell:
                if useLeftCalendar:
                    path = "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/div[1]/div[2]/ul[" + str(week+1) + "]/li[" + str(cell+1) + "]"
                else:
                    path = "//*[@id='searchBoxCon']/div/div/form/div/div[2]/div[1]/ul/li[2]/div[3]/div/div[1]/div[2]/div[2]/ul[" + str(week+1) + "]/li[" + str(cell+1) + "]"
                dayCell = driver.find_elements("xpath", path)

            if dayCell:
                print("dayCell[0] is ", dayCell[0].text)
                if dayCell[0].text == str(day) and dayCell[0].get_attribute("class") != "is-disable":
                    a = ActionChains(driver)
                    a.move_to_element(dayCell[0]).click().perform()
                    return True
    print("clickDate: Cannot find the day")
    return False


# Airport near LA area: "LAX", "ONT", "LGB", "SNA", "BUR" 
# Airport in Washington DC: "IAD", "DCA", "BWI"

# fromAirportList = [ "ONT", "LGB", "SNA", "BUR" ]
# toAirportList = [ "DCA", "BWI" ]
# Result: 0 non-stop

# fromAirportList = [ "ONT", "LGB", "SNA", "BUR" ]
# toAirportList = [ "IAD" ]
# Result: 0 non-stop


fromAirportList = [ "LAX" ]
toAirportList = [ "IAD", "DCA", "BWI" ]


for fromAirport in fromAirportList:
    for toAirport in toAirportList:
        searchFlight(fromAirport, toAirport, "Oct", 6, "Oct", 9)



#driver.quit()