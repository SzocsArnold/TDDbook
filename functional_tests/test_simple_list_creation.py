from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



class NewVisitorTest(FunctionalTest):
         
    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('item_text')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url,'/lists/.+')
        self.browser.quit()
        self.browser = webdriver.Firefox(executable_path="C:\\Users\\Arnold\\geckodriver\\geckodriver.exe")
        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        inputbox = self.browser.find_element_by_id('item_text')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')

        self.assertNotEqual(francis_list_url,edith_list_url)
        
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Buy milk',page_text)
        
        

       