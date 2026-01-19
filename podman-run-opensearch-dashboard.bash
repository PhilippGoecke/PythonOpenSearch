podman run -d --name opensearch-dashboard --publish 5601:5601 -e OPENSEARCH_HOSTS='["https://host.containers.internal:9200"]' docker.io/opensearchproject/opensearch-dashboards:3.4.0

echo "Access it at: http://localhost:5601"
echo "Default credentials: admin / MyStrongPassword123!"
