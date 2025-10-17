from bs4 import BeautifulSoup
import subprocess
import time
import pyautogui
from setting import Setting
# Enter the idm path here ...
idm_path = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
setting = Setting()
# read html
def readHtml(filename):
    with open(filename , "r" , encoding="utf-8") as f:
        html = f.read()
        #parse html
        soup = BeautifulSoup(html , "html.parser")
        return soup
    
def reset_idm_queue():
    # run IDM
    print("opening IDM...")
    subprocess.Popen(idm_path)
    time.sleep(0.5)

    # stop all download and 
    print("Stopping Downloads...")
    pyautogui.hotkey('alt' , 'd')
    pyautogui.press(['down' , 'enter'])
    time.sleep(0.5)

    # delete all download then minimize
    print("Deleting Downloads...")
    pyautogui.hotkey('ctrl' , 'a' , 'delete')
    time.sleep(0.5)
    print("Minimizing...")
    pyautogui.hotkey('alt' , 'space')
    pyautogui.press('N')
    time.sleep(0.5)

def extract_links(seasons):
    #Extracts Links
    with open("links.txt", "w", encoding="utf-8") as f:
        i = 1
        for season in seasons:
            season_num = season.find("h3").text.strip()
            quality = season.find("div", class_="head_left_side").text.strip()
            links = [a["href"] for a in season.select(".part_item a.partlink[href]") if a["href"] != "#"]
            if quality.find(setting.quality) != -1:
                f.write(f"{season_num} - {quality}\n")
                for link in links:
                    f.write(str(i) +  ". " + link +"\n")
                    print(f"{i}.Link Extracted ")
                    if setting.idm_download:
                        subprocess.run([idm_path , "/d" , link , "/a" , "/n"])
                    i += 1
                f.write("\n")


soup = readHtml("file.html")
qualities = []


#extracts all quality names
seasons = soup.find_all("div" , class_="item_row_series parent_item")
for quality_div in seasons:
    quality = quality_div.find("div" , class_="head_left_side").text.strip()
    qualities.append(quality)
print('\n'.join(qualities))
while True:
    user_quality = input("Enter the Quality you want : ")
    if user_quality in qualities:
        print("Quality Found!!!")
        setting.quality = user_quality
        break
    else:
        print("No Matching Quality! ")

#check if the user wants to add to idm queue
user_download = input("Do you want to add them to IDM? ")
if user_download.lower() in ["yes" , "true" , "y" , "1"]:
    setting.idm_download = True
    reset_idm_queue()
    
#check if the user wants to download now
user_start_download = input("Do you want to start download now? ")
if user_start_download.lower() in ["yes" , "true" , "y" , "1"]:
    setting.idm_start = True

extract_links(seasons)
if setting.idm_start :
    subprocess.run([idm_path , "/s"])
elif setting.idm_download :
    subprocess.run(idm_path)
print(setting)
setting.resetSetting()