from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from config import Config
import os
from utils.es_utils import wait_for_elasticsearch

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

try:
    # Configure Elasticsearch with connection verification
    app.elasticsearch = wait_for_elasticsearch()
except ConnectionError as e:
    print(f"Failed to connect to Elasticsearch: {e}")
    exit(1)



@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    filters = {
        'genre': request.args.get('Genre', ''),
        'imdb_rating': request.args.get('IMDB_Rating', ''),
        'released_year': request.args.get('Released_Year', ''),
        'certificate': request.args.get('Certificate', '')
    }
    sort_by = request.args.get('sort', 'rating')

    must_filters = []
    
    if filters['genre']:
        must_filters.append({"match": {"Genre": filters['genre']}})
    if filters['imdb_rating']:
        must_filters.append({"range": {"IMDB_Rating": {"gte": float(filters['imdb_rating'])}}})
    if filters['released_year']:
        must_filters.append({"term": {"Released_Year": int(filters['released_year'])}})
    if filters['certificate']:
        must_filters.append({"match": {"Certificate": filters['certificate']}})

    sort_options = {
        "rating": [{"IMDB_Rating": "desc"}],
        "year": [{"Released_Year": "desc"}],
        "title": [{"Series_Title.keyword": "asc"}],
        "votes": [{"No_of_Votes": "desc"}],
        "gross": [{"Gross": "desc"}]
    }

    try:
        body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": [
                                    "Series_Title^3",
                                    "Overview^2",
                                    "Genre",
                                    "Director",
                                    "Star1",
                                    "Star2",
                                    "Star3",
                                    "Star4"
                                ],
                                "fuzziness": "AUTO"
                            }
                        }
                    ] + must_filters
                }
            },
            "sort": sort_options.get(sort_by, sort_options["rating"])
        }

        response = app.elasticsearch.search(
            index="imdb_top_1000",
            body=body
        )

        results = [
            {
                'Poster_Link': hit['_source'].get('Poster_Link'),
                'Series_Title': hit['_source'].get('Series_Title'),
                'Released_Year': hit['_source'].get('Released_Year'),
                'Certificate': hit['_source'].get('Certificate'),
                'Runtime': hit['_source'].get('Runtime'),
                'Genre': hit['_source'].get('Genre'),
                'IMDB_Rating': hit['_source'].get('IMDB_Rating'),
                'Overview': hit['_source'].get('Overview'),
                'Meta_score': hit['_source'].get('Meta_score'),
                'Director': hit['_source'].get('Director'),
                'Star1': hit['_source'].get('Star1'),
                'Star2': hit['_source'].get('Star2'),
                'Star3': hit['_source'].get('Star3'),
                'Star4': hit['_source'].get('Star4'),
                'No_of_Votes': hit['_source'].get('No_of_Votes'),
                'Gross': hit['_source'].get('Gross')
            }
            for hit in response['hits']['hits']
        ]

        return jsonify(results)

    except Exception as e:
        print(f"Search error: {e}")
        return jsonify({"error": "Search failed"}), 500


@app.route('/api/save-recommendation', methods=['POST'])
def save_recommendation():
    data = request.get_json()
    user_id = data.get('user_id')
    recommendation = data.get('recommendation')
    
    if not user_id or not recommendation:
        return jsonify({"error": "User ID and recommendation are required"}), 400
    
    # Save the recommendation to the user's profile
    app.elasticsearch.index(index="user_recommendations", body={
        "user_id": user_id,
        "recommendation": recommendation,
        "timestamp": "now"
    })
    
    return jsonify({"message": "Recommendation saved successfully"})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=Config.DEBUG)