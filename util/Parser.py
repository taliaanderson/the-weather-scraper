import unicodedata
from datetime import datetime


class Parser:
    @staticmethod
    def format_key(key: str) -> str:
        # Replace white space and delete dots
        return key.replace(' ', '_').replace('.', '')

    @staticmethod
    def parse_html_table(date_string: str, history_table: list) -> dict:

        table_rows = [tr for tr in history_table[0].xpath('//tr') if len(tr) == 16]
        headers_list = []
        data_rows = []
        
        # Set overarching headers to match dictionary
        overarch_headers = ['', 'Temperature_','Temperature_','Temperature_','DewPoint_','DewPoint_','DewPoint_','Humidity_',
                   'Humidity_','Humidity_', 'WindSpeed_','WindSpeed_','WindSpeed_','Pressure_','Pressure_', 'Precip_']

        # set Table Headers
        #for header in table_rows[0]:
            #headers_list.append(header.text)
        for i in range(len(table_rows[0])):
    	    all_cols = table_rows[0]
    	    header = all_cols[i]
    	    headers_list.append(overarch_headers[i]+header.text)

        for tr in table_rows[1:]:
            row_dict = {}
            for i, td in enumerate(tr.getchildren()):
                td_content = unicodedata.normalize("NFKD", td.text_content())

                # set date and time in the first 2 columns
                #if i == 0:
                    #date = datetime.strptime(date_string, "%Y-%m-%d")
                    #time = datetime.strptime(td_content, "%I:%M %p")
                    #row_dict['Date'] = date.strftime('%Y/%m/%d')
                   # row_dict['Time'] = time.strftime('%I:%M %p')
                #else:
                row_dict[Parser.format_key(headers_list[i])] = td_content

            data_rows.append(row_dict)
        
        return data_rows
