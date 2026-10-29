from copilot.models import Job, Application
from copilot.textio import load_text

job = Job(
    company="Example Corp",
    title="Software Engineer",
    location="San Francisco, CA",
    description=load_text("data/jd.txt"),
 )

app = Application(job=job)
print(f"Job: {app.job.title} at {app.job.company}")
print(app)

app.mark_applied(cv_version="v8")
print(app.status, app.applied_on)
print(len(job.keywords()), "keywords in the job description")

app.set_status("interviewing")
print(app.status)

app.set_status("ghosted")