from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Julie has heard about a cool new online to-do app.
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')
        
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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1. Buy concert tickets', [row.text for row in rows])

        # There is still a text box inviting her to add another item
        # She enters "Buy a sofa"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a sofa')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and now shows both items on her list
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1. Buy concert tickets', [row.text for row in rows])
        self.assertIn('2. Buy a sofa', [row.text for row in rows])

        # Julie wonders whether the site will remember her list.
        # Than she sees that the site has generated a unique URL just for her
        # -- there is some explanatory text to that effect
        self.fail('Finish the test!')

        # She visits that URL - her list is still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')


