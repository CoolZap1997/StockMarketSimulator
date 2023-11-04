from jugaad_data.nse import NSELive

def find_stock_price(query):
    n = NSELive()
    q = n.stock_quote(query)
    return q['priceInfo']['lastPrice']
