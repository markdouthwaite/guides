from typing import Literal
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor


graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="password",
    url="bolt://127.0.0.1:7687"
)

llm = OpenAI(model="gpt-4o-mini", temperature=0.0)
kg_extractors = [SchemaLLMPathExtractor(llm=llm)]

index = PropertyGraphIndex.from_existing(
    property_graph_store=graph_store,
    kg_extractors=kg_extractors,
    embed_model=OpenAIEmbedding(model_name="text-embedding-ada-002"),
    show_progress=True,
)

query_engine = index.as_query_engine(include_text=True)
response = query_engine.query("Who does Paul Graham know?")
print(response)