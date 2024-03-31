# Parses `source.json` and outputs data that's an array of 604 pages.
import json

class Main:
    _SOURCE_FILE = 'source.json'
    _OUTPUT_FILE = 'quran-pages.json'
    
    def run(self):
        with open(Main._SOURCE_FILE, 'r', encoding='utf-8') as file_handle:
            data = json.load(file_handle)

        print(f"Parsing {len(data)} entries from our JSON array ...")

        pages = []
        # 604 entries. Each is an array of Qur'anic text.
        current_page = []
        current_page_number = 1

        for ayah in data:
            arabic = ayah["uthmaniText"]
            page_number = ayah["page"]

            if page_number == current_page_number:
                current_page.append(arabic)
            else:
                pages.append(current_page)
                current_page = []
                current_page_number = page_number
        
        # Final ayah
        pages.append(current_page)

        with open(Main._OUTPUT_FILE, 'w', encoding='utf-8') as file_handle:
            file_handle.write('[')
            
            for page in pages:
                file_handle.write(json.dumps(page))

                if not page == pages[len(pages) - 1]:
                    file_handle.write(', ')
        
            file_handle.write(']')
        
        print(f"Done {len(pages)} pages; check out {Main._OUTPUT_FILE}.")

Main().run()