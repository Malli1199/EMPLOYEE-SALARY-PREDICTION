import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    # Crucial flags for running inside Jenkins/automated pipelines smoothly:
    options.add_argument("--headless=new") # Runs without opening a UI window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Selenium 4 automatically downloads and matches the correct ChromeDriver for your system
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_dashboard_title(driver):
    driver.get("http://localhost:8500")
    time.sleep(4) # Allow Streamlit app layout components to fully render
    assert "Salary Predictor" in driver.title or "Employee" in driver.title