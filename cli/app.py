"""Main CLI application entry point."""

from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

from config.settings import get_settings


console = Console()


def display_banner() -> None:
    """Display application banner."""
    banner = """
╔══════════════════════════════════════════════════╗
║          Wiki-QA CLI v1.0.0                      ║
║    Intelligent Document Q&A System               ║
╚══════════════════════════════════════════════════╝
"""
    console.print(Panel(Text(banner, justify="center"), style="bold cyan"))


def display_menu() -> None:
    """Display main menu options."""
    menu_text = """
[bold]Select an option:[/bold]

  [1] Start Q&A Session (Computer Science)
  [2] Configure Domain
  [3] Change Q&A Strategy
  [4] View Status
  [5] Help
  [6] Exit
"""
    console.print(menu_text)


async def configure_domain(settings: dict) -> None:
    """Configure the domain for Q&A."""
    console.print("\n[bold]Current domain:[/bold] " + settings["domain"])

    domain = Prompt.ask(
        "\nEnter domain (e.g., 'Machine Learning', 'Physics'):",
        default="Computer Science",
    )

    settings["domain"] = domain
    console.print(f"\n[green]Domain set to: {domain}[/green]")


async def configure_strategy(settings: dict) -> None:
    """Configure the Q&A strategy."""
    console.print("\n[bold]Current strategy:[/bold] " + settings["qna_strategy"])

    strategy = Prompt.ask(
        "\nSelect strategy:",
        choices=["vector", "graph", "hybrid"],
        default="hybrid",
    )

    settings["qna_strategy"] = strategy
    console.print(f"\n[green]Strategy set to: {strategy}[/green]")


def show_status(settings: dict) -> None:
    """Show current application status."""
    status_text = f"""
[bold]Current Settings[/bold]

  Domain: {settings["domain"]}
  Strategy: {settings["qna_strategy"]}
  Article Limit: {settings["article_limit"]}
  Citations: {"Enabled" if settings["enable_citations"] else "Disabled"}
"""
    console.print(Panel(status_text, title="Status"))


def show_help() -> None:
    """Show help information."""
    help_text = """
[bold]Wiki-QA CLI Help[/bold]

This application enables intelligent Q&A over Wikipedia articles
by combining vector search (Qdrant) and graph traversal (Neo4j).

[bold]Commands:[/bold]
  1 - Start an interactive Q&A session
  2 - Set the domain/topic (default: Computer Science)
  3 - Change search strategy (vector, graph, hybrid)
  4 - View current configuration
  5 - Show this help message
  6 - Exit the application

[bold]Search Strategies:[/bold]
  vector  - Use semantic similarity search only
  graph   - Use knowledge graph traversal only
  hybrid  - Combine both for best results (recommended)

[bold]Note:[/bold]
  Run 'python -m pipeline.streamer' first to index articles.
"""
    console.print(Panel(help_text, title="Help"))


async def main() -> None:
    """Main application entry point."""
    display_banner()

    settings = get_settings()
    settings_dict = {
        "domain": settings.domain,
        "article_limit": settings.article_limit,
        "qna_strategy": settings.qna_strategy,
        "enable_citations": settings.enable_citations,
    }

    while True:
        display_menu()

        choice = Prompt.ask(
            "Enter your choice",
            choices=["1", "2", "3", "4", "5", "6"],
            default="1",
        )

        if choice == "1":
            console.print("\n[yellow]Q&A session not yet implemented.[/yellow]")
            console.print("[yellow]Run the ingestion pipeline first.[/yellow]\n")

        elif choice == "2":
            await configure_domain(settings_dict)

        elif choice == "3":
            await configure_strategy(settings_dict)

        elif choice == "4":
            show_status(settings_dict)

        elif choice == "5":
            show_help()

        elif choice == "6":
            console.print("\n[bold green]Goodbye![/bold green]\n")
            break


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
