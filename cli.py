#!/usr/bin/env python3
# src/ggp/cli.py
from __future__ import annotations
import click
import logging
import sys
from pathlib import Path
import yaml
from typing import Optional

LOG = logging.getLogger("ggp")

def setup_logging(verbose: bool):
    lvl = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=lvl, format="%(asctime)s %(levelname)s %(message)s")

def load_config(path: Optional[Path]):
    if not path:
        return {}
    with open(path, "r") as f:
        return yaml.safe_load(f)

@click.group()
@click.option("--config", type=click.Path(exists=True), help="Project config YAML.")
@click.option("--verbose", "-v", is_flag=True, help="Verbose logs.")
@click.pass_context
def cli(ctx, config, verbose):
    """ggp — General Game Player toolkit CLI"""
    setup_logging(verbose)
    ctx.obj = {"config": load_config(Path(config)) if config else {}}

@cli.command()
@click.option("--example", type=click.Choice(["ttt", "connect4", "chess"]), default="ttt")
@click.option("--out", type=click.Path(), default="examples")
def init(example: str, out: str):
    """Create skeleton files and example rules."""
    p = Path(out)
    p.mkdir(parents=True, exist_ok=True)
    # copy or render example rule file (implement with templates)
    LOG.info("Scaffolded example %s to %s", example, p.resolve())

@cli.command()
@click.option("--input", "-i", required=True, help="Input PGN/JSON file")
@click.option("--out", "-o", required=True, help="Output traces JSONL")
@click.option("--game", default="chess")
def ingest(input: str, out: str, game: str):
    """Parse PGN or logs into canonical trace JSONL"""
    # call your parser: parse_pgn_to_traces(input, out, game)
    LOG.info("Ingested %s -> %s", input, out)

@cli.command("extract-rules")
@click.option("--traces", "-t", required=True, help="Traces JSONL file or folder")
@click.option("--out", "-o", required=True, help="Output rules JSON")
@click.option("--method", type=click.Choice(["ilp", "llm", "hybrid"]), default="hybrid")
def extract_rules(traces: str, out: str, method: str):
    """Run rule induction (ILP/LLM/hybrid)."""
    LOG.info("Extracting rules from %s using %s", traces, method)
    # run pipeline: load traces, mine rules, write json

@cli.command("validate-rules")
@click.option("--rules", "-r", required=True, help="Rules JSON")
@click.option("--n-sim", default=5, help="Number of random playouts to validate")
def validate_rules(rules: str, n_sim: int):
    """Validate rules by running playouts and checking contradictions."""
    LOG.info("Validating %s with %d sims", rules, n_sim)
    # run validator

@cli.command()
@click.option("--rules", "-r", required=True)
@click.option("--agent", default="mcts")
@click.option("--sims", default=200)
@click.option("--out", default="games/out.jsonl")
def play(rules: str, agent: str, sims: int, out: str):
    """Play a single game with given agent and ruleset."""
    LOG.info("Play: rules=%s agent=%s sims=%d", rules, agent, sims)
    # instantiate RuleSet+Agent, run game, save traces

@cli.command()
@click.option("--config", "-c", type=click.Path(), help="Training config (YAML)")
def train(config: Optional[str]):
    """Start a training run (supervised/offline/rl)."""
    cfg = load_config(Path(config)) if config else {}
    LOG.info("Training with config %s", config or "<inline>")
    # hook into your training module or Ray

@cli.command()
@click.option("--port", default=8000, help="Dev server port")
def serve(port: int):
    """Run the small FastAPI rule-edit server (for demos)."""
    LOG.info("Starting dev server on port %d", port)
    # import and run your FastAPI app: uvicorn.run(...)

if __name__ == "__main__":
    try:
        cli()
    except Exception:
        LOG.exception("Fatal error")
        sys.exit(2)
