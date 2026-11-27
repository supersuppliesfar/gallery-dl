# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from gallery_dl.extractor import nudogram


__tests__ = (
{
    "#url"    : "https://nudogram.com/models/gigantits/",
    "#class"  : nudogram.NudogramModelExtractor,
    "#pattern": r"https://nudogram\.com/contents/g/i/gigantits/1000/gigantits_\d{4}\.jpg",
    "#count"  : range(112, 200),

    "count"      : range(112, 200),
    "num"        : range(1, 200),
    "extension"  : "jpg",
    "filename"   : r"re:gigantits_\d{4}",
    "gallery_id" : "gigantits",
    "model"      : "Gigantits",
    "model_slug" : "gigantits",
    "model_names": ["Gigantits", "Gigantitsx", "gigantit"],
},

{
    "#url"    : "https://de.nudogram.com/models/gigantits/",
    "#class"  : nudogram.NudogramModelExtractor,
},

{
    "#url"    : "https://nudogram.com/models/gigantits/112/",
    "#class"  : nudogram.NudogramImageExtractor,
    "#results": "https://nudogram.com/contents/g/i/gigantits/1000/gigantits_0112.jpg",

    "extension"  : "jpg",
    "filename"   : "gigantits_0112",
    "gallery_id" : "gigantits",
    "num"        : 112,
    "url"        : "https://nudogram.com/contents/g/i/gigantits/1000/gigantits_0112.jpg",
    "model"      : "Gigantits",
    "model_slug" : "gigantits",
    "model_names": ["Gigantits", "Gigantitsx", "gigantit"],
},

)
