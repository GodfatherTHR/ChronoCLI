# ChronoCLI ⏱️🚀

**ChronoCLI** is a modern, terminal-first productivity and time-tracking tool built for freelancers, developers, and students. It combines powerful tracking capabilities with AI-driven insights powered by the Groq API.

## 🌟 Features

- **Precise Tracking**: Start, stop, and manage sessions with simple CLI commands.
- **AI Insights**: Personalized productivity coaching, weekly analysis, and natural language command processing.
- **Modern Dashboard**: A beautiful, interactive TUI dashboard built with `Textual`.
- **Rich Reports**: Daily, weekly, and monthly reports with visual tables and stats.
- **Exporting**: Export your data to production-ready CSV and PDF formats.
- **Offline First**: Works fully offline using SQLite; AI features are optional.

## 🚀 Installation

### From PyPI (Recommended)
```bash
pip install chronocli
```

### From Source
```bash
git clone https://github.com/yourusername/ChronoCLI.git
cd ChronoCLI
pip install -e .
```

## ⚙️ Configuration
Create a `.env` file in your project directory (or in the package location) and add your Groq API Key:
```env
GROQ_API_KEY=your_api_key_here
```

## 📖 Usage

### Core Commands
```bash
# Start a task
chronocli track start "Coding New Feature" --category "Development"

# Check status
chronocli track status

# Stop current task
chronocli track stop

# Launch the interactive TUI Dashboard
chronocli dashboard
```

### AI Powered Features
```bash
# Get personalized coaching
chronocli coach

# AI analysis of your week
chronocli ai-weekly

# Ask a specific question about your data
chronocli ask "What time do I usually start working?"
```

### Reporting & Exporting
```bash
# View reports
chronocli report --type weekly

# Export data
chronocli export --format pdf
```

## 🛠️ Project Structure
```
chronocli/
├── ai/          # Groq API integration
├── cli/         # Typer command definitions
├── dashboard/   # Textual TUI app
├── database/    # SQLite & SQLModel logic
├── models/      # Data models
├── reports/     # Analytics engine
└── utils/       # Helpers (Git integration, etc.)
```

## 📜 License
MIT License.
