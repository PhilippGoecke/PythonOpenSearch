from opensearchpy import OpenSearch

# Configure OpenSearch connection
host = 'localhost'
port = 9200
auth = ('admin', 'MyStrongPassword123!')  # Default credentials, change as needed

# Create OpenSearch client
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=False,
    verify_certs=False,
    ssl_show_warn=False
)

# Search configuration
index_name = 'my_index'
search_string = 'your search term'

# Perform search
query = {
    'query': {
        'match': {
            '_all': search_string  # Search across all fields
        }
    }
}

# Alternative: Search in specific field
# query = {
#     'query': {
#         'match': {
#             'field_name': search_string
#         }
#     }
# }

# Execute search
response = client.search(
    index=index_name,
    body=query
)

# Display results
print(f"Found {response['hits']['total']['value']} results:")
for hit in response['hits']['hits']:
    print(f"\nScore: {hit['_score']}")
    print(f"Source: {hit['_source']}")
