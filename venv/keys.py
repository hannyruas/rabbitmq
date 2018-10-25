
PATH = "C:\\Users\HannyBuns\Desktop\sqlite\chinook\chinook.db"

CSV = "csv"
XML = "xml"
JSON = "json"

SONGS_INFO_NAME = "song_info"
CUSTOMERS_INFO_NAME = "customers_info"
DOMAIN_TO_COUNTRY_NAME = "domain_to_country"
INVOICES_TO_COUNTRY_NAME = "invoice_to_country"

SONGS_INFO = "SELECT tracks.Name as tracks_name, genres.Name as genres_name, artists.Name as artists_name FROM tracks" \
             " INNER JOIN genres ON genres.GenreId=tracks.GenreId JOIN albums ON albums.AlbumId = tracks.AlbumId " \
             "JOIN artists ON artists.ArtistId = albums.ArtistId;"

CUSTOMERS_INFO = "SELECT FirstName, LastName, Phone, Email, Address FROM customers;"

DOMAIN_TO_COUNTRY = "select country, count (Domain) as domain_number, Domain from " \
                    "(select country, substr(Email, instr(Email, '@') + 1) as Domain from customers) As C " \
                    "GROUP By Domain order by country"

INVOICES_TO_COUNTRY = "SELECT customers.Country, COUNT (invoices.InvoiceID) FROM invoices, customers " \
                      "where customers.CustomerId == invoices.CustomerId GROUP BY customers.Country"