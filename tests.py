import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SITE_URL = 'http://atomicboard.devman.org/'
CREATE_USER_URL = 'http://atomicboard.devman.org/create_test_user/'


class AtomicboardTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get(CREATE_USER_URL)
        self.driver.find_element_by_xpath("//button[@type='submit']").click()
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//p[text()="Сделано. Пользователь создан и авторизован"]')))
        self.driver.get(SITE_URL)
        self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH,
                     '//span[@class="col-md-4 tickets-column '
                     'js-tickets-column ng-scope"]')))

    def test_load_page(self):
        if "AtomicBoard" not in self.driver.title:
            raise Exception("Unable to load AtomicBoard page!")
        assert "AtomicBoard" in self.driver.title
        assert self.driver.find_element_by_xpath(
            '//span[contains(@class, "ticket_id")]')

    def test_edit_task(self):
        task = self.driver.find_element_by_xpath(
            '//div[contains(@class, "panel-heading-no-padding")]')
        task.find_element_by_xpath(
            '//span[@editable-text="ticket.title"]').click()
        task_input = task.find_element_by_xpath(
            '//input[contains(@class, "editable-input")]')
        task_input.clear()
        task_input.send_keys('some text')
        task.find_element_by_xpath(
            '//button[@type="submit"]').click()
        assert 'some text' in task.text

    def test_mark_task_closed(self):
        task = self.driver.find_element_by_xpath(
            '//div[contains(@class, "panel-heading-no-padding")]')
        task.find_element_by_xpath(
            '//span[@data-target="#changeStatusModal" and '
            'contains(text(), "open")]').click()
        sleep(1)
        self.driver.find_element_by_xpath(
            '//button[contains(@class, "change-status-form__button") and '
            'contains(text(), "closed")]').click()
        assert task.find_element_by_xpath(
            '//span[@data-target="#changeStatusModal" and '
            'contains(text(), "closed")]')

    def test_create_new_task(self):
        div_add_task = self.driver.find_element_by_xpath(
            '//div[contains(@class, "add-ticket-block")]')
        div_add_task.find_element_by_xpath(
            '//span[contains(@class, "add-ticket-block_button")]').click()
        input_field = div_add_task.find_element_by_xpath(
            '//input[contains(@class, "editable-input")]')
        input_field.send_keys('test create new task')
        div_add_task.find_element_by_xpath(
                    '//button[@type="submit"]').click()
        sleep(1)
        assert 'test create new task' in self.driver.page_source


    def tearDown(self):
        self.driver.quit()
        pass


if __name__ == '__main__':
    unittest.main()
