#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os
import sys
import unittest
from unittest.mock import Mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gallery_dl import extractor  # noqa E402
from gallery_dl.extractor import nudogram  # noqa E402
from gallery_dl.extractor.common import Message  # noqa E402


class TestNudogramExtractor(unittest.TestCase):
    root = "https://nudogram.com"
    model_url = root + "/models/gigantits/"
    image_url = root + "/contents/g/i/gigantits/1000/gigantits_0112.jpg"
    title = "Gigantits / Gigantitsx / gigantit Nude Leaks OnlyFans"

    def extract(self, url, page):
        extr = extractor.find(url)
        extr.request = Mock(return_value=Mock(text=page))
        messages = [(msg, url, data.copy()) for msg, url, data in extr.items()]
        extr.request.assert_called_once_with(
            extr.page_url, notfound=extr.subcategory)
        return messages

    def test_model(self):
        page = (
            f"<title>{self.title} - Nudogram v2.1</title>"
            '<script src="https://nudogram.com/js/main.js"></script>'
            f'<img src="{self.image_url[:-4]}_280.jpg">'
        )
        messages = self.extract(self.model_url, page)
        self.assertEqual(len(messages), 113)
        self.assertEqual(messages[0][0], Message.Directory)
        self.assertEqual(messages[0][2], {
            "gallery_id": "gigantits",
            "model_slug": "gigantits",
            "model_names": ["Gigantits", "Gigantitsx", "gigantit"],
            "model": "Gigantits",
            "title": "",
            "count": 112,
        })
        self.assertEqual(messages[1][1],
                         self.image_url.replace("0112", "0001"))
        self.assertEqual(messages[-1][1], self.image_url)
        self.assertEqual(messages[1][2]["num"], 1)
        self.assertEqual(messages[-1][2]["num"], 112)
        self.assertTrue(all(msg[0] == Message.Url for msg in messages[1:]))

    def test_model_thousand_boundary(self):
        extr = nudogram.NudogramModelExtractor.from_url(self.model_url)
        page = ('<img src="https://nudogram.com/contents/g/i/gigantits/'
                '3000/gigantits_2001_280.jpg">')
        images = extr.images(page)
        self.assertEqual(len(images), 2001)
        for num, folder in ((1, 1000), (999, 1000), (1000, 2000),
                            (1999, 2000), (2000, 3000), (2001, 3000)):
            with self.subTest(num=num):
                self.assertEqual(images[num-1], (
                    f"{self.root}/contents/g/i/gigantits/"
                    f"{folder}/gigantits_{num:04}.jpg", None))

    def test_image(self):
        page = (
            f"<title>{self.title} Photo #112 - Nudogram v2.1</title>"
            '<div class="headline"><h1>Gigantits</h1></div>'
            f'<a href="{self.image_url}"><img class="img-content" '
            f'src="{self.image_url}"></a>'
            '<img class="thumb" src="https://nudogram.com/contents/'
            'o/t/other/1000/other_0001_280.jpg">'
        )
        messages = self.extract(self.model_url + "112/", page)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0][0], Message.Directory)
        self.assertEqual(messages[1][0:2], (Message.Url, self.image_url))
        self.assertEqual(messages[1][2]["num"], 112)
        self.assertEqual(messages[1][2]["filename"], "gigantits_0112")
        self.assertEqual(messages[1][2]["model"], "Gigantits")

    def test_url_matching(self):
        for prefix in (self.root, "http://nudogram.com", "nudogram.com",
                       "https://www.nudogram.com", "https://de.nudogram.com"):
            for suffix, cls in (
                    ("", nudogram.NudogramModelExtractor),
                    ("/112", nudogram.NudogramImageExtractor)):
                for ending in ("", "/", "/?ref=test", "/#photo"):
                    url = prefix + "/models/gigantits" + suffix + ending
                    with self.subTest(url=url):
                        extr = extractor.find(url)
                        self.assertIsInstance(extr, cls)
                        self.assertEqual(extr.category, "nudogram")
                        self.assertEqual(extr.root, self.root)
        for path in ("/models/", "/models/gigantits/videos/",
                     "/models/gigantits/112/other/", "/models/gigantits/112x"):
            with self.subTest(path=path):
                self.assertIsNone(extractor.find(self.root + path))

    def test_nudostar_regression(self):
        extr = extractor.find("https://nudostar.tv/models/eva-joys/")
        page = ('<img class="thumb" src="https://nudostar.tv/contents/'
                'e/v/eva-joys/1000/eva-joys_0054_320px.jpg">')
        images = extr.images(page)
        self.assertEqual(len(images), 54)
        self.assertEqual(images[0], (
            "https://nudostar.tv/contents/e/v/eva-joys/1000/eva-joys_0001.jpg",
            None))
        self.assertEqual(images[-1], (
            "https://nudostar.tv/contents/e/v/eva-joys/1000/eva-joys_0054.jpg",
            None))


if __name__ == "__main__":
    unittest.main()
