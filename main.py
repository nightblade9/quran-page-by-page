# Parses `source.json` and outputs data that's an array of 604 pages.
import json

class Main:
    _SOURCE_FILE = 'source.json'
    _OUTPUT_FILE = 'quran-pages.json'
    _SURAHS_OUTPUT_FILE = 'surah-pages.json'
    
    def run(self):
        with open(Main._SOURCE_FILE, 'r', encoding='utf-8') as file_handle:
            data = json.load(file_handle)

        print(f"Parsing {len(data)} entries from our JSON array ...")

        # Collect the text of each page
        pages = []
        # 604 entries. Each is an array of Qur'anic text.
        current_page = []
        current_page_number = 1

        # Collect the range of pages for each surah
        surahs = [] # 114 entries
        current_surah = [] # list of pages, e.g. [2, 3, 4]
        current_surah_number = 1
        current_surah_name = {"english": "Al-Faatiha", "arabic": "ٱلْفَاتِحَةِ"}

        # Collect each page's data
        for ayah in data:
            arabic = ayah["uthmaniText"]
            page_number = ayah["page"]
            surah_number = ayah["surah"]["number"]

            if page_number == current_page_number:
                current_page.append(arabic)
            else:
                pages.append(current_page)
                current_page = []
                current_page_number = page_number
            
            if surah_number == current_surah_number:
                if page_number not in current_surah:
                    current_surah.append(page_number)
            else:
                #surahs.append(current_surah)
                surah_data = {
                    "arabicName": current_surah_name["arabic"],
                    "englishName": current_surah_name["english"],
                    "startPage": current_surah[0],
                    "endPage": current_surah[len(current_surah) - 1]
                }

                surahs.append(surah_data)
                current_surah = []
                current_surah_number = surah_number
                current_surah_name = {"english": ayah["surah"]["englishName"], "arabic": ayah["surah"]["name"]}
        
        # Final ayah goes on the final page
        pages.append(current_page)
        # Final page goes in final surah
        surahs.append(current_surah)

        #self.write_list_of_pages(pages)
        self.write_surah_pages_index(surahs)

    def write_list_of_pages(self, pages):
        # Write the output, taking care to quote it properly
        with open(Main._OUTPUT_FILE, 'w', encoding='utf-8') as file_handle:
            file_handle.write('[') # top-level array
            
            for page in pages:
                file_handle.write('[') # page start
                quoted_lines = [f'"{x}"' for x in page]

                for line in quoted_lines:
                    file_handle.write(line)

                    if not line == quoted_lines[len(quoted_lines) - 1]:
                        file_handle.write(", ") # between lines
                
                file_handle.write(']') # page end

                if not page == pages[len(pages) - 1]:
                    file_handle.write(', ') # between pages
        
            file_handle.write(']') # top-level array
        
        print(f"Done {len(pages)} pages; check out {Main._OUTPUT_FILE}.")

        # Massage the final output to remove any JSON errors.
        # Fix a bug where we get double-double-quotes, ("") for some reason...
        with open(Main._OUTPUT_FILE, 'r', encoding='utf-8') as file_handle:
            raw = file_handle.read()
        raw = raw.replace('""', '", "')
        with open(Main._OUTPUT_FILE, 'w', encoding='utf-8') as file_handle:
            file_handle.write(raw)

        # TEST IT: load it back and verify that we can parse it (valid JSON)
        with open(Main._OUTPUT_FILE, 'r', encoding='utf-8') as file_handle:
            data = json.load(file_handle)
        print("Confirmed: file is parsable as JSON.")

    def write_surah_pages_index(self, surahs):
         with open(Main._SURAHS_OUTPUT_FILE, 'w', encoding='utf-8') as file_handle:
            file_handle.write('[') # top-level array

            for surah in surahs:
                file_handle.write(json.dumps(surah, ensure_ascii=False))
                if not surah == surahs[len(surahs) - 1]:
                    file_handle.write(', ') # between surahs

            file_handle.write(']') # top-level array

Main().run()