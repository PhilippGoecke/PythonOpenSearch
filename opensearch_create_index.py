from opensearchpy import OpenSearch

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

# Index settings
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

response = client.indices.create(index=index_name, body=index_body)
print("Index created")

#response = client.indices.delete(index=index_name)
