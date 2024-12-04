class Config:
    # Flask settings
    SECRET_KEY = 'your_secret_key'
    DEBUG = True

    # Elasticsearch settings
    ELASTICSEARCH_HOST = 'localhost'
    ELASTICSEARCH_PORT = 9200
    ELASTICSEARCH_INDEX = 'imdb_top_1000'
    ELASTICSEARCH_USER = 'elastic'
    ELASTICSEARCH_PASSWORD = 'JAUQB=hnm8KGjYpGlEGc'
    ELASTICSEARCH_SCHEME = 'http'
    ELASTICSEARCH_VERIFY_CERTS = False
    ELASTICSEARCH_URL = 'https://localhost:9200'

    @staticmethod
    def get_elasticsearch_url():
        return f"{Config.ELASTICSEARCH_SCHEME}://{Config.ELASTICSEARCH_HOST}:{Config.ELASTICSEARCH_PORT}"
