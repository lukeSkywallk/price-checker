#from scraper import Scraper
from configProperties import ConfigProperties
from drive import Drive

folder = None
configProperties = ConfigProperties()
drive = Drive()
DRIVE_FOLDER_ID = configProperties.get_value('DEFAULT', 'drive.folder.id')

if not DRIVE_FOLDER_ID:
    drive = Drive()
    folder = drive.create_folder('price_checker')
    DRIVE_FOLDER_ID = folder['id']

    if not DRIVE_FOLDER_ID:
        print('ERROR: was not possible to create the drive folder for price-checker')
        sys.exit()

    configProperties.save_value('DEFAULT', 'drive.folder.id', DRIVE_FOLDER_ID)


for product in configProperties.get_products():
    if not product.spreadsheet_id:
        spreadsheet = drive.create_google_spreadsheet(product.name, DRIVE_FOLDER_ID)
        if spreadsheet:
            product.spreadsheet_id = spreadsheet.id
            configProperties.save_value(product.name, 'spreadsheet.id', spreadsheet.id)
    
    if product.spreadsheet_id:
        drive_spreadsheet = drive.open_google_spreadsheet(product.spreadsheet_id)
        if drive_spreadsheet:
            for site in product.sites_list:
                worksheet = None
                try:
                    worksheet = drive_spreadsheet.worksheet(site.site_type.name)
                except:
                    worksheet = drive_spreadsheet.add_worksheet(site.site_type.name, 1000, 1000)
                
                
                available_row = drive.next_available_row(worksheet)
                last_row = int(available_row) - 1
                last_value_cell = None
                if last_row > 0:
                    last_cell = 'A' + str(last_row)
                    last_value_cell = worksheet.acell(last_cell).value
    
                preco = buscaPreco()#aqui

                if last_value_cell is not None:
                    if last_value_cell != preco:
                        cell_edit = 'A' + str(available_row)
                        worksheet.update(cell_edit, save)