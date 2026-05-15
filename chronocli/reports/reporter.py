import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from chronocli.database.db import get_session
from chronocli.models.models import Session as TrackingSession
from sqlmodel import select
from datetime import datetime, timedelta
import os

class Reporter:
    @staticmethod
    def get_data_frame(days=7):
        with get_session() as session:
            start_date = datetime.now() - timedelta(days=days)
            statement = select(TrackingSession).where(TrackingSession.start_time >= start_date)
            results = session.exec(statement).all()
            
            data = [
                {
                    "id": s.id,
                    "task": s.task_name,
                    "category": s.category,
                    "start": s.start_time,
                    "end": s.end_time,
                    "duration": s.duration / 3600 if s.duration else 0  # Hours
                }
                for s in results
            ]
            return pd.DataFrame(data)

    @staticmethod
    def export_csv(filename="exports/report.csv"):
        os.makedirs("exports", exist_ok=True)
        df = Reporter.get_data_frame(30)
        df.to_csv(filename, index=False)
        return filename

    @staticmethod
    def generate_pdf(filename="exports/report.pdf"):
        os.makedirs("exports", exist_ok=True)
        df = Reporter.get_data_frame(7)
        
        # Create a simple chart
        if not df.empty:
            plt.figure(figsize=(8, 4))
            df.groupby('category')['duration'].sum().plot(kind='pie', autopct='%1.1f%%')
            plt.title("Time Distribution by Category")
            plt.savefig("exports/chart.png")
            plt.close()

        c = canvas.Canvas(filename, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "ChronoCLI Productivity Report")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        if not df.empty:
            total_hours = df['duration'].sum()
            c.drawString(100, 700, f"Total Tracked Hours (Last 7 Days): {total_hours:.2f}")
            c.drawImage("exports/chart.png", 100, 400, width=400, height=200)
        else:
            c.drawString(100, 700, "No data found for the last 7 days.")
            
        c.save()
        return filename
