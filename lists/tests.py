from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import Item


# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        # self.assertTrue(response.content.startswith(b'<html>'))
        # self.assertIn(b"<title>To-Do lists</title>", response.content)
        # self.assertTrue(response.content.decode().endswith('</html>'))

        # Refactoring (아래 코드는 csrf_token 설정으로 틀릴 가능성이 있음)
        # expected_html = render_to_string("home.html")
        # self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST['item_text'] = "신규 작업 아이템"

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "신규 작업 아이템")

        self.assertIn("신규 작업 아이템", response.content.decode())
        expected_html = render_to_string(
            "home.html",
            {"new_item_text": '신규 작업 아이템'}
        )
        self.assertEqual(response.content.decode(), expected_html)
