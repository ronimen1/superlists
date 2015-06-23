from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Julie has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get(self.live_server_url)
        
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy concert tickets" into a text box
        inputbox.send_keys('Buy concert tickets')

        # When she hits enter the page updates and now the page lists
        # "1. Buy concert tickets" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        julie_list_url = self.browser.current_url
        self.assertRegex(julie_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1. Buy concert tickets')

        # There is still a text box inviting her to add another item
        # She enters "Buy a sofa"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a sofa')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and now shows both items on her list
        self.check_for_row_in_list_table('1. Buy concert tickets')
        self.check_for_row_in_list_table('2. Buy a sofa')

        # Now a new user, Steve, comes along to the site

        ## We use a new browser session to make sure that no information of
        ## Julie's is coming through from cookies etc
        self.browser.quit
        self.browser = webdriver.Firefox()

        # Steve visits the home page. There is no sign of Julie's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy concert tickets', page_text)
        self.assertNotIn('Buy a sofa', page_text)

        # Steve starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Sing along')
        inputbox.send_keys(Keys.ENTER)

        # Steve gets his own unique URL
        steve_list_url = self.browser.current_url
        self.assertRegex(steve_list_url, '/lists/.+')
        self.assertNotEqual(steve_list_url, julie_list_url)

        # Again, there is no trace of Julie's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy concert tickets', page_text)
        self.assertIn('Sing along', page_text)

    def test_layout_and_styling(self):
        # Julie goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 5
        )

        # She starts a new list and sees the input is nicely centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 5
        )


if __name__ == '__main__':
    unittest.main(warnings='ignore')


