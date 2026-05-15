from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, DataTable, Label
from textual.containers import Container, Horizontal, Vertical
from chronocli.database.db import get_session
from chronocli.models.models import Session as TrackingSession
from sqlmodel import select
from datetime import datetime

class DashboardApp(App):
    CSS = """
    Screen {
        background: #1a1b26;
    }
    #sidebar {
        width: 30;
        background: #24283b;
        border-right: solid #414868;
        padding: 1;
    }
    #main-content {
        padding: 1;
    }
    .stat-card {
        background: #414868;
        color: white;
        margin: 1;
        padding: 1;
        height: 5;
        border: round #7aa2f7;
    }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Label("[bold cyan]CHRONO CLI[/bold cyan]")
                yield Label("---")
                yield Label("Today's Focus: 4h 20m")
                yield Label("Weekly Streak: 5 days")
                yield Label("Efficiency: 88%")
            with Vertical(id="main-content"):
                yield Label("[bold]Recent Sessions[/bold]")
                yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Task", "Category", "Duration", "Start Time")
        
        with get_session() as session:
            statement = select(TrackingSession).order_by(TrackingSession.start_time.desc()).limit(10)
            sessions = session.exec(statement).all()
            for s in sessions:
                table.add_row(
                    str(s.id),
                    s.task_name,
                    s.category,
                    f"{int(s.duration//60)}m" if s.duration else "Active",
                    s.start_time.strftime("%H:%M")
                )

def run_dashboard():
    app = DashboardApp()
    app.run()

if __name__ == "__main__":
    run_dashboard()
