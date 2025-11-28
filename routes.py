from flask import Blueprint, request, jsonify
import services

# Create a Blueprint to organize routes
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/articles/search', methods=['GET'])
def search_articles():
    """
    Searches for articles based on a single keyword in the 'q' query parameter.
    Example: /api/articles/search?q=tokyo
    """
    query_string = request.args.get('q', '')
    if not query_string:
        return jsonify({"status": "error", "code": 400, "message": "Query parameter 'q' is missing."}), 400
    
    # Now, the query_string is treated as a single keyword.
    result = services.find_articles_by_keyword(query_string)
    return jsonify(result), result.get('code', 200)

@api_blueprint.route('/articles/<article_id>', methods=['GET'])
def get_article(article_id):
    """
    Retrieves a full article by its unique ID.
    Example: /api/articles/60c72b2f9b1d8c001f8e4a9c
    """
    result = services.get_article_by_id(article_id)
    return jsonify(result), result.get('code', 200)

@api_blueprint.route('/articles/<article_id>/toc', methods=['GET'])
def get_toc(article_id):
    """
    Gets the table of contents (a list of section titles) for a specific article.
    'toc' stands for Table of Contents.
    Example: /api/articles/60c72b2f9b1d8c001f8e4a9c/toc
    """
    result = services.get_article_table_of_contents(article_id)
    return jsonify(result), result.get('code', 200)

@api_blueprint.route('/articles/<article_id>/sections/<section_title>', methods=['GET'])
def get_section_by_title(article_id, section_title):
    """
    Retrieves a specific section from an article by its full title.
    The section title in the URL is case-insensitive and spaces should be URL-encoded (e.g., %20).
    Example: /api/articles/some_id/sections/A%20Famous%20Landmark
    """
    # The section_title is automatically URL-decoded by Flask
    result = services.get_article_section_by_title(article_id, section_title)
    return jsonify(result), result.get('code', 200)
