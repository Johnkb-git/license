import requests
import bs4
import json
from subprocess import call
import time

appointment_count = 5

def Round():
    url = "https://www.dmv.virginia.gov/onlineservices/driverTests.json"
    page = requests.get(url)
    content = page.text
    location_list = json.loads(content)
    ids = []

    # Please modify the locations you accept here
    allowed_location = ['Manassas Satellite Location- 7931 Mason King Court', 'Woodbridge - 2731 Caton Hill Road',
                       'Sterling - 100 Free Court']
    allowed_location.append("")
    for location in location_list["locations"]:
        for allowed in allowed_location:
            if location["location"] == allowed:
                ids.append(location["locationID"])
    for id in ids:
        Checkvailability(id)
    time.sleep(600)


def Checkvailability(id):
    url = "https://vadmvappointments.as.me/schedule.php?action=showCalendar&fulldate=1&owner=19444409&template=monthly"

    headers = {
        'authority': 'vadmvappointments.as.me',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://vadmvappointments.as.me',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://vadmvappointments.as.me/schedule.php?calendarID=4344351',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
    }

    months = ["2020-12-15","2020-11-15"]
    for month in months:
        payload = "type=15191541&calendar=" + id + "&month="+ month +"&skip=true&options%5BnumDays%5D=3&ignoreAppointment=&appointmentType=&calendarID=" + id
        response = requests.request("POST", url, headers=headers, data=payload)
        soup=bs4.BeautifulSoup(response.text,"lxml")
        result = soup.find_all(name='td',attrs={"class":"scheduleday activeday"})
        # This notification is for Mac only
        if len(result) != 0:
            cmd = 'display notification \"' + \
                  "There are available appointment!" + "Id:" + id + "    Month:" + month + '\" with title \"Attention!\"'
            call(["osascript", "-e", cmd])
        print(response.text.encode('utf8'))

# Unfinished function for filling the register appointment form automatically
# def SelectTime(id,date):
#     url = "https://vadmvappointments.as.me/schedule.php?action=availableTimes&showSelect=0&fulldate=1&owner=19444409"
#
#     # payload = "type=15191541&calendar=" + id + "&date=" + date + "&ignoreAppointment="
#     payload = "type=14002959&calendar=4344176&date=2020-09-22&ignoreAppointment="
#     headers = {
#         'authority': 'vadmvappointments.as.me',
#         'pragma': 'no-cache',
#         'cache-control': 'no-cache',
#         'accept': '*/*',
#         'x-requested-with': 'XMLHttpRequest',
#         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
#         'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'origin': 'https://vadmvappointments.as.me',
#         'sec-fetch-site': 'same-origin',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-dest': 'empty',
#         'referer': 'https://vadmvappointments.as.me/schedule.php?calendarID=4344176',
#         'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6',
#         'cookie': 'PHPSESSID=qq6p878d5l58casdmvmpisod2u; AWSALB=T63K7wwkR6O2k/WEUUiW8dFzCNRNS6hegnYLZixl17cGNuzeGjZhLI7Te5AY4tumqRRD7IIaVWNCgOenuETNjUlLOo9DERy069WwziGQa3/i7MYOgxU8LlSqOdlR; AWSALBCORS=T63K7wwkR6O2k/WEUUiW8dFzCNRNS6hegnYLZixl17cGNuzeGjZhLI7Te5AY4tumqRRD7IIaVWNCgOenuETNjUlLOo9DERy069WwziGQa3/i7MYOgxU8LlSqOdlR; AWSALB=qRJiGTVDt+hsQdaOQgrjgL3CODPe/yXzNpy3TbGTrbkHalwMUUMgRuaUGgNTT0h/R8dl7LsEgICoj04W7pJFb7ByD74WtohjPXvHp/YjSsjqraxL0d9xoDIFkVyh; AWSALBCORS=qRJiGTVDt+hsQdaOQgrjgL3CODPe/yXzNpy3TbGTrbkHalwMUUMgRuaUGgNTT0h/R8dl7LsEgICoj04W7pJFb7ByD74WtohjPXvHp/YjSsjqraxL0d9xoDIFkVyh'
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#     soup=bs4.BeautifulSoup(response.text,"lxml")
#     result = soup.find_all(name='label')
#
#     driver = webdriver.Chrome()
#     driver.get("https://vadmvappointments.as.me/schedule.php?calendarID="+id)
#     select = Select(driver.find_element_by_name('chooseMonthSched'))
#     select.select_by_value(id[:-2+"01"])
#
#     driver.find_element_by_class_name('scheduleday activeday').click()



while True:
    try:
        Round()
    except BaseException:
        print("Error")
