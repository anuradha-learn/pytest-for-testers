# pytest for Testers

Starter project for the free course **pytest for Testers**, by Anuradha Agarwal.

You will learn pytest the way testers use it today: by testing an API and an AI assistant.

The app you test is **NexaDesk Lite**, the IT and HR service desk for the employees of a company called Nexa Group. It runs on your own computer and has:

- **Tickets**: an API with business rules you check against written requirements
- **An AI assistant**: it answers employee questions in different words every time, so simple checks are not enough

The rules are in [REQUIREMENTS.md](REQUIREMENTS.md). The `tests/` folder starts empty. You write every test yourself as you follow the lessons.

- Blog: [anuradhaagarwal.com](https://anuradhaagarwal.com)
- YouTube: [@Anuradha-Agarwal](https://www.youtube.com/@Anuradha-Agarwal)

---

## What you need

- **Python 3.10 or newer**. Download it from [python.org](https://www.python.org/downloads/).
  - Windows: on the first installer screen, tick **Add python.exe to PATH**.
- **A code editor**. The lessons use VS Code, but any editor works.
- **Git** (optional). Only needed if you want to clone the project. You can download a ZIP instead.

No API keys, no accounts and no paid tools are needed. The "AI" in this project is a small fake assistant that runs locally.

---

## Step 1: Get the project

Choose one option.

**Option A: Clone with Git**

```bash
git clone https://github.com/anuradha-learn/pytest-for-testers.git
cd pytest-for-testers
```

**Option B: Download a ZIP from GitHub**

1. On the GitHub page, click the green **Code** button, then **Download ZIP**.
2. Unzip it. The folder will be called `pytest-for-testers-main`. You can rename it to `pytest-for-testers`.
3. Open a terminal inside that folder.

**Option C: Download the ZIP from the course**

Download the ZIP attached to the setup lecture, unzip it, and open a terminal inside the folder.

> All commands below are run from the **project folder** (the one that contains `README.md`).

---

## Step 2: Create and activate a virtual environment

A virtual environment keeps this project's packages separate from the rest of your computer.

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell says running scripts is disabled, run this once, then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

**Windows (Command Prompt)**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS (Terminal)**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When it works, your prompt starts with `(.venv)`. From now on, `python` works on both Windows and macOS.

> Every new terminal window needs the environment activated again.

---

## Step 3: Install the packages

```bash
python -m pip install -r requirements.txt
```

This installs pytest, requests, FastAPI and uvicorn.

---

## Step 4: Check that pytest runs

```bash
pytest
```

Expected result: pytest starts and reports **no tests ran**. That is correct, because `tests/` is empty. You will add tests in the lessons.

---

## Step 5: Start NexaDesk Lite

The tests talk to NexaDesk Lite, so it must be running whenever you run them.

Open a **second terminal** in the project folder, activate the virtual environment again (Step 2), then run:

```bash
uvicorn practice_api.stub_api:app --reload
```

Leave this terminal running. Then open these in your browser:

- NexaDesk web page: <http://127.0.0.1:8000/app>
- API docs: <http://127.0.0.1:8000/docs>
- All tickets: <http://127.0.0.1:8000/tickets>

Stop the API with **Ctrl + C** in that terminal.

### What NexaDesk Lite offers

| Method | Path | What it does |
|---|---|---|
| GET | `/` | Check that NexaDesk Lite is running |
| GET | `/app` | The NexaDesk web page, which calls this same API |
| GET | `/tickets` | List tickets. Optional filters: `?category=IT` or `HR`, `?priority=P1`, `P2` or `P3` |
| GET | `/tickets/{id}` | One ticket. Returns 404 if it does not exist |
| POST | `/tickets` | Create a ticket. Returns 201, or 422 if the data breaks a rule |
| DELETE | `/tickets/{id}` | Delete a ticket. Returns 204, or 404 if it does not exist |
| POST | `/reset` | Put the starting tickets back |
| POST | `/assistant/ask` | Ask the AI assistant a question. Same facts, different wording each time |

You will use `/docs` to explore and try each endpoint before testing it.

---

## Project structure

```
pytest-for-testers/
  practice_api/
    stub_api.py          NexaDesk Lite, the app you test
    nexadesk.html        the NexaDesk web page
  tests/                 empty: your tests go here
  REQUIREMENTS.md        the rules your tests check
  pytest.ini             pytest settings
  requirements.txt       packages to install
  README.md              this file
```

---

## Solutions

Finished tests for every lesson are on the **solutions** branch.

- On GitHub: use the branch dropdown (it says `main`) and pick `solutions`.
- With Git:

  ```bash
  git switch solutions
  ```

  Switch back with `git switch main`.

Try each lesson yourself first. Use the solutions to compare, not to copy.

---

## Troubleshooting

**`python` is not recognized (Windows)**
Reinstall Python and tick **Add python.exe to PATH**, or use `py` instead of `python`, for example `py -m venv .venv`.

**`python: command not found` (macOS)**
Use `python3` to create the environment. After activating it, `python` works.

**`ModuleNotFoundError: No module named 'practice_api'`**
You are not in the project folder. Use `cd` to move into the folder that contains `README.md`, then run the command again.

**`No module named pytest` or `No module named uvicorn`**
The virtual environment is not active in this terminal. Activate it (Step 2).

**`ConnectionError` or `Connection refused` in API tests**
NexaDesk Lite is not running. Start it in a second terminal (Step 5).

**`address already in use` when starting the API**
Another copy of the API is already running. Find that terminal and press Ctrl + C, then start it again.

**API tests pass alone but fail together**
Some tests change the data. The course shows how to reset the API before each test, so watch that lesson before adding more API tests.

---

## Getting help

If something in this project does not work, open an issue on the GitHub repository with:

- your operating system and Python version (`python --version`)
- the command you ran
- the full error message
