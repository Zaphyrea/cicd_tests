FROM python:3.11

RUN pip install poetry  
RUN mkdir -p /app  
COPY . /app

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

RUN poetry install

# Expose port 5000 for the container
EXPOSE 5000

RUN poetry install 

CMD ["poetry", "run", "python",  "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]