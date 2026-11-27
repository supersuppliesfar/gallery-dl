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
from gallery_dl import exception, extractor  # noqa E402
from gallery_dl.extractor import masterfap  # noqa E402
from gallery_dl.extractor.common import Message  # noqa E402


class TestMasterfapExtractor(unittest.TestCase):
    profile_url = "https://www.masterfap.net/profile/example-model/"
    photo_url = profile_url + "photos/abc123/"

    def test_profile_queues_only_its_unique_photo_posts(self):
        extr = extractor.find("https://masterfap.net/profile/example-model")
        self.assertIsInstance(extr, masterfap.MasterfapUserExtractor)
        extr.request = Mock(return_value=Mock(text=(
            f'<a href="{self.photo_url}"><img src="thumbnail.webp"></a>'
            '<a href="photos/abc123/?duplicate=1">Duplicate</a>'
            '<a href="photos/abc123/thumbnail.webp">Thumbnail</a>'
            '<a href="/profile/other-model/photos/def456/">Other profile</a>'
            '<a href="//other.example/profile/example-model/photos/ghi789/">'
            'External</a>'
            '<a class="tile" href="photos/def456/">Another photo</a>'
        )))

        queue = {"_extractor": masterfap.MasterfapImageExtractor}
        self.assertEqual(list(extr.items()), [
            (Message.Queue, self.photo_url, queue),
            (Message.Queue, self.profile_url + "photos/def456/", queue),
        ])
        extr.request.assert_called_once_with(
            self.profile_url, notfound="profile")

    def test_photo_uses_main_image(self):
        extr = extractor.find(self.photo_url + "?ref=test")
        self.assertIsInstance(extr, masterfap.MasterfapImageExtractor)
        extr.request = Mock(return_value=Mock(text=(
            "<title>Example &amp; Model</title>"
            '<img src="/static/logo.png">'
            '<img data-src="thumbnail.webp" src="example-model.webp" '
            'id="showimg2">'
        )))

        directory, image = extr.items()
        self.assertEqual(directory[0], Message.Directory)
        self.assertEqual(image[:2], (
            Message.Url, self.photo_url + "example-model.webp"))
        self.assertEqual(image[2], {
            "profile"      : "example-model",
            "id"           : "abc123",
            "title"        : "Example & Model",
            "filename"     : "example-model",
            "extension"    : "webp",
            "_http_headers": {"Referer": self.photo_url},
        })
        extr.request.assert_called_once_with(self.photo_url, notfound="image")

    def test_missing_photo_does_not_return_site_assets(self):
        extr = extractor.find(self.photo_url)
        extr.request = Mock(return_value=Mock(text=(
            '<meta property="og:image" content="/static/logo.png">'
        )))

        with self.assertRaises(exception.NotFoundError):
            next(extr.items())
