import json
from opensearchpy import OpenSearch, helpers

# OpenSearch configuration
host = 'localhost'
port = 9200
auth = ('admin', 'MyStrongPassword123!') # For testing only. Don't store credentials in code.
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Optional client certificates if you don't want to use HTTP basic authentication.
client_cert_path = '/full/path/to/client.pem'
client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    #client_cert = client_cert_path,
    #client_key = client_key_path,
    use_ssl = True,
    #verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    #ca_certs = ca_certs_path
    #use_ssl = False,
    verify_certs = False
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

#document = {
#  'title': 'Moneyball',
#  'director': 'Bennett Miller',
#  'year': '2011'
#}

#response = client.index(
#    index = 'python-test-index',
#    body = document,
#    id = '1',
#    refresh = True
#)

# Bulk index documents
success, failed = helpers.bulk(client, actions, stats_only=True)
print(f"Successfully indexed {success} documents")
if failed:
    print(f"Failed to index {failed} documents")

# Refresh index to make documents searchable
client.indices.refresh(index=index_name)
print("Index refreshed")

# Delete a document by ID
#response = client.delete(index=index_name, id = '1', refresh = True)
