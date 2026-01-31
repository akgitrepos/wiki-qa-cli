"""Configuration management for Wiki-QA CLI."""

from pathlib import Path
from typing import Literal, Optional
from pydantic import BaseModel, Field
import yaml
import os


class Neo4jConfig(BaseModel):
    """Neo4j database configuration."""

    uri: str = "bolt://localhost:7687"
    user: str = "neo4j"
    password: str = Field(default="", description="Loaded from env var NEO4J_PASSWORD")

    @classmethod
    def from_env(cls) -> "Neo4jConfig":
        """Load Neo4j config from environment variables."""
        return cls(
            uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            user=os.getenv("NEO4J_USER", "neo4j"),
            password=os.getenv("NEO4J_PASSWORD", ""),
        )


class QdrantConfig(BaseModel):
    """Qdrant vector database configuration."""

    url: str = "http://localhost:6333"

    @classmethod
    def from_env(cls) -> "QdrantConfig":
        """Load Qdrant config from environment variables."""
        return cls(url=os.getenv("QDRANT_URL", "http://localhost:6333"))


class OllamaConfig(BaseModel):
    """Ollama LLM configuration."""

    base_url: str = "http://localhost:11434"
    embedding_model: str = "nomic-embed-text"
    llm_model: str = "llama3.2"

    @classmethod
    def from_env(cls) -> "OllamaConfig":
        """Load Ollama config from environment variables."""
        return cls(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            embedding_model=os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"),
            llm_model=os.getenv("OLLAMA_LLM_MODEL", "llama3.2"),
        )


class WikiQASettings(BaseModel):
    """Main application settings."""

    domain: str = "Computer Science"
    article_limit: int = Field(default=1000, ge=1, le=10000)
    qna_strategy: Literal["vector", "graph", "hybrid"] = "hybrid"
    batch_size: int = Field(default=50, ge=1, le=1000)
    concurrent_requests: int = Field(default=10, ge=1, le=50)
    cache_embeddings: bool = True
    enable_citations: bool = True

    neo4j: Neo4jConfig = Field(default_factory=Neo4jConfig)
    qdrant: QdrantConfig = Field(default_factory=QdrantConfig)
    ollama: OllamaConfig = Field(default_factory=OllamaConfig)

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "WikiQASettings":
        """Load settings from YAML file with environment variable overrides."""
        config_path = config_path or Path("config/settings.yaml")

        settings_dict = {}

        if config_path.exists():
            with open(config_path, "r") as f:
                settings_dict = yaml.safe_load(f) or {}

        return cls(
            domain=settings_dict.get("domain", "Computer Science"),
            article_limit=settings_dict.get("article_limit", 1000),
            qna_strategy=settings_dict.get("qna_strategy", "hybrid"),
            batch_size=settings_dict.get("batch_size", 50),
            concurrent_requests=settings_dict.get("concurrent_requests", 10),
            cache_embeddings=settings_dict.get("cache_embeddings", True),
            enable_citations=settings_dict.get("enable_citations", True),
            neo4j=Neo4jConfig.from_env(),
            qdrant=QdrantConfig.from_env(),
            ollama=OllamaConfig.from_env(),
        )

    def save(self, config_path: Path = Path("config/settings.yaml")) -> None:
        """Save settings to YAML file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)

        settings_dict = {
            "domain": self.domain,
            "article_limit": self.article_limit,
            "qna_strategy": self.qna_strategy,
            "batch_size": self.batch_size,
            "concurrent_requests": self.concurrent_requests,
            "cache_embeddings": self.cache_embeddings,
            "enable_citations": self.enable_citations,
        }

        with open(config_path, "w") as f:
            yaml.dump(settings_dict, f, default_flow_style=False, indent=2)


def get_settings(config_path: Optional[Path] = None) -> WikiQASettings:
    """Get application settings."""
    return WikiQASettings.load(config_path)
