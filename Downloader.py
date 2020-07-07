import os
import unittest
from queue import Queue
import Repository
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import shutil

class Downloader:
    def __init__(self):
        self.workshop_downloader_url = "http://steamworkshop.download/download/view/"
        self.download_dir = "Downloads"
        if not os.path.isdir(self.download_dir):
            os.mkdir(self.download_dir)

    def get_id(self, workshop_url: str) -> int:
        part1 = workshop_url.split("id=")[1]
        id = part1.split("&")[0]
        return int(id)

    def download_all_mods(self):
        links_dict: dict = {}
        download_queue: dict = {}
        repo = Repository.Repository()
        workshop_links: dict = repo.read_repo()
        for k in workshop_links:
            link = self.workshop_downloader_url + str(self.get_id(workshop_links[k]))
            download_queue[k] = link
            print(f"Added {k} workshop downloader link to queue {link}")
        # Selenium part
        driver = webdriver.Firefox()
        direct_download: dict = {}
        for mod in download_queue:
            link = download_queue[mod]
            driver.get(link)

            try:
                elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'steamdownload'))
                )
                elem.click()
                elem_result = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '/html/body/div[1]/div[2]/div/table/tbody/tr/td/b/div[2]/pre/a'))
                )
                direct_download_link = elem_result.get_attribute("href")
                print(direct_download_link)
                direct_download[mod] = direct_download_link
            finally:
                pass
        driver.quit()

        return direct_download

    def wget_all(self):
        direct_links = self.download_all_mods()
        cmd = 'wget {0} -O Downloads/{1}.zip'
        for mod in direct_links:
            subprocess.run(cmd.format(direct_links[mod], mod.replace(" ", "")), shell=True)
        self.extract_all('Downloads/')

    def extract_all(self, path):
        files = os.listdir(path)
        to_unzip = []
        for i in files:
            if os.path.isfile(os.path.join(path, i)) and i.endswith('.zip'):
                to_unzip.append(i)

        for file in to_unzip:
            cmd = 'unzip {0} -d {1}'
            tmppath = os.path.join(path, 'tmp')
            if os.path.isdir(os.path.join(path, 'tmp')):
                shutil.rmtree(os.path.join(path, 'tmp'))
            if not os.path.isdir(os.path.join(path, 'tmp')):
                os.mkdir(os.path.join(path, 'tmp'))
            subprocess.run(cmd.format(os.path.join(path, file), tmppath), shell=True)
            extracted = os.listdir(tmppath)
            os.rename(os.path.join(tmppath, extracted[0]), os.path.join(path, file.replace('.zip', '')))
            shutil.rmtree(os.path.join(path, 'tmp'))
        return 0

class Test(unittest.TestCase):
    def test_get_id(self):
        url = r"https://steamcommunity.com/sharedfiles/filedetails/?id=1423699208&searchtext=Wall+Light"
        downloader = Downloader()
        result = downloader.get_id(url)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1423699208)

    def test_download_all_mods(self):
        downloader = Downloader()
        t = downloader.wget_all()
        self.assertGreater(len(t), -1)

    def test_extract_all(self):
        downloader = Downloader()
        t = downloader.extract_all('Downloads/')
        self.assertIs(t, 0)

if __name__ == "__main__":
    unittest.main()
