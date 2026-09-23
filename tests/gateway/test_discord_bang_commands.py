"""Discord `!command` compatibility tests."""

from hermes_cli.commands import resolve_command
from plugins.platforms.discord.adapter import _rewrite_known_bang_command


def test_bang_model_alias_rewrites_to_slash_command():
    assert _rewrite_known_bang_command("!modèle openrouter/gpt-5") == "/modèle openrouter/gpt-5"
    assert resolve_command("modèle").name == "model"


def test_bang_effort_alias_rewrites_to_reasoning():
    assert _rewrite_known_bang_command("!effort xhigh") == "/effort xhigh"
    assert resolve_command("effort").name == "reasoning"


def test_unknown_bang_text_is_left_alone():
    assert _rewrite_known_bang_command("!important ceci reste du texte") == "!important ceci reste du texte"
