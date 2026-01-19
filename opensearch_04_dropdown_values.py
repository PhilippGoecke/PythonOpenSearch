import boto3
from opensearchpy import OpenSearch

def get_opensearch_client():
    """Initialize and return OpenSearch client"""

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
    
    return client

def get_dropdown_values(index_name, field_name, max_results=100):
    """
    Get unique values from a field to populate dropdown
    
    Args:
        index_name: Name of the OpenSearch index
        field_name: Field to get unique values from
        max_results: Maximum number of results to return
    
    Returns:
        List of unique values
    """
    client = get_opensearch_client()
    
    query = {
        "size": 0,
        "aggs": {
            "unique_values": {
                "terms": {
                    "field": field_name,
                    "size": max_results
                }
            }
        }
    }
    
    response = client.search(index=index_name, body=query)
    
    # Extract values from aggregation buckets
    dropdown_values = [
        bucket['key'] 
        for bucket in response['aggregations']['unique_values']['buckets']
    ]
    
    return dropdown_values

if __name__ == "__main__":
    # Example usage
    index_name = 'my_index'
    field = "category.keyword"  # Use .keyword for exact matches
    
    values = get_dropdown_values(index_name, field)
    print(f"Dropdown values for {field}:")
    for value in values:
        print(f"  - {value}")
