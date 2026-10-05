from urllib.parse import quote_plus

CATALOG = {
    "home": [
        {"name":"LED Ceiling Light", "category":"lighting", "price":1499, "platform":"Amazon", "query":"LED ceiling light"},
        {"name":"Minimalist Floor Lamp", "category":"lighting", "price":3299, "platform":"IKEA", "query":"floor lamp"},
        {"name":"Compact Study Table", "category":"furniture", "price":4999, "platform":"Amazon", "query":"compact study table"},
        {"name":"Dining Table 4 Seater", "category":"furniture", "price":12999, "platform":"IKEA", "query":"4 seater dining table"},
        {"name":"Decorative Wall Art Set", "category":"decor", "price":1799, "platform":"Flipkart", "query":"wall art decor set"},
        {"name":"Indoor Planter", "category":"decor", "price":899, "platform":"IKEA", "query":"indoor planter"},
        {"name":"Ceiling Fan", "category":"appliances", "price":2899, "platform":"Amazon", "query":"ceiling fan"},
    ],
    "party": [
        {"name":"Vegetarian Catering Package", "category":"catering", "price":450, "unit":"per guest", "platform":"Zomato", "query":"party catering"},
        {"name":"Party Meal Package", "category":"catering", "price":550, "unit":"per guest", "platform":"Swiggy", "query":"party food"},
        {"name":"Birthday Decoration Kit", "category":"decoration", "price":2499, "platform":"Amazon", "query":"birthday decoration kit"},
        {"name":"Balloon Decoration Set", "category":"decoration", "price":1599, "platform":"Flipkart", "query":"balloon decoration"},
        {"name":"Budget Event Room", "category":"venue", "price":2500, "unit":"per night", "platform":"OYO", "query":"event accommodation"},
    ],
    "jewelry": [
        {"name":"Pearl Drop Earrings", "category":"earrings", "price":1299, "platform":"Amazon", "query":"pearl drop earrings"},
        {"name":"Gold-Tone Necklace Set", "category":"necklace", "price":2499, "platform":"Flipkart", "query":"gold tone necklace set"},
        {"name":"Minimal Bracelet", "category":"bracelet", "price":999, "platform":"Amazon", "query":"minimal bracelet"},
        {"name":"Statement Jhumka Earrings", "category":"earrings", "price":1799, "platform":"Flipkart", "query":"jhumka earrings"},
        {"name":"Kundan-Style Necklace", "category":"necklace", "price":3999, "platform":"Amazon", "query":"kundan necklace"},
    ]
}

def link_for(item):
    domains = {"Amazon":"https://www.amazon.in/s?k=", "Flipkart":"https://www.flipkart.com/search?q=", "IKEA":"https://www.ikea.com/in/en/search/?q=", "Swiggy":"https://www.swiggy.com/search?query=", "Zomato":"https://www.zomato.com/search?q=", "OYO":"https://www.oyorooms.com/search?location="}
    return domains[item["platform"]] + quote_plus(item["query"])

def fallback_recommendations(planner: str, budget: float, context: dict):
    items = CATALOG[planner]
    selected = []
    remaining = budget
    if planner == "party":
        guests = max(1, int(context.get("guests", 1)))
        for item in items:
            if item["category"] == "catering":
                total = item["price"] * guests
                if total <= budget * 0.7:
                    selected.append({**item, "estimated_total": total, "url": link_for(item)})
                    break
        for item in items:
            if item["category"] != "catering" and item["price"] <= budget * 0.4:
                selected.append({**item, "estimated_total": item["price"], "url": link_for(item)})
                if len(selected) >= 4: break
    else:
        for item in sorted(items, key=lambda x: x["price"]):
            price = item["price"]
            if price <= remaining * 0.65:
                selected.append({**item, "estimated_total": price, "url": link_for(item)})
                remaining -= price
            if len(selected) >= 5: break
    return selected
