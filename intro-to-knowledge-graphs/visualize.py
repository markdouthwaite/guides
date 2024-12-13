from pyvis.network import Network
from neo4j import GraphDatabase, Result

AUTH = ("neo4j", "password")
URI = "neo4j://localhost:7687"

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    results = driver.execute_query("MATCH (n)-[r]-(b) RETURN n, r, b;", result_transformer_=Result.graph)

g = Network()

for node in results.nodes:

    name = node["name"]

    if name is None:
        name = node["file_name"]
    
    node_label = list(node.labels)[0]
    node_text = node["labels"]
    g.add_node(node.element_id, name, group=node_label)

for relationship in results.relationships:
    g.add_edge(
        relationship.start_node.element_id,
        relationship.end_node.element_id,
        title=relationship.type
    )

g.save_graph("example.html")