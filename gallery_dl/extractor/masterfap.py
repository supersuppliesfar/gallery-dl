# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://www.masterfap.net/"""

from .common import Extractor, Message
from .. import text

BASE_PATTERN = r"(?:https?://)?(?:www\.)?masterfap\.net/profile/([\w-]+)"
URL_END = r"/?(?:[?#]|$)"
PHOTO_PATTERN = BASE_PATTERN + r"/photos/([\w-]+)" + URL_END


class MasterfapExtractor(Extractor):
    """Base class for MasterFap extractors"""
    category = "masterfap"
    root = "https://www.masterfap.net"
    directory_fmt = ("{category}", "{profile}")
    filename_fmt = "{id}.{extension}"
    archive_fmt = "{profile}_{id}"


class MasterfapImageExtractor(MasterfapExtractor):
    """Extractor for individual photos on MasterFap"""
    subcategory = "image"
    pattern = PHOTO_PATTERN
    example = "https://www.masterfap.net/profile/PROFILE/photos/ID/"

    def items(self):
        profile, photo_id = self.groups
        page_url = f"{self.root}/profile/{profile}/photos/{photo_id}/"
        page = self.request(page_url, notfound="image").text

        image = text.re(r'<img\b[^>]*\sid="showimg2"[^>]*>').search(page)
        src = image and text.re(r'\ssrc="([^"]+)"').search(image[0])
        if not src:
            raise self.exc.NotFoundError("image")
        url = text.urljoin(page_url, text.unescape(src[1]))
        data = {
            "profile": profile,
            "id"     : photo_id,
            "title"  : text.unescape(text.extr(page, "<title>", "</title>")),
            "_http_headers": {"Referer": page_url},
        }
        yield Message.Directory, "", data
        yield Message.Url, url, text.nameext_from_url(url, data)


class MasterfapUserExtractor(MasterfapExtractor):
    """Extractor for photos from a MasterFap profile"""
    subcategory = "user"
    pattern = BASE_PATTERN + URL_END
    example = "https://www.masterfap.net/profile/PROFILE/"

    def items(self):
        profile = self.groups[0]
        page_url = f"{self.root}/profile/{profile}/"
        page = self.request(page_url, notfound="profile").text

        photo_pattern = text.re(PHOTO_PATTERN)
        links = text.re(r'<a\b[^>]*\shref="([^"]+)"').findall(page)
        seen = set()
        data = {"_extractor": MasterfapImageExtractor}
        for href in links:
            url = text.urljoin(page_url, text.unescape(href))
            if not (match := photo_pattern.match(url)) or match[1] != profile:
                continue
            photo_id = match[2]
            if photo_id not in seen:
                seen.add(photo_id)
                yield Message.Queue, f"{page_url}photos/{photo_id}/", data
