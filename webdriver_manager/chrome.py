import os
import re
import requests
from typing import Optional

from webdriver_manager.core.download_manager import DownloadManager
from webdriver_manager.core.manager import DriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.drivers.chrome import ChromeDriver


class ChromeDriverManager(DriverManager):
    def __init__(
            self,
            version: Optional[str] = None,
            os_type: Optional[str] = None,
            path: Optional[str] = None,
            name: str = "chromedriver",
            url: str = "https://chromedriver.storage.googleapis.com",
            latest_release_url: str = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE",
            chrome_type: str = ChromeType.GOOGLE,
            cache_valid_range: int = 1,
            download_manager: Optional[DownloadManager] = None,
    ):
        if re.fullmatch("[0-9]*\.[0-9]*\.[0-9]*", version) or re.fullmatch(
            "[0-9]*", version
        ):
            version_response = requests.get(
                f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}"
            )
            if version_response.status_code == 404:
                raise ValueError(
                    f"There is no such driver version number by url {version_response.url}"
                )
            if version_response.status_code == 200:
                if re.fullmatch(
                    "[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*", version_response.text
                ):
                    version = version_response.text

        super().__init__(
            path,
            cache_valid_range=cache_valid_range,
            download_manager=download_manager)

        self.driver = ChromeDriver(
            name=name,
            version=version,
            os_type=os_type,
            url=url,
            latest_release_url=latest_release_url,
            chrome_type=chrome_type,
            http_client=self.http_client,
        )

    def install(self) -> str:
        driver_path = self._get_driver_path(self.driver)
        os.chmod(driver_path, 0o755)
        return driver_path
