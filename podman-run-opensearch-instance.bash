podman run -d --name opensearch-node --publish 9200:9200 --publish 9600:9600 -e "discovery.type=single-node" -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=MyStrongPassword123!" -e "DISABLE_SECURITY_PLUGIN=false" -v opensearch-data:/usr/share/opensearch/data docker.io/opensearchproject/opensearch:3.4.0

echo "Access it at: http://localhost:9200"
echo "Default credentials: admin / MyStrongPassword123!"
