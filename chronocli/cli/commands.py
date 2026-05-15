import typer
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from chronocli.database.db import get_session, get_active_session, init_db
from chronocli.models.models import Session as TrackingSession
from sqlmodel import select
from chronocli.utils.git_tools import get_git_info
import time

app = typer.Typer()
console = Console()

@app.command()
def start(task_name: str, category: str = "Personal"):
    """Start a new tracking session."""
    active = get_active_session()
    if active:
        console.print(f"[bold red]Error:[/bold red] Already tracking: '{active.task_name}'")
        raise typer.Exit()
    
    git_info = get_git_info()
    
    with get_session() as session:
        new_session = TrackingSession(
            task_name=task_name, 
            category=category,
            notes=git_info
        )
        session.add(new_session)
        session.commit()
        console.print(f"[bold green]Started tracking:[/bold green] {task_name} ({category})")
        if git_info:
            console.print(f"[dim]{git_info}[/dim]")

@app.command()
def pause():
    """Pause the active tracking session."""
    active = get_active_session()
    if not active or active.is_paused:
        console.print("[bold red]Error:[/bold red] No active or unpaused session.")
        return
    
    with get_session() as session:
        active.is_paused = True
        active.last_pause_time = datetime.now()
        session.add(active)
        session.commit()
        console.print(f"[bold yellow]Paused:[/bold yellow] {active.task_name}")

@app.command()
def resume():
    """Resume a paused tracking session."""
    active = get_active_session()
    if not active or not active.is_paused:
        console.print("[bold red]Error:[/bold red] No paused session.")
        return
    
    with get_session() as session:
        active.is_paused = False
        # Calculate time spent while paused if needed, but here we just toggle
        session.add(active)
        session.commit()
        console.print(f"[bold green]Resumed:[/bold green] {active.task_name}")

@app.command()
def stop():
    """Stop the active tracking session."""
    active = get_active_session()
    if not active:
        console.print("[bold red]Error:[/bold red] No active session found.")
        raise typer.Exit()
    
    with get_session() as session:
        active.end_time = datetime.now()
        duration = (active.end_time - active.start_time).total_seconds()
        active.duration = duration
        session.add(active)
        session.commit()
        
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        console.print(f"[bold blue]Stopped tracking:[/bold blue] {active.task_name}")
        console.print(f"Duration: {minutes}m {seconds}s")

@app.command()
def status():
    """Check the status of current session."""
    active = get_active_session()
    if not active:
        console.print("[yellow]No active session.[/yellow]")
    else:
        elapsed = (datetime.now() - active.start_time).total_seconds()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        console.print(f"[bold green]Active Session:[/bold green] {active.task_name}")
        console.print(f"Started at: {active.start_time.strftime('%H:%M:%S')}")
        console.print(f"Elapsed: {minutes}m {seconds}s")

@app.command()
def list_sessions(limit: int = 10):
    """List recent tracking sessions."""
    with get_session() as session:
        statement = select(TrackingSession).order_by(TrackingSession.start_time.desc()).limit(limit)
        results = session.exec(statement).all()
        
        table = Table(title="Recent Sessions")
        table.add_column("ID", style="cyan")
        table.add_column("Task", style="magenta")
        table.add_column("Category", style="green")
        table.add_column("Duration", style="yellow")
        table.add_column("Date", style="blue")
        
        for s in results:
            duration_str = f"{int(s.duration // 60)}m" if s.duration else "Active"
            table.add_row(
                str(s.id),
                s.task_name,
                s.category,
                duration_str,
                s.start_time.strftime("%Y-%m-%d")
            )
        
        console.print(table)

@app.command()
def pomodoro(minutes: int = 25):
    """Start a Pomodoro timer."""
    console.print(f"[bold red]Pomodoro Started:[/bold red] {minutes} minutes of focus!")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description="Focusing...", total=minutes * 60)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)
    
    console.print("[bold green]Time's up![/bold green] Take a break.")

if __name__ == "__main__":
    init_db()
    app()
