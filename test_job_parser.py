from app.job_parser import parse_job_description

jd = """
We are looking for a Data Scientist with experience in Python, SQL,
Machine Learning, and FastAPI. React is a plus.
"""

print(parse_job_description(jd))
