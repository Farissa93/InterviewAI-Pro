<!-- Auto-generated: update with project-specific details when available -->
# Copilot instructions for contributors and AI agents

Purpose
- Help AI coding agents be immediately productive in this repository.

Quick context
- Repository name: Interview prep chatbot — primary code likely lives in top-level folders like `src/`, `app/`, or a single `app.py`/`server.py`.
- I did not find any existing AI instruction files or README in the workspace; please update file paths and commands below if they differ.

How to get the "big picture"
- Inspect the main entry points: search for `main()`, `if __name__ == "__main__"`, `app =`, or `create_app()`.
- Look for API routes and handlers under `src/` or `server/` to understand service boundaries.
- Check for `models/`, `data/`, or `db/` folders to discover data flow and persistence choices.

Build / run / test (project-specific — replace when known)
- Typical Python run: `python -m venv .venv && .venv\Scripts\activate && pip install -r requirements.txt`
- Typical Node run: `npm install && npm start`
- Tests: run `pytest` (Python) or `npm test` (Node). If tests live under `tests/`, run the test runner against that folder.

Project conventions and patterns to follow
- Small, focused commits with descriptive messages.
- Follow existing style if present (PEP8 for Python; ESLint/Prettier for JS). If config files exist, prefer those rules.
- Use feature branches named `feat/<short-desc>` and PR titles that reference issue numbers when available.

Integration points and external dependencies
- Look for `requirements.txt`, `pyproject.toml`, `package.json`, `.env`, or `Dockerfile` for declared dependencies and runtime environment.
- Check for `.github/workflows` for CI steps and any deployment hooks.

What AI agents should do first (concrete steps)
1. Run a repository search for `README.md`, `requirements.txt`, `package.json`, `Dockerfile`, `src/`, and `tests/`.
2. Open the main application entry (common names: `app.py`, `server.py`, `index.js`, `src/main.*`) and summarize its data flow.
3. Find CI workflows under `.github/workflows` and extract test/build commands to reproduce locally.
4. When proposing code changes, include the exact command(s) to run unit tests and linters that your change affects.

Examples from this repo (placeholders — update if incorrect)
- If you find `app.py` with `create_app()`, prefer adding changes to a new route in `src/routes/` and updating `tests/test_routes.py`.
- If you find `package.json` with `scripts.test`, use `npm run test -- <file>` to run a single test file.

Notes for maintainers
- This file was generated automatically because no existing AI guidance files were found. Please edit to add precise commands, file paths, and examples from the real codebase.

Feedback
- If parts of this are unclear or missing (entry points, test command, build steps), paste the relevant file paths or small snippets and request an updated version.

— End of auto-generated guidance —
