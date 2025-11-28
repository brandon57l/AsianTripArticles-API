import datetime
from bson import ObjectId
from bson.errors import InvalidId
from db import articles_collection

def serialize_doc(doc):
    """
    Converts MongoDB document fields (like ObjectId and datetime) to JSON-serializable formats.
    """
    if not doc:
        return None
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    if 'published_at' in doc and isinstance(doc['published_at'], datetime.datetime):
        doc['published_at'] = doc['published_at'].isoformat()
    return doc

def find_articles_by_keywords(keywords: list):
    """
    Searches for articles where the title, summary, or paragraphs match any of the given keywords.
    """
    regex_pattern = "|".join(keywords)
    query = {
        "$or": [
            {"title": {"$regex": regex_pattern, "$options": "i"}},
            {"summary": {"$regex": regex_pattern, "$options": "i"}},
            {"sections.paragraphs": {"$regex": regex_pattern, "$options": "i"}}
        ]
    }
    projection = {
        "title": 1, "summary": 1, "published_at": 1, "url": 1, "author": 1
    }
    
    cursor = articles_collection.find(query, projection)
    results = [serialize_doc(doc) for doc in cursor]

    return {
        "status": "success", "code": 200,
        "meta": {
            "query": keywords,
            "total_results": len(results),
            "timestamp": datetime.datetime.now().isoformat()
        },
        "data": results
    }

def get_article_by_id(article_id: str):
    """
    Fetches a single, complete article by its unique ID.
    """
    try:
        oid = ObjectId(article_id)
    except (InvalidId, TypeError):
        return {"status": "error", "code": 400, "message": "Invalid article ID format."}

    article = articles_collection.find_one({"_id": oid})
    if not article:
        return {"status": "error", "code": 404, "message": "Article not found."}

    return {
        "status": "success", "code": 200,
        "meta": {"fetched_id": article_id},
        "data": serialize_doc(article)
    }

def get_article_table_of_contents(article_id: str):
    """
    Retrieves just the titles of all sections for a given article, serving as a table of contents.
    """
    try:
        oid = ObjectId(article_id)
    except (InvalidId, TypeError):
        return {"status": "error", "code": 400, "message": "Invalid article ID format."}

    projection = {"sections.title": 1}
    article = articles_collection.find_one({"_id": oid}, projection)
    if not article:
        return {"status": "error", "code": 404, "message": "Article not found."}

    titles = [sec['title'] for sec in article.get('sections', [])]
    return {
        "status": "success", "code": 200,
        "meta": {"article_id": article_id},
        "data": {"table_of_contents": titles}
    }

def get_article_section_by_title(article_id: str, title: str):
    """
    Finds and returns the content of a specific section within an article by its exact title (case-insensitive).
    """
    try:
        oid = ObjectId(article_id)
    except (InvalidId, TypeError):
        return {"status": "error", "code": 400, "message": "Invalid article ID format."}

    article = articles_collection.find_one({"_id": oid})
    if not article:
        return {"status": "error", "code": 404, "message": "Article not found."}

    found_section = None
    if 'sections' in article:
        for sec in article['sections']:
            if title.lower() == sec['title'].lower():
                found_section = sec
                break

    if found_section:
        return {
            "status": "success", "code": 200,
            "meta": {
                "article_id": str(article['_id']),
                "searched_section_title": title
            },
            "data": found_section
        }
    else:
        return {"status": "error", "code": 404, "message": f"No section with the title '{title}' found."}
