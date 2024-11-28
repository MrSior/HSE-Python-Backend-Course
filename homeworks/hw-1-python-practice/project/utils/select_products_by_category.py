def select_products_by_category(products, category):
    res = []
    for p in products:
        if p.category == category:
            res.append(p)
    return res
