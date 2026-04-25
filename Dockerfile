FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md /app/
COPY ilm_wiki /app/ilm_wiki
COPY config /app/config
COPY data/manual_records /app/data/manual_records
RUN pip install --no-cache-dir -e .

CMD ["ilm-wiki", "run", "--pdf-dir", "data/pdfs", "--manual-dir", "data/manual_records", "--output-dir", "output"]

