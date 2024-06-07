import csv 

csv_file_path = ...
data = ... 

def get_post_content(item):
    ...

fieldnames = [
    "post_title", "post_content", "post_name", "post_author", "post_status", 
    "featured_image", "post_format", "comment_status", "ping_status", 
    "rank_math_pillar_content", "index", "nofollow", "noimageindex", 
    "noindex", "noarchive", "nosnippet", "rank_math_advanced_robots", 
    "headline", "post_category", "post_tag"
]


with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for item in data:
        post_content = get_post_content(item)
        post_title = ...
        portada = ...
        tags = ...
        row = {
            "post_title": post_title,
            "post_content": post_content,
            "post_name": post_title.replace(" ", "-").lower(),
            "post_author": "admin",
            "post_status": "publish",
            "featured_image": portada,
            "post_format": "standard",
            "comment_status": "closed",
            "ping_status": "open",
            "rank_math_pillar_content": "on",
            "index": "1",
            "nofollow": "",
            "noimageindex": "",
            "noindex": "", 
            "noarchive": "",
            "nosnippet": "",
            "rank_math_advanced_robots": "-1,-1,large",
            "headline": "article_headline",
            "post_category": "categoria",
            "post_tag": f"{tags}"
        }
        writer.writerow(row)
