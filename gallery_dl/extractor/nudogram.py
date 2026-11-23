# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extractors for https://nudogram.com/"""

from . import nudostar

BASE_PATTERN = r"(?:https?://)?(?:(?:www|[a-z]{2})\.)?nudogram\.com"


class NudogramExtractor(nudostar.NudostarExtractor):
    """Base class for Nudogram extractors"""
    category = "nudogram"
    root = "https://nudogram.com"


class NudogramModelExtractor(NudogramExtractor,
                             nudostar.NudostarModelExtractor):
    """Extractor for Nudogram models"""
    pattern = BASE_PATTERN + r"(/models/([^/?#]+)/?)(?:[?#]|$)"
    example = "https://nudogram.com/models/MODEL/"


class NudogramImageExtractor(NudogramExtractor,
                             nudostar.NudostarImageExtractor):
    """Extractor for individual Nudogram images"""
    pattern = BASE_PATTERN + r"(/models/([^/?#]+)/(\d+)/?)(?:[?#]|$)"
    example = "https://nudogram.com/models/MODEL/123/"
