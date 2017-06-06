import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SITE_URL = 'http://atomicboard.devman.org/'
CREATE_USER_URL = 'http://atomicboard.devman.org/create_test_user/'
JQUERY_URL = "http://code.jquery.com/jquery-1.11.2.min.js"


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
                (By.CSS_SELECTOR,
                 'span.tickets-column.js-tickets-column.ng-scope')))

    def test_load_page(self):
        if "AtomicBoard" not in self.driver.title:
            raise Exception("Unable to load AtomicBoard page!")
        self.assertIn("AtomicBoard", self.driver.title)
        self.assertTrue(self.driver.find_element_by_css_selector(
            'span.ticket_id'))

    def test_displaying_list_of_current_tasks(self):
        list_of_current_tasks = self.driver.find_elements_by_xpath(
            '//span[@data-target="#changeStatusModal" and '
            'contains(text(), "open")]')
        self.assertNotEqual(len(list_of_current_tasks), 0)

    def test_edit_task(self):
        task = self.driver.find_element_by_css_selector(
            'div.panel-heading-no-padding')
        task.find_element_by_xpath(
            '//span[@editable-text="ticket.title"]').click()
        task_input = task.find_element_by_css_selector(
            'input.editable-input')
        task_input.clear()
        task_input.send_keys('some text')
        task.find_element_by_xpath(
            '//button[@type="submit"]').click()
        self.assertIn('some text', task.text)

    def test_mark_task_closed(self):
        task = self.driver.find_element_by_css_selector(
            'div.panel-heading-no-padding')
        task.find_element_by_xpath(
            '//span[@data-target="#changeStatusModal" and '
            'contains(text(), "open")]').click()
        btn_close = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH,
                 '//div[contains(@style, "display: block")]'
                 '//button[contains(@class, "change-status-form__button") and '
                 'contains(text(), "closed")]')))
        btn_close.click()
        self.assertTrue(task.find_element_by_xpath(
            '//span[@data-target="#changeStatusModal" and '
            'contains(text(), "closed")]'))

    def test_create_new_task(self):
        div_add_task = self.driver.find_element_by_css_selector(
            'div.add-ticket-block')
        div_add_task.find_element_by_css_selector(
            'span.add-ticket-block_button').click()
        input_field = div_add_task.find_element_by_css_selector(
            'input.editable-input')
        input_field.send_keys('test create new task')
        div_add_task.find_element_by_xpath(
                    '//button[@type="submit"]').click()
        self.assertTrue(self.driver.find_element_by_xpath(
                '//span[contains(@class, "panel-heading_text") and '
                'contains(text(), "test create new task")]'))

    def test_drag_and_drop_task(self):
        tickets_columns = self.driver.find_elements_by_css_selector(
            'span.tickets-column')
        tickets_column_source = tickets_columns[0]
        tickets_column_target = tickets_columns[1]
        task = tickets_column_source.find_element_by_css_selector(
            'div.ticket__compact')
        task_id = task.find_element_by_css_selector(
            'span.ticket_id').text
        with open("jquery_load_helper.js") as jquery_load_helper_file:
            load_jquery_js = jquery_load_helper_file.read()
        with open("drag_and_drop_helper.js") as drag_and_drop_helper_file:
            drag_and_drop_js = drag_and_drop_helper_file.read()
        self.driver.execute_async_script(load_jquery_js, JQUERY_URL)
        self.driver.execute_script(
            drag_and_drop_js
            + "$('div.ticket__compact:eq(0)').simulateDragDrop("
              "{ dropTarget: 'span.tickets-column:eq(1)'});")
        self.assertNotIn(task_id, tickets_column_source.text)
        self.assertIn(task_id, tickets_column_target.text)

    def tearDown(self):
        self.driver.quit()
        pass


if __name__ == '__main__':
    unittest.main()
