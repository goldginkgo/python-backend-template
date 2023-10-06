# ================= Generate requirements.txt ==================
FROM python:3.11-slim-bookworm as requirements-stage

WORKDIR /tmp

# Use the Tsinghua pypi mirror
RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple/

COPY ./pyproject.toml ./poetry.lock* /tmp/

# we export pyproject.toml which is poetry-native to plain requirements.txt that we can install with pip
# as it's the recommended approach thanks to which we do not have to install poetry in production-stage image
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# =================       PRODUCTION          ==================
FROM python:3.11-slim-bookworm as production-stage

# Install system dependencies
# Use Tsinghua mirror
RUN sed -i -e 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list.d/debian.sources && \
  apt-get update && \
  apt-get -y install --no-install-recommends libpq-dev gcc g++ curl procps net-tools tini && \
  rm -rf /var/lib/apt/lists/*

# Set up the Python environment
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install the project dependencies
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# Copy the rest of the project files
COPY app/ app/
COPY alembic.ini alembic.ini
COPY alembic/versions alembic/versions
COPY alembic/env.py alembic/env.py

# Create a non-root user and switch to it, for security.
RUN groupadd -g 10001 app && \
  useradd -u 10001 -g app app \
  && chown -R app:app /app

USER app

# Expose the application port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
