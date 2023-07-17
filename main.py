import time
from utils import calculate_sentence_similarity
import pandas as pd
import chromedriver_autoinstaller

#Using (special)undected chromedriver to bypass cloudflare security
import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By


#set options to make chrome start in full screen
opt = uc.ChromeOptions() 
opt.add_argument("--start-maximized")
#opt.add_experimental_option("detach", True)


#Auto install the latest chromedriver
chromedriver_autoinstaller.install()

SEARCH_URL = "https://www.indeed.com/jobs?q=searchQuery&l=Remote&from=searchOnHP&vjk=e9e77cebf0e41601"


#Create array/list for confidence level
RESULT_CONFIDENCE = []

#Create array/list for job title for indeed
RESULT_TITLE = []

#Create array/list for position
RESULT_POSITION = []

#read csv file 
df = pd.read_csv("IndeedBot.csv")

#get positions from first column of csv file and convert to a list/array
positions = df.iloc[:,0].tolist()

#Initialize chrome driver

driver = uc.Chrome(use_subprocess=True, options=opt) 


#Loop through each position in positions list and search for it on indeed.com
for position in positions:
    driver.get(SEARCH_URL.replace("searchQuery", position))
    while True:
        job_titles = driver.find_elements(by=By.CLASS_NAME, value='jobTitle')
        for job_title in job_titles:
            RESULT_POSITION.append(position)
            RESULT_TITLE.append(job_title.text.strip())
            confidence_level = calculate_sentence_similarity(position.lower(), job_title.text.lower())
            RESULT_CONFIDENCE.append(confidence_level)
        try:
            next_btn = driver.find_element(by=By.CSS_SELECTOR, value='a[data-testid="pagination-page-next"]')
            next_btn.click()
        except Exception as e:
            break
        

#Create final result dataframe
df_result = pd.DataFrame({"Position": RESULT_POSITION, "Title": RESULT_TITLE, "Confidence Level": RESULT_CONFIDENCE})

#print the first 20 rows
print(df_result.head(20))

#save final result as a csv file called result.csv
df_result.to_csv("result.csv", index=False)

