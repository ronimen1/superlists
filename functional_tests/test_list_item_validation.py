from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
    
    def test_cannot_add_empty_list_items(self):
        # Julie goes to the home page and accidentally tries to submit an empty list item
        # She hits enter on the empty input box
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # The home page refreshes and there is an error message saying that list items cannot be blank
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")

        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Write recommendation\n')
        self.check_for_row_in_list_table('1. Write recommendation')

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys('\n')

        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1. Write recommendation')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Transfer money\n')
        self.check_for_row_in_list_table('1. Write recommendation')
        self.check_for_row_in_list_table('2. Transfer money')

    def test_cannot_add_duplicate_items(self):
        # Julie goes to the home page and starts a new list
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Moving\n')
        self.check_for_row_in_list_table('1. Moving')

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys('Moving\n')

        # She sees a helpful error message
        self.check_for_row_in_list_table('1. Moving')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")

    def test_error_messages_are_cleared_on_input(self):
        # Julie starts a new list in a way that causes a validation error:
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())

        # She starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertFalse(error.is_displayed())

