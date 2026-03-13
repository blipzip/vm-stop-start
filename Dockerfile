# ---------- Build wheels ----------
FROM python:3.13-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip wheel \
 && pip wheel --wheel-dir /wheels -r requirements.txt


# ---------- Runtime image ----------
FROM python:3.13-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy wheels and install
COPY --from=builder /wheels /wheels
COPY requirements.txt .

RUN pip install --no-cache-dir --no-index \
    --find-links=/wheels \
    -r requirements.txt

# Copy app
COPY app.py .
COPY templates ./templates

# Drop privileges
USER appuser

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
