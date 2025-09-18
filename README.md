Partid-0

Phase 1 ▶ “Rule‑driven Player”

Goal: Given a formal rule set, spin up an agent that can play any turn‑based, perfect‑information game. (Standard GGP Creation)

1.1 Rule Loader	• Parser for GDL/VGDL/JSON rules
• Pydantic/Prolog‑based validator
1.2 Generic Game API	• GameState interface: legal_moves(), step(move), is_terminal(), reward()
• Adapters: Tic‑Tac‑Toe, Chess (via python‑chess), Connect‑4
1.3 Baseline Agent	• Random and Minimax baselines
• Tiny MCTS (pure CPU)
1.4 Integration Test & Demo	• CLI: play --rules=chess.gdl --agent=mcts --sims=100
• Record one full game to PGN/log

Phase 2 ▶ “Human‑in‑the‑Loop Rule Elicitor”

Goal: Build the chatbot/API that ingests example games (PGN or log traces) and asks clarifying questions to output a machine‑readable rule set.

2.1 FastAPI Chatbot Skeleton	• POST /chat on GPT‑4o with streaming
• Conversation state in PostgreSQL + pgvector	1 week
2.2 Rule‑Extraction Prompts & Schema	• JSON schema for rules
• Prompt templates + function‑calling tests on tic‑tac‑toe & chess	1 week
2.3 Validation Harness	• Load extracted rules into Phase 1’s Rule Loader
• Auto‑play 1–2 playouts, flag contradictions	1 week
2.4 User Interface & Versioning	• Simple React UI or Swagger UI
• Rule diffs & version history	1 week

Phase 2.5 ▶ “Optimize & Profile”

Goal: Take your Phase 1 agent and squeeze performance; swap in learned rules.
Deliverable	Components	Timeline
2.5.1 Profiler Integration	• PyTorch Profiler / nvidia‑smi hooks
• Flamegraphs for MCTS & encoding	1 week
2.5.2 Hot‑loop Port	• Identify slowest MCTS subroutine
• Reimplement in C++ (pybind11) or TorchScript	1 week
2.5.3 Hyperparameter Sweep	• Ray Tune experiments: sims vs. latency vs. win‑rate
• Auto‑report best config	1 week
2.5.4 Benchmark Report	• Dashboard of throughput, memory, energy
• README badges with “best sims/sec”	1 week

Phase 3 ▶ “Cross‑Game Mastery Network”

Goal: Learn transferable heuristics/embeddings across games to warm‑start new titles.
Deliverable	Components	Timeline
3.1 Representation Learning	• Train a graph or transformer model over game graphs/traces
• Produce per‑state embeddings	2 weeks
3.2 Meta‑Agent API	• API to query embed = Encoder(state, game_id)
• Feed embed into Phase 1’s value/policy nets	2 weeks
3.3 Transfer Experiments	• Zero‑shot agent on an unseen game (e.g., small board size variant)
• Measure jump‑start win‑rate vs. from‑scratch	2 weeks
3.4 End‑to‑End Demo & Paper	• Web demo: “Pick Game → Show rules → Play with meta‑warm start”
• 6‑page write‑up on transfer gains	2 weeks
