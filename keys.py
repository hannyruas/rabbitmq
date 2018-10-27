
PATH = "C:\\Users\HannyBuns\Desktop\sqlite\chinook\chinook.db"

ENCODED_ERROR = "Encoded character can not be write into a file"

CSV = "csv"
XML = "xml"
JSON = "json"
SQL_TABLE = "sql_table"


SONGS_INFO_NAME = "song_info"
CUSTOMERS_INFO_NAME = "customers_info"
DOMAIN_TO_COUNTRY_NAME = "domain_to_country"
INVOICES_TO_COUNTRY_NAME = "invoice_to_country"
BEST_SOLD_FROM_2011_NAME = "best_sold_from_2011"
CUSTOMERS_MISSING_2_OR_MORE_INVOICE_COLUMNS_NAME = "customers_missing_2_or_more_invoice_columns"
MAX_SALS_ALBUM_TO_COUNTRY_NAME = "max_sals_album_to_country"


SONGS_INFO = "SELECT tracks.Name AS tracks_name, albums.Title AS title, artists.Name AS artists_name, " \
             "genres.Name AS genres_name " \
             "FROM tracks, genres, artists, albums " \
             "WHERE genres.GenreId=tracks.GenreId AND albums.AlbumId = tracks.AlbumId " \
             "AND artists.ArtistId = albums.ArtistId"

CUSTOMERS_INFO = "SELECT customers.FirstName AS first_name, customers.LastName AS last_name, " \
                 "customers.Phone AS phone_number, customers.Email AS email," \
                 " customers.Address AS address FROM customers"

DOMAIN_TO_COUNTRY = "SELECT domain_name, country, COUNT(*) AS num_of_album_invoices FROM (SELECT country, " \
                    "substr(substr(Email, instr(Email, '@') + 1),1, instr(substr(Email, instr(Email, '@') + 1), '.')-1)"\
                    " AS domain_name FROM customers) GROUP BY domain_name, country HAVING COUNT(*) > 0"

INVOICES_TO_COUNTRY = "SELECT customers.Country, COUNT (invoices.InvoiceID) AS num_of_sold FROM invoices, customers " \
                      "WHERE customers.CustomerId == invoices.CustomerId GROUP BY customers.Country"

MAX_SALS_ALBUM_TO_COUNTRY = "SELECT country, title, MAX(num_of_album_invoices) AS max_sals FROM " \
                            "(SELECT title, country, COUNT(*) AS num_of_album_invoices FROM " \
                            "(SELECT albums.Title AS title, invoices.BillingCountry AS country " \
                            "FROM invoices,invoice_items, tracks, albums " \
                            "WHERE invoices.InvoiceId == invoice_items.InvoiceId " \
                            "AND invoice_items.TrackId == tracks.TrackId " \
                            "AND tracks.AlbumId == albums.AlbumId ORDER BY country)"\
                            "GROUP BY title, country HAVING COUNT(*) > 1) GROUP BY country"

BEST_SOLD_FROM_2011 = "SELECT MAX (num_of_invoice) AS num_of_sold, title AS best_sold FROM " \
                      "(SELECT title, COUNT (*) AS num_of_invoice FROM " \
                      "(SELECT invoice_items.TrackId, albums.Title  AS title  " \
                      "FROM invoice_items, tracks,albums, invoices " \
                      "WHERE  invoices.InvoiceDate < '2011-01-01 00:00:00'" \
                      "AND invoices.invoiceId == invoice_items.invoiceId " \
                      "AND tracks.TrackId == invoice_items.TrackId " \
                      "AND albums.AlbumId == tracks.AlbumId) " \
                      "GROUP BY title)"
CUSTOMERS_MISSING_2_OR_MORE_INVOICE_COLUMNS= "SELECT customers.CustomerId AS customer_id, " \
                                             "customers.FirstName AS first_name, customers.LastName AS last_name" \
                                             " FROM customers," \
                                             "(SELECT CustomerId as Id, " \
                                             "CASE WHEN InvoiceId IS NULL THEN 1 ELSE 0 END +  " \
                                             "CASE WHEN CustomerId IS NULL THEN 1 ELSE 0 END + " \
                                             "CASE WHEN InvoiceDate IS NULL THEN 1 ELSE 0 END + " \
                                             "CASE WHEN CustomerId IS NULL THEN 1 ELSE 0 END + " \
                                             "CASE WHEN BillingAddress IS NULL THEN 1 ELSE 0 END + " \
                                             "CASE WHEN BillingCity IS NULL THEN 1 ELSE 0 END +" \
                                             "CASE WHEN BillingState IS NULL THEN 1 ELSE 0 END + " \
                                             "CASE WHEN BillingCountry IS NULL THEN 1 ELSE 0 END + " \
                                             "CASE WHEN BillingPostalCode IS NULL THEN 1 ELSE 0 END + " \
                                             "CASE WHEN Total  IS NULL THEN 1 ELSE 0 END AS num_of_null " \
                                             "FROM invoices GROUP BY Id) AS count_nulls WHERE  num_of_null>=2 " \
                                             "AND count_nulls.Id ==  customers.CustomerId"

QUERY_NAMES =[SONGS_INFO_NAME, CUSTOMERS_INFO_NAME, DOMAIN_TO_COUNTRY_NAME, INVOICES_TO_COUNTRY_NAME,
              MAX_SALS_ALBUM_TO_COUNTRY_NAME, BEST_SOLD_FROM_2011_NAME, CUSTOMERS_MISSING_2_OR_MORE_INVOICE_COLUMNS_NAME]

QUERYS =[SONGS_INFO, CUSTOMERS_INFO, DOMAIN_TO_COUNTRY, INVOICES_TO_COUNTRY, MAX_SALS_ALBUM_TO_COUNTRY,
         BEST_SOLD_FROM_2011, CUSTOMERS_MISSING_2_OR_MORE_INVOICE_COLUMNS]