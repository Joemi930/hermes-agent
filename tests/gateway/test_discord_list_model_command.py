"""Tests for the Discord !list-model inventory command."""

import asyncio
import unittest
from unittest.mock import patch

from gateway.slash_commands_model import GatewayModelCommandsMixin


class _Runner(GatewayModelCommandsMixin):
    pass


class _Event:
    def __init__(self, args=""):
        self._args = args

    def get_command_args(self):
        return self._args


class TestListModelCommand(unittest.TestCase):
    def test_list_model_returns_authenticated_catalogs(self):
        runner = _Runner()
        with patch(
            "hermes_cli.model_switch.list_authenticated_providers",
            return_value=[{"slug": "copilot", "name": "GitHub Copilot", "models": ["gpt-5.6-luna"], "total_models": 1}],
        ):
            out = asyncio.run(runner._handle_list_model_command(_Event()))
        self.assertIn("GitHub Copilot", out)
        self.assertIn("gpt-5.6-luna", out)

    def test_list_model_filters_provider_and_supports_refresh(self):
        runner = _Runner()
        with patch(
            "hermes_cli.model_switch.list_authenticated_providers",
            return_value=[
                {"slug": "copilot", "name": "GitHub Copilot", "models": ["gpt-5.6-luna"], "total_models": 1},
                {"slug": "anthropic", "name": "Anthropic", "models": ["claude-opus-5"], "total_models": 1},
            ],
        ) as mocked:
            out = asyncio.run(runner._handle_list_model_command(_Event("anthropic --refresh")))
        self.assertIn("Anthropic", out)
        self.assertIn("claude-opus-5", out)
        self.assertNotIn("GitHub Copilot", out)
        mocked.assert_called_once()
        self.assertTrue(mocked.call_args.kwargs["refresh"])


if __name__ == "__main__":
    unittest.main()
