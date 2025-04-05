import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class JobScraper:
    def __init__(self, keyword, level):
        self.keyword = keyword.replace(" ", "-")
        self.level = level.replace(" ", "-")

    def get_naukri_jobs(self):
        options = Options()
        options.add_argument("--headless")  # Run in background
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("user-agent=Mozilla/5.0")  # Mimic real user

        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option(name="detach", value=True)
        driver = webdriver.Chrome(options=chrome_option)
        url = f"https://www.naukri.com/{self.keyword}-{self.level}-jobs"
        driver.get(url)

        # Wait for jobs to load
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cust-job-tuple")))
        except:
            print("No jobs found or website changed structure.")
            driver.quit()
            return []

        # Scroll to load more jobs
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Allow loading

        job_list = []
        jobs = driver.find_elements(By.CSS_SELECTOR, "div.cust-job-tuple")[:10]  # Get top 10 jobs

        for job in jobs:
            try:
                title = job.find_element(By.CSS_SELECTOR, "h2 a").text
                company = job.find_element(By.CSS_SELECTOR, "a.comp-name").text
                rating = job.find_element(By.CSS_SELECTOR, "a.rating span.main-2").text if job.find_elements(
                    By.CSS_SELECTOR, "a.rating span.main-2") else "N/A"
                experience = job.find_element(By.CSS_SELECTOR, "span.expwdth").text
                salary = job.find_element(By.CSS_SELECTOR, "span.sal span").text if job.find_elements(By.CSS_SELECTOR,
                                                                                                      "span.sal span") else "Not Disclosed"
                location = job.find_element(By.CSS_SELECTOR, "span.locWdth").text
                description = job.find_element(By.CSS_SELECTOR, "span.job-desc").text
                skills = [skill.text for skill in job.find_elements(By.CSS_SELECTOR, "ul.tags-gt li.tag-li")]
                date_posted = job.find_element(By.CSS_SELECTOR, "span.job-post-day").text
                apply_link = job.find_element(By.CSS_SELECTOR, "h2 a.title").get_attribute("href")

                job_list.append({
                    "title": title,
                    "company": company,
                    "rating": rating,
                    "experience": experience,
                    "salary": salary,
                    "location": location,
                    "description": description,
                    "skills": skills,
                    "date_posted": date_posted,
                    "apply_link": apply_link
                })
            except Exception as e:
                print(f"Error: {e}")

        driver.quit()
        return job_list

    def get_all_jobs(self):
        results = {
           "naukri_job": self.get_naukri_jobs()
        }
        return results
