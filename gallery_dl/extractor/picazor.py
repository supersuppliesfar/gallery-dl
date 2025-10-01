# -*- coding: utf-8 -*-

# Copyright 2025
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://picazor.com/"""

from .common import Extractor, Message
from .. import text, util

BASE_PATTERN = r"(?:https?://)?(?:www\.)?picazor\.com"


class PicazorExtractor(Extractor):
    """Base class for picazor extractors"""
    category = "picazor"
    root = "https://picazor.com"
    directory_fmt = ("{category}", "{user}")
    filename_fmt = "{num:>03}_{filename}.{extension}"
    archive_fmt = "{user}_{id}"


class PicazorUserExtractor(PicazorExtractor):
    """Extractor for all images from a picazor user"""
    subcategory = "user"
    pattern = BASE_PATTERN + r"/(?:en|[a-z]{2})/([^/?#]+)/?$"
    example = "https://picazor.com/en/USER"

    def __init__(self, match):
        PicazorExtractor.__init__(self, match)
        self.user = match.group(1)

    def items(self):
        data = {"user": self.user}
        yield Message.Directory, data

        for num, image_data in enumerate(self._get_all_files(), 1):
            image_data["num"] = num
            image_data.update(data)
            yield Message.Url, image_data["url"], image_data

    def _get_all_files(self):
        """Get all files via pagination API"""
        page = 1

        while True:
            url = f"{self.root}/api/files/{self.user}/sfiles"
            params = {"page": page}

            try:
                files = self.request(url, params=params).json()
            except Exception as e:
                self.log.debug("Failed to fetch page %d: %s", page, e)
                break

            if not files or not isinstance(files, list):
                break

            file_count = 0
            for file_data in files:
                if not isinstance(file_data, dict):
                    continue

                path = file_data.get("path")
                if not path:
                    continue

                if not path.startswith("/uploads/"):
                    continue

                file_url = self.root + path
                filename = path.split('/')[-1]

                yield {
                    "url": file_url,
                    "id": file_data.get("id", filename.rsplit('.', 1)[0] if '.' in filename else filename),
                    "order": file_data.get("order", 0),
                    "filename": filename.rsplit('.', 1)[0] if '.' in filename else filename,
                    "extension": filename.rsplit('.', 1)[1] if '.' in filename else "jpg",
                }
                file_count += 1

            if file_count == 0:
                break

            page += 1

