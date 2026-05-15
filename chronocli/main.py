import typer
from chronocli.cli import commands
from chronocli.database.db import init_db
from chronocli.reports.reporter import Reporter
from chronocli.ai.client import GroqClient
from chronocli.dashboard.app import run_dashboard
from rich.console import Console
import os

app = typer.Typer(help="ChronoCLI - AI Powered Time Tracker")
console = Console()

# Include core commands
app.add_typer(commands.app, name="track")

@app.command()
def dashboard():
    """Launch the modern TUI dashboard."""
    run_dashboard()

@app.command()
def report(type: str = "weekly"):
    """Generate a report (daily, weekly, monthly)."""
    days = 1 if type == "daily" else 7 if type == "weekly" else 30
    df = Reporter.get_data_frame(days)
    if df.empty:
        console.print("[yellow]No data found for this period.[/yellow]")
        return
    
    console.print(f"[bold green]{type.capitalize()} Report Summary[/bold green]")
    console.print(df.groupby('category')['duration'].sum())

@app.command()
def export(format: str = "csv"):
    """Export data to CSV or PDF."""
    if format == "csv":
        path = Reporter.export_csv()
        console.print(f"Exported to {path}")
    elif format == "pdf":
        path = Reporter.generate_pdf()
        console.print(f"Exported to {path}")
    else:
        console.print("[red]Unsupported format. Use 'csv' or 'pdf'.[/red]")

@app.command(name="ai-weekly")
def ai_weekly():
    """AI Analysis of your weekly performance."""
    client = GroqClient()
    df = Reporter.get_data_frame(7)
    context = df.to_string() if not df.empty else "No tracking data yet."
    prompt = f"Analyze this week's productivity data and provide a summary with suggestions:\n{context}"
    
    with console.status("[bold blue]Analyzing week..."):
        response = client.get_completion(prompt)
    console.print(f"\n[bold green]Weekly AI Insight[/bold green]\n{response}")

@app.command()
def coach():
    """Get personalized productivity advice from the AI Coach."""
    client = GroqClient()
    df = Reporter.get_data_frame(30)
    context = df.to_string() if not df.empty else "No tracking data yet."
    prompt = f"Based on my last 30 days of work, what are some productivity tips or burnout warnings for me?\n{context}"
    
    with console.status("[bold blue]Consulting Coach..."):
        response = client.get_completion(prompt)
    console.print(f"\n[bold yellow]AI Coach Advice[/bold yellow]\n{response}")

@app.command()
def ask(question: str):
    """Ask a specific question about your tracking data."""
    client = GroqClient()
    df = Reporter.get_data_frame(30)
    context = df.to_string()
    
    with console.status("[bold blue]Thinking..."):
        response = client.get_completion(f"Context:\n{context}\n\nQuestion: {question}")
    console.print(f"\n[bold magenta]AI Response[/bold magenta]\n{response}")

@app.callback()
def main():
    """ChronoCLI - Professional Time Tracking CLI"""
    if not os.path.exists("chronocli.db"):
        init_db()

if __name__ == "__main__":
    app()
