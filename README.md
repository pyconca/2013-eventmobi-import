Data-Munging for PyConCa 2013 Mobile Application Import
=======================================================

PyCon Canada 2013 is using a mobile application system from EventMobi for the
conference. Rather than importing data manually, we can make use of the Excel
spreadsheet import functionality to do bulk uploads of data, once we've made
the raw information available from the website.

This isn't exactly pretty code -- it's essentially 100% special cases, nasty
hacks, and one-off stuff to match the way we're doing things this year. It's
probably not very widely applicable, but the ideas and techniques are likely
to be similar to what other users might need to do.


USAGE
-----
Run `refresh.py`, and upload the files found in the new `out` directory.


HACKS
-----
There are several parts of the code that are not particularly nice. You
should be aware of these (and fixes for them would be very welcome):

In the `components.speakers` module, calling `get_speakers` has the
side-effect of creating a temporary directory, downloading speaker photos to
it, cropping them into squares, and zipping up the result. That's not exactly
what you'd expect, given that all the other information is returned as a data
structure.

In the `components.schedule` module, the date of a schedule slot is inferred
after everything else, based on the `start` field from the JSON API. Ideally,
the field should just be added to the data returned from the server.

To correlate speakers and their talks, we really should be getting speaker
IDs from the JSON API. Instead, we get their names, and later use the
`speaker_names_to_ids` function in `components.schedule` to match these names
up with the IDs from the speakers API. Similar stuff goes on for sponsors
and the schedule (sponsorship levels and talk tracks, respectively).

Fields that need to be present in the output spreadsheets but which are not
used are still included in the various `FIELDS` structures, albeit with a
conversion function that just returns `None`.

There's an unexpected dependency on Django. This is because we're using the
`easy-thumbnails` Django application to do speaker photo resizing. It's far
from ideal to have such a big dependency, but the code works well enough.

80% of the code for handling each type of data is a copy/paste job, with a
few special cases and tweaks for each one.

Setting the value of OUTPUT_DIR is duplicated a few times across modules.

There are surely plenty more things that you'll consider dirty hacks too.


LICENSE
-------
Copyright © 2013 Felix Crux (<felixc@felixcrux.com>) & contributors.
Released under the terms of the MIT License ("Expat" version):

  Permission is hereby granted, free of charge, to any person obtaining
  a copy of this software and associated documentation files (the
  "Software"), to deal in the Software without restriction, including
  without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to
  the following conditions:

  The above copyright notice and this permission notice shall be included
  in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
