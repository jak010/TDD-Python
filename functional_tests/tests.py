from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.url = "D:\\Source\\TDD-Python\\superlists\\functional_tests\\chromedriver.exe"
        self.browser = webdriver.Chrome(self.url)
        import time
        time.sleep(5)

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_tag_name("tr")
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 해당 웺 사이트를 확인하러 간다.
        self.browser.get(self.live_server_url)

        # 웹페이지 타이틀과 헤더가 "To-Do"를 표시하고 있다.
        print(self.browser.title)
        self.assertIn("To-Do lists", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do list", header_text)

        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "신규 작업 아이템"
        )

        # "공작깃털 사기:라고 텍스트 상자에 입력한다.
        inputbox.send_keys("공작깃털 사기")

        # 엔터키를 치면 페이지가 갱신되고 작업 목록에
        # "1: 공작깃털 사기" 아이템이 추가된다.
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, "/lists/.+")
        self.check_for_row_in_list_table('1: 공작깃털 사기')


        # 추가 이이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("공작깃털을 이용해서 그물 만들기")
        inputbox.send_keys(Keys.ENTER)

        # 페이지 갱신, 두 개의 아이템이 목록에 보인다.
        table = self.browser.find_element_by_id("id_list_table")
        rows = table.find_elements_by_id("tr")

        # self.assertTrue(
        #     any(row.text == "1: 공작깃털 사기" for row in rows),
        #     "신규 작업 아이템이 테이블에 표시되지 않는다 -- 해당 텍스트:\n%s" % (
        #         table.text
        #     ),
        # )
        # 더 나은 방법 (#2. assertIn을 이용해서 테스팅)
        # self.assertIn("1: 공작깃털 사기", [row.text for row in rows])
        # self.assertIn(
        #     '2: 공작깃털을 이용해서 그물만들기',
        #     [row.text for row in rows]
        # )
        #
        # self.fail("Finish the test!")
        # 3. helper 메소드를 이용해서 테스트하는 방법
        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')
        self.check_for_row_in_list_table('1: 공작깃털 사기')

        # 새호운 사용자인 프란시스가 사이트에 접속한다

        ## 새로운 브라우저 세션을 이용해서 에디스의 정보가
        ## 쿠키를 통해 유입되는 것을 방지한다.
        self.browser.quit()
        self.browser = webdriver.Chrome(self.url)


        # 프란시스가 홈페이지에 접속한다.
        # 에디스의 리스트는 보이지 않는다.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn("공작깃털 사기", page_text)
        self.assertNotIn("그물 만들기", page_text)

        # 프란시스가 새로운 작업 아이템을 입력하기 시작한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 URL을 취득한다
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없다는 것을 다시 확인한다.
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)
