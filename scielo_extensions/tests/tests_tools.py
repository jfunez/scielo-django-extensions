# coding: utf-8
from django.test import TestCase
from django.template import Context, Template

class ToolsTest(TestCase):
    def test_paginator_factory(self):
        """
        Wraps django paginator object to handle some common
        validations.
        """
        from scielo_extensions.tools import get_paginated

        items_list = [chr(i) for i in range(97, 123)]
        page_num = 1
        items_per_page = 5

        paginated = get_paginated(items_list, page_num, items_per_page=items_per_page)

        self.assertEqual(paginated.paginator.count, 26)
        self.assertEqual(paginated.paginator.num_pages, 6)
        self.assertTrue(hasattr(paginated, 'object_list'))
        self.assertEqual(len(paginated.object_list), 5)

        del(paginated)

        # When requiring a non-existing page, the last one is retrieved
        paginated = get_paginated(items_list, 10, items_per_page=items_per_page)
        self.assertEqual(paginated.number, paginated.paginator.num_pages)

        del(paginated)

        # Testing if page parameter is integer
        paginated = get_paginated(items_list, str(1), items_per_page=items_per_page)

        self.assertEqual(paginated.paginator.count, 26)
        self.assertEqual(paginated.paginator.num_pages, 6)
        self.assertTrue(hasattr(paginated, 'object_list'))
        self.assertEqual(len(paginated.object_list), 5)

        del(paginated)

        # Testing if page parameter is a "string"
        self.assertRaises(TypeError, get_paginated, items_list, 'foo', items_per_page=items_per_page)

    def test_named_pagination(self):

        from django.http import HttpRequest

        request = HttpRequest()

        list_letter = ('f','u','r','p','m','t','a','t','z')

        html = '{% load scielo_common %}'
        html += '{% named_pagination list_letter selected %}'

        template = Template(html)
        context = Context({'list_letter': sorted(list_letter), 'selected': 'f', 'request': request})

        result_html = template.render(context)

        self.assertEqual('''<div class="pagination">
            <ul><li><a href="?">All</a></li>
                <li><a href="?letter=a">a</a></li>
                <li class="active"><a href="?letter=f">f</a></li>
                <li><a href="?letter=m">m</a></li>
                <li><a href="?letter=p">p</a></li>
                <li><a href="?letter=r">r</a></li>
                <li><a href="?letter=t">t</a></li>
                <li><a href="?letter=t">t</a></li>
                <li><a href="?letter=u">u</a></li>
                <li><a href="?letter=z">z</a></li>
            </ul></div>''', result_html)
