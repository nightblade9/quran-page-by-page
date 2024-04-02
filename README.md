# Page by Page Qur'an

Page by page data of the Qur'an. For making apps and stuff. 

# Structure

For page-by-page data, check out `quran-pages.json`. It's a JSON array of 604 pages. Each page is an array of text strings (lines between ayaat).

For an index of which surahs contain which pages, check out `quran-surahs.json`. It's an array of elements. Each element contains the surah name (in Arabic and English), and `startPage` and `endPage` indexes. Note that these are base-1, like a real book, not base-0.

Source data: https://github.com/onattech/QuranJSON
