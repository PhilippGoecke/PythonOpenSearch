import json
from opensearchpy import OpenSearch, helpers

# OpenSearch configuration
host = 'localhost'
port = 9200
auth = ('admin', 'MyStrongPassword123!')  # Update with your credentials

# Create OpenSearch client
client = OpenSearch(
    hosts=[{'host': host, 'port': port}],
    http_auth=auth,
    use_ssl=False,
    verify_certs=False,
    ssl_show_warn=False
)

# Index name
index_name = 'my_index'

# Sample data to index
data = [
    {
        'id': 1,
        'title': 'First Document',
        'content': 'This is the content of the first document',
        'timestamp': '2024-01-01T10:00:00'
    },
    {
        'id': 2,
        'title': 'Second Document',
        'content': 'This is the content of the second document',
        'timestamp': '2024-01-02T11:00:00'
    },
    {
        'id': 3,
        'title': 'Third Document',
        'content': 'This is the content of the third document',
        'timestamp': '2024-01-03T12:00:00'
    }
]

# Create index if it doesn't exist
if not client.indices.exists(index=index_name):
    client.indices.create(index=index_name)
    print(f"Index '{index_name}' created")

# Prepare documents for bulk indexing
actions = [
    {
        '_index': index_name,
        '_id': doc['id'],
        '_source': doc
    }
    for doc in data
]

# Bulk index documents
success, failed = helpers.bulk(client, actions, stats_only=True)
print(f"Successfully indexed {success} documents")
if failed:
    print(f"Failed to index {failed} documents")

# Refresh index to make documents searchable
client.indices.refresh(index=index_name)
print("Index refreshed")

