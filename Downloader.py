import os
import unittest


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


class Test(unittest.TestCase):
    def test_get_id(self):
        url = r"https://steamcommunity.com/sharedfiles/filedetails/?id=1423699208&searchtext=Wall+Light"
        downloader = Downloader()
        result = downloader.get_id(url)
        self.assertIsInstance(result, int)
        self.assertEqual(result, 1423699208)


if __name__ == "__main__":
    unittest.main()
