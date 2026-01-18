import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

def get_opensearch_client():
    """Initialize and return OpenSearch client"""
    region = 'us-east-1'  # Change to your region
    service = 'es'
    
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        service,
        session_token=credentials.token
    )
    
    client = OpenSearch(
        hosts=[{'host': 'your-opensearch-endpoint.region.es.amazonaws.com', 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
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
    index = "my-index"
    field = "category.keyword"  # Use .keyword for exact matches
    
    values = get_dropdown_values(index, field)
    print(f"Dropdown values for {field}:")
    for value in values:
        print(f"  - {value}")
