from typing import Literal
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import SimpleDirectoryReader
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor


documents = SimpleDirectoryReader("documents/beyond-the-veil").load_data()
import nest_asyncio

nest_asyncio.apply()
# Create a MemgraphPropertyGraphStore instance
graph_store = Neo4jPropertyGraphStore(
    username="neo4j",
    password="password",
    url="bolt://0.0.0.0:7687"
)


# # recommended uppercase, underscore separated
# entities = Literal["PERSON", "PLACE", "ORGANIZATION"]
# relations = Literal["HAS", "PART_OF", "WORKED_ON", "WORKED_WITH", "WORKED_AT"]

# # define which entities can have which relations
# validation_schema = {
#     "PERSON": ["HAS", "PART_OF", "WORKED_ON", "WORKED_WITH", "WORKED_AT"],
#     "PLACE": ["HAS", "PART_OF", "WORKED_AT"],
#     "ORGANIZATION": ["HAS", "PART_OF", "WORKED_WITH"],
# }


kg_extractor = SchemaLLMPathExtractor(
    llm=OpenAI(model="gpt-4o-mini", temperature=0.0),
    # possible_entities=entities,
    # possible_relations=relations,
    # kg_validation_schema=validation_schema,
    strict=True,
)

# kg_extractor = SchemaLLMPathExtractor(
#     llm=OpenAI(model="gpt-4o-mini", temperature=0.0),
#     possible_entities=entities,
#     possible_relations=relations,
#     kg_validation_schema=schema,
#     strict=True,  # if false, will allow triplets outside of the schema
#     num_workers=4,
#     max_triplets_per_chunk=10,
# )


# Create the index
index = PropertyGraphIndex.from_documents(
    documents,
    embed_model=OpenAIEmbedding(model_name="text-embedding-ada-002"),
    kg_extractors=[
        kg_extractor
    ],
    property_graph_store=graph_store,
    show_progress=True,
)

# Close the Memgraph connection explicitly.
graph_store.close()