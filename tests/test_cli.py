"""Tests for CLI module."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.app import (
    display_banner,
    display_menu,
    show_status,
    show_help,
    configure_domain,
    configure_strategy,
)


class TestCLIBanner:
    """Test cases for CLI banner display."""

    def test_display_banner(self, capsys):
        """Test that banner is displayed without error."""
        display_banner()
        captured = capsys.readouterr()

        assert "Wiki-QA CLI" in captured.out
        assert "v1.0.0" in captured.out


class TestCLIMenu:
    """Test cases for CLI menu."""

    def test_display_menu(self, capsys):
        """Test that menu is displayed correctly."""
        display_menu()
        captured = capsys.readouterr()

        assert "Select an option" in captured.out
        assert "Start Q&A Session" in captured.out
        assert "Configure Domain" in captured.out


class TestCLIStatus:
    """Test cases for CLI status."""

    def test_show_status(self, capsys):
        """Test that status is displayed correctly."""
        settings = {
            "domain": "Machine Learning",
            "qna_strategy": "hybrid",
            "article_limit": 1000,
            "enable_citations": True,
        }

        show_status(settings)
        captured = capsys.readouterr()

        assert "Machine Learning" in captured.out
        assert "hybrid" in captured.out
        assert "1000" in captured.out
        assert "Enabled" in captured.out


class TestCLIHelp:
    """Test cases for CLI help."""

    def test_show_help(self, capsys):
        """Test that help is displayed correctly."""
        show_help()
        captured = capsys.readouterr()

        assert "Wiki-QA CLI Help" in captured.out
        assert "vector" in captured.out
        assert "graph" in captured.out
        assert "hybrid" in captured.out


class TestCLIConfigure:
    """Test cases for CLI configuration."""

    @pytest.mark.asyncio
    async def test_configure_domain(self, capsys, monkeypatch):
        """Test domain configuration."""
        monkeypatch.setattr(
            "rich.prompt.Prompt.ask", lambda *args, **kwargs: "Physics"
        )

        settings = {"domain": "Computer Science"}
        await configure_domain(settings)

        assert settings["domain"] == "Physics"

    @pytest.mark.asyncio
    async def test_configure_strategy(self, capsys, monkeypatch):
        """Test strategy configuration."""
        monkeypatch.setattr(
            "rich.prompt.Prompt.ask", lambda *args, **kwargs: "vector"
        )

        settings = {"qna_strategy": "hybrid"}
        await configure_strategy(settings)

        assert settings["qna_strategy"] == "vector"


class TestCLIIntegration:
    """Integration tests for CLI application."""

    def test_app_import(self):
        """Test that CLI module can be imported."""
        from cli.app import main

        assert main is not None

    def test_settings_import(self):
        """Test that settings can be imported."""
        from config.settings import get_settings

        settings = get_settings()
        assert settings.domain == "Computer Science"
